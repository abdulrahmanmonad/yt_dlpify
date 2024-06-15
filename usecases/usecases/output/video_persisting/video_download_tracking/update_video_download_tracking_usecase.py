from os import path

from domain.entity.video.download_status import DownloadingStatus
from domain.entity.video.youtube import ToBeDownloadedYouTubeVideo

from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError
from usecases.input.interface.repository.downloading_tracker import (
    DownloadingTrackerInterface,
)
from usecases.input.interface.shared.generic_usecase import GenericUseCaseInterface


class UpdateVideoDownloadTrackingUseCase(GenericUseCaseInterface):
    def __init__(
        self, *, download_tracking_repository: DownloadingTrackerInterface
    ) -> None:
        self.__download_tracking_repository = download_tracking_repository

    def execute(
        self,
        *,
        video_url: str,
        video_resolution: int,
        destination_path: str,
        downloading_status: DownloadingStatus,
    ) -> VideoTrackingRepositoryUpdateError | None:
        if not path.exists(destination_path):
            return VideoTrackingRepositoryUpdateError(
                error_msg=f"This destination path [{destination_path}] doesn't exist !",
                invalid_entity=ToBeDownloadedYouTubeVideo(
                    video_url=video_url,
                    resolution=video_resolution,
                    destination_path=destination_path,
                ),
            )

        return self.__download_tracking_repository.insert_or_update_entry(
            video_url=video_url,
            video_resolution=video_resolution,
            destination_path=destination_path,
            downloading_status=downloading_status,
        )
