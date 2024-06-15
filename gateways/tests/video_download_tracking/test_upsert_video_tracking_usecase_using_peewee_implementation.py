from os import path
from tempfile import mkdtemp

from domain.entity.video.download_status import DownloadingStatus
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError
from usecases.output.video_persisting.video_download_tracking.update_video_download_tracking_usecase import (
    UpdateVideoDownloadTrackingUseCase,
)

from gateways.implementations.repository.video_download_tracker.peewee_implementation import (
    PeeweeDownloadingTracker,
)
from tests.utilities.constants import valid_downloaded_youtube_video


def test_happy_path() -> None:
    destination_path: str = mkdtemp()
    downloading_tracker = PeeweeDownloadingTracker(
        database_destination_path=destination_path
    )

    update_status = UpdateVideoDownloadTrackingUseCase(
        download_tracking_repository=downloading_tracker
    ).execute(
        video_url=valid_downloaded_youtube_video.video_url,
        video_resolution=valid_downloaded_youtube_video.resolution,
        video_title=valid_downloaded_youtube_video.video_title,
        destination_path=destination_path,
        downloading_status=DownloadingStatus.FINISHED,
    )

    assert update_status is None
    assert path.exists(path.join(destination_path, "database.db"))


def test_invalid_destination_path_path() -> None:
    destination_path: str = "invalid"
    downloading_tracker = PeeweeDownloadingTracker(database_destination_path=mkdtemp())

    update_status = UpdateVideoDownloadTrackingUseCase(
        download_tracking_repository=downloading_tracker
    ).execute(
        video_url=valid_downloaded_youtube_video.video_url,
        video_resolution=valid_downloaded_youtube_video.resolution,
        video_title="nothing for now",
        destination_path=destination_path,
        downloading_status=DownloadingStatus.FINISHED,
    )

    assert isinstance(update_status, UseCaseExecutionError)
    assert isinstance(update_status.invalid_entity, VideoTrackingRepositoryUpdateError)
    assert (
        update_status.invalid_entity.error_msg
        == f"This destination path [{destination_path}] doesn't exist !"
    )
