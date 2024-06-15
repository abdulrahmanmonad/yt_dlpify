from multiprocessing.pool import ThreadPool
from os import path
from typing import Any, Callable

from domain.entity.error.video.youtube import (
    YouTubeVideoDownloadError,
    YouTubeVideosDownloadError,
)
from domain.entity.video.download_status import OnCompletionStatus, OnProgressStatus
from domain.entity.video.youtube import (
    DownloadedYouTubeVideo,
    ToBeDownloadedYouTubeVideos,
)

from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.input.interface.shared.generic_usecase import GenericUseCaseInterface
from usecases.input.interface.video_downloader.youtube import (
    YouTubeVideoDownloaderInterface,
)
from usecases.output.video_downloading.youtube.from_url_usecase import (
    DownloadYouTubeVideoFromUrlUseCase,
)


class DownloadYouTubeVideoFromUrlsFileUseCase(GenericUseCaseInterface):
    def __init__(
        self, *, youtube_video_downloader: YouTubeVideoDownloaderInterface
    ) -> None:
        self.__download_from_url_usecase = DownloadYouTubeVideoFromUrlUseCase(
            youtube_video_downloader=youtube_video_downloader
        )

    def execute(
        self,
        *,
        urls_file_path: str,
        videos_resolution: int = 1080,
        destination_path: str,
        download_retries: int = 3,
        download_timeout: int = 9,
        on_progress_callback: Callable[[OnProgressStatus], Any],
        on_complete_callback: Callable[[OnCompletionStatus], Any],
        parallel_downloads: int = 3,
    ) -> tuple[
        list[UseCaseExecutionError[YouTubeVideosDownloadError]]
        | list[UseCaseExecutionError[YouTubeVideoDownloadError]],
        list[DownloadedYouTubeVideo],
    ]:
        if not path.exists(urls_file_path):
            return [
                UseCaseExecutionError(
                    invalid_entity=YouTubeVideosDownloadError(
                        error_msg=f"This urls file path [{urls_file_path}] doesn't exist !",
                        invalid_entity=ToBeDownloadedYouTubeVideos(
                            urls_file_path=urls_file_path,
                            videos_resolution=videos_resolution,
                            destination_path=destination_path,
                        ),
                    ),
                )
            ], []

        with open(urls_file_path, "r") as urls_file:
            videos_urls: list[str] = list(
                filter(
                    lambda s: s != "", [url.strip() for url in urls_file.readlines()]
                )
            )

        def wrapper(
            video_url: str,
        ) -> UseCaseExecutionError[YouTubeVideoDownloadError] | DownloadedYouTubeVideo:
            return self.__download_from_url_usecase.execute(
                video_url=video_url,
                video_resolution=videos_resolution,
                destination_path=destination_path,
                download_timeout=download_timeout,
                download_retries=download_retries,
                on_progress_callback=on_progress_callback,
                on_complete_callback=on_complete_callback,
            )

        with ThreadPool(processes=parallel_downloads) as execution_pool:
            results: list[
                UseCaseExecutionError[YouTubeVideoDownloadError]
                | DownloadedYouTubeVideo
            ] = execution_pool.map_async(wrapper, videos_urls).get()

            download_errors: list[UseCaseExecutionError[YouTubeVideoDownloadError]] = [
                result
                for result in results
                if isinstance(result, UseCaseExecutionError)
            ]

            download_successes: list[DownloadedYouTubeVideo] = [
                result
                for result in results
                if isinstance(result, DownloadedYouTubeVideo)
            ]

            return download_errors, download_successes
