from abc import ABCMeta, abstractmethod

from domain.entity.video.download_status import DownloadingStatus

from usecases.input.entity.error.repository import VideoTrackingRepositoryUpdateError


class DownloadingTrackerInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("This suppose to be an abstract function !")

    @abstractmethod
    def insert_or_update_entry(
        self,
        *,
        video_url: str,
        video_resolution: int,
        video_title: str,
        destination_path: str,
        downloading_status: DownloadingStatus
    ) -> VideoTrackingRepositoryUpdateError | None:
        raise NotImplementedError("This suppose to be an abstract function !")
