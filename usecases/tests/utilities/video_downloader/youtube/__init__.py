from typing import Any, Callable

from domain.entity.error.video.youtube import YouTubeVideoDownloadError
from domain.entity.video.download_status import OnCompletionStatus, OnProgressStatus
from domain.entity.video.youtube import DownloadedYouTubeVideo

from usecases.input.interface.video_downloader.youtube import (
    YouTubeVideoDownloaderInterface,
)


class DummyYouTubeDownloader(YouTubeVideoDownloaderInterface):
    def __init__(
        self,
        *,
        download_from_url_return_value: (
            YouTubeVideoDownloadError | DownloadedYouTubeVideo
        )
    ) -> None:
        self.__download_from_url_return_value = download_from_url_return_value

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
        return self.__download_from_url_return_value
