from domain.entity.video.download_status import DownloadingStatus

from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError
from usecases.input.interface.repository.downloading_tracker import (
    DownloadingTrackerInterface,
)


class DummyDownloadingTrackerInterface(DownloadingTrackerInterface):
    def __init__(
        self,
        *,
        insert_or_update_entry_return_value: VideoTrackingRepositoryUpdateError | None
    ) -> None:
        self.__insert_or_update_entry_return_value = insert_or_update_entry_return_value

    def insert_or_update_entry(
        self,
        *,
        video_url: str,
        video_resolution: int,
        destination_path: str,
        downloading_status: DownloadingStatus
    ) -> VideoTrackingRepositoryUpdateError | None:
        return self.__insert_or_update_entry_return_value
