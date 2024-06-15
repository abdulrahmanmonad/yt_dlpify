from tempfile import mkdtemp

from domain.entity.video.download_status import DownloadingStatus

from tests.utilities.shared.functions import (
    generate_random_string_without_digits,
    generate_random_url,
)
from tests.utilities.video_download_tracking import DummyDownloadingTrackerInterface
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError
from usecases.output.video_persisting.video_download_tracking.update_video_download_tracking_usecase import (
    UpdateVideoDownloadTrackingUseCase,
)


def test_happy_path() -> None:
    update_status = UpdateVideoDownloadTrackingUseCase(
        download_tracking_repository=DummyDownloadingTrackerInterface(
            insert_or_update_entry_return_value=None
        )
    ).execute(
        video_url=generate_random_url(),
        video_resolution=144,
        video_title=generate_random_string_without_digits(),
        destination_path=mkdtemp(),
        downloading_status=DownloadingStatus.FINISHED,
    )

    assert update_status is None


def test_invalid_destination_path_path() -> None:
    destination_path: str = "invalid"
    update_status = UpdateVideoDownloadTrackingUseCase(
        download_tracking_repository=DummyDownloadingTrackerInterface(
            insert_or_update_entry_return_value=None
        )
    ).execute(
        video_url=generate_random_url(),
        video_resolution=144,
        video_title=generate_random_string_without_digits(),
        destination_path=destination_path,
        downloading_status=DownloadingStatus.FINISHED,
    )

    assert isinstance(update_status, UseCaseExecutionError)
    assert isinstance(update_status.invalid_entity, VideoTrackingRepositoryUpdateError)
    assert (
        update_status.invalid_entity.error_msg
        == f"This destination path [{destination_path}] doesn't exist !"
    )
