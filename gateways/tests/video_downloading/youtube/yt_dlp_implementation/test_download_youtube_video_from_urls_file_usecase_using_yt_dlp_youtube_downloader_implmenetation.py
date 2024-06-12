from os import path
from tempfile import mkdtemp, mkstemp

from usecases.output.video_downloading.youtube.from_urls_file_usecase import (
    DownloadYouTubeVideoFromUrlsFileUseCase,
)

from gateways.implementations.video_downloader.youtube.yt_dlp import (
    YtDlpYouTubeDownloader,
)
from tests.utilities.constants import valid_downloaded_youtube_video


def test_happy_path() -> None:
    downloaded_youtube_video = valid_downloaded_youtube_video
    destination_path: str = mkdtemp()
    _file_descriptor, urls_file_path = mkstemp(dir=destination_path)
    with open(urls_file_path, "w") as urls_file:
        urls_file.write(downloaded_youtube_video.video_url + "\n")

    download_errors, download_successes = DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        urls_file_path=urls_file_path,
        videos_resolution=downloaded_youtube_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert len(download_errors) == 0
    assert len(download_successes) == 1
    assert download_successes[0] == downloaded_youtube_video
    assert path.exists(
        path.join(destination_path, download_successes[0].video_title) + ".mkv"
    )


def test_invalid_destination_path_path() -> None:
    downloaded_youtube_video = valid_downloaded_youtube_video
    destination_path: str = "invalid"
    _file_descriptor, urls_file_path = mkstemp()
    with open(urls_file_path, "w") as urls_file:
        urls_file.write(downloaded_youtube_video.video_url + "\n")

    download_errors, download_successes = DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        urls_file_path=urls_file_path,
        videos_resolution=downloaded_youtube_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert len(download_errors) == 1
    assert len(download_successes) == 0
    assert (
        download_errors[0].invalid_entity.error_msg
        == f"This destination path [{destination_path}] doesn't exist !"
    )


def test_invalid_urls_file_path_path() -> None:
    downloaded_youtube_video = valid_downloaded_youtube_video
    destination_path: str = mkdtemp()
    urls_file_path = "invalid"

    download_errors, download_successes = DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=YtDlpYouTubeDownloader()
    ).execute(
        urls_file_path=urls_file_path,
        videos_resolution=downloaded_youtube_video.resolution,
        destination_path=destination_path,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Finished ..."),
    )

    assert len(download_errors) == 1
    assert len(download_successes) == 0
    assert (
        download_errors[0].invalid_entity.error_msg
        == f"This urls file path [{urls_file_path}] doesn't exist !"
    )
