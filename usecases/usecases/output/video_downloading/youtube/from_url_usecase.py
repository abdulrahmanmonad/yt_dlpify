from os import path
from typing import Any, Callable

from domain.entity.error.video.youtube import (
    ToBeDownloadedYouTubeVideo,
    YouTubeVideoDownloadError,
)
from domain.entity.video.download_status import OnCompletionStatus, OnProgressStatus
from domain.entity.video.youtube import DownloadedYouTubeVideo

from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.input.interface.shared.generic_usecase import GenericUseCaseInterface
from usecases.input.interface.video_downloader.youtube import (
    YouTubeVideoDownloaderInterface,
)


class DownloadYouTubeVideoFromUrlUseCase(GenericUseCaseInterface):
    def __init__(
        self, *, youtube_video_downloader: YouTubeVideoDownloaderInterface
    ) -> None:
        self.__youtube_video_downloader = youtube_video_downloader

    def execute(
        self,
        *,
        video_url: str,
        video_resolution: int = 1080,
        destination_path: str,
        download_retries: int = 3,
        download_timeout: int = 9,
        on_progress_callback: Callable[[OnProgressStatus], Any],
        on_complete_callback: Callable[[OnCompletionStatus], Any],
    ) -> UseCaseExecutionError[YouTubeVideoDownloadError] | DownloadedYouTubeVideo:
        if not path.exists(destination_path):
            return UseCaseExecutionError(
                invalid_entity=YouTubeVideoDownloadError(
                    error_msg=f"This destination path [{destination_path}] doesn't exist !",
                    invalid_entity=ToBeDownloadedYouTubeVideo(
                        video_url=video_url, resolution=video_resolution
                    ),
                ),
            )

        download_status: YouTubeVideoDownloadError | DownloadedYouTubeVideo = (
            self.__youtube_video_downloader.download_from_url(
                video_url=video_url,
                video_resolution=video_resolution,
                destination_path=destination_path,
                download_retries=download_retries,
                download_timeout=download_timeout,
                on_progress_callback=on_progress_callback,
                on_complete_callback=on_complete_callback,
            )
        )

        if isinstance(download_status, YouTubeVideoDownloadError):
            return UseCaseExecutionError(invalid_entity=download_status)
        return download_status
