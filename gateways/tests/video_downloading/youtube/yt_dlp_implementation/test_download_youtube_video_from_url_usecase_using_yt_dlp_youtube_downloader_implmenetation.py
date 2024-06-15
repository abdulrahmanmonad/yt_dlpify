from os import path
from tempfile import mkdtemp

from domain.entity.error.video.youtube import (
    ToBeDownloadedYouTubeVideo,
    YouTubeVideoDownloadError,
)
from domain.entity.video.youtube import DownloadedYouTubeVideo
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_downloading.youtube.from_url_usecase import (
    DownloadYouTubeVideoFromUrlUseCase,
)

from gateways.implementations.video_downloader.youtube.yt_dlp import (
    YtDlpYouTubeDownloader,
)
from tests.utilities.constants import valid_downloaded_youtube_video


def test_happy_path() -> None:
    downloaded_youtube_video = valid_downloaded_youtube_video
    destination_path: str = mkdtemp()
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        video_url=downloaded_youtube_video.video_url,
        video_resolution=downloaded_youtube_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert isinstance(download_status, DownloadedYouTubeVideo)

    assert download_status.video_url == downloaded_youtube_video.video_url
    assert download_status.video_title == downloaded_youtube_video.video_title
    assert download_status.resolution == downloaded_youtube_video.resolution
    assert download_status.channel_id == downloaded_youtube_video.channel_id
    assert download_status.channel_title == downloaded_youtube_video.channel_title
    assert download_status.channel_url == downloaded_youtube_video.channel_url
    assert path.exists(
        path.join(destination_path, download_status.video_title) + ".mkv"
    )


def test_invalid_destination_path_path() -> None:
    destination_path: str = "invalid"
    to_be_downloaded_video = ToBeDownloadedYouTubeVideo(
        video_url=valid_downloaded_youtube_video.video_url,
        resolution=144,
        destination_path=destination_path,
    )
    download_error = YouTubeVideoDownloadError(
        error_msg=f"This destination path [{destination_path}] doesn't exist !",
        invalid_entity=to_be_downloaded_video,
    )
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        video_url=to_be_downloaded_video.video_url,
        video_resolution=to_be_downloaded_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert isinstance(download_status, UseCaseExecutionError)
    assert isinstance(download_status.invalid_entity, YouTubeVideoDownloadError)
    assert download_status.invalid_entity == download_error


def test_invalid_video_resolution_path() -> None:
    destination_path: str = mkdtemp()
    resolution = 100
    to_be_downloaded_video = ToBeDownloadedYouTubeVideo(
        video_url=valid_downloaded_youtube_video.video_url,
        resolution=100,
        destination_path=destination_path,
    )
    download_error = YouTubeVideoDownloadError(
        error_msg=f"This video resolution [{resolution}] is not available for this video !",
        invalid_entity=to_be_downloaded_video,
    )
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        video_url=to_be_downloaded_video.video_url,
        video_resolution=to_be_downloaded_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert isinstance(download_status, UseCaseExecutionError)
    assert isinstance(download_status.invalid_entity, YouTubeVideoDownloadError)
    assert download_status.invalid_entity == download_error


def test_invalid_download_path() -> None:
    destination_path: str = mkdtemp()
    to_be_downloaded_video = ToBeDownloadedYouTubeVideo(
        video_url="invalid_url", resolution=144, destination_path=destination_path
    )
    download_error = YouTubeVideoDownloadError(
        error_msg=f"This url [{to_be_downloaded_video.video_url}] doesn't exist !",
        invalid_entity=to_be_downloaded_video,
    )
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        video_url=to_be_downloaded_video.video_url,
        video_resolution=to_be_downloaded_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert isinstance(download_status, UseCaseExecutionError)
    assert isinstance(download_status.invalid_entity, YouTubeVideoDownloadError)
    assert download_status.invalid_entity == download_error
