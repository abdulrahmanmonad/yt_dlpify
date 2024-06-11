from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from domain.entity.error.video.youtube import YouTubeVideoDownloadError
from domain.entity.video.download_status import OnCompletionStatus, OnProgressStatus
from domain.entity.video.youtube import DownloadedYouTubeVideo


class YouTubeVideoDownloaderInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("This suppose to be an abstract function !")

    @abstractmethod
    def download_from_url(
        self,
        *,
        video_url: str,
        video_resolution: int = 1080,
        destination_path: str,
        download_retries: int = 3,
        download_timeout: int = 9,
        on_progress_callback: Callable[[OnProgressStatus], Any],
        on_complete_callback: Callable[[OnCompletionStatus], Any]
    ) -> YouTubeVideoDownloadError | DownloadedYouTubeVideo:
        raise NotImplementedError("This suppose to be an abstract function !")
