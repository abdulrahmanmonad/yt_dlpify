from os import path
from typing import Type

from domain.entity.video.download_status import DownloadingStatus
from domain.entity.video.youtube import ToBeDownloadedYouTubeVideo
from peewee import IntegrityError, Model
from playhouse.sqlite_ext import SqliteExtDatabase
from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError
from usecases.input.interface.repository.downloading_tracker import (
    DownloadingTrackerInterface,
)

from gateways.implementations.repository.video_download_tracker.peewee_implementation.models.download_tracking import (
    DownloadTrackingModel,
)


class PeeweeDownloadingTracker(DownloadingTrackerInterface):
    def __init__(
        self, *, database_destination_path: str, database_name: str = "database.db"
    ) -> None:
        self.__database_destination_path = database_destination_path
        self.__database_name = database_name
        self.__models: dict[str, Type[Model]] = dict(
            download_tracking_model=DownloadTrackingModel
        )

        database_full_path: str = path.join(
            self.__database_destination_path, self.__database_name
        )

        self.__db = SqliteExtDatabase(database=database_full_path)

        for model in self.__models.values():
            model.bind(self.__db)

        self.__db.create_tables(self.__models.values())

    def insert_or_update_entry(
        self,
        *,
        video_url: str,
        video_resolution: int,
        video_title: str,
        destination_path: str,
        downloading_status: DownloadingStatus
    ) -> VideoTrackingRepositoryUpdateError | None:
        try:
            (
                self.__models["download_tracking_model"]
                .insert(
                    video_url=video_url,
                    video_resolution=video_resolution,
                    video_title=video_title,
                    destination_path=destination_path,
                    downloading_status=downloading_status.value,
                )
                .on_conflict_replace()
                .execute()
            )
            return None
        except IntegrityError as err:
            return VideoTrackingRepositoryUpdateError(
                error_msg=str(err),
                invalid_entity=ToBeDownloadedYouTubeVideo(
                    video_url=video_url,
                    resolution=video_resolution,
                    destination_path=destination_path,
                ),
            )
