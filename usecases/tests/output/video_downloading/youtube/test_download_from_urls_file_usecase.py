from tempfile import mkdtemp, mkstemp

from domain.entity.video.youtube import DownloadedYouTubeVideo

from tests.utilities.shared.functions import (
    generate_random_string_with_digits,
    generate_random_string_without_digits,
    generate_random_url,
)
from tests.utilities.video_downloader.youtube import DummyYouTubeDownloader
from usecases.output.video_downloading.youtube.from_urls_file_usecase import (
    DownloadYouTubeVideoFromUrlsFileUseCase,
)


def test_happy_path() -> None:
    downloaded_youtube_video = DownloadedYouTubeVideo(
        video_title=generate_random_string_without_digits(),
        channel_id=generate_random_string_with_digits(),
        channel_title=generate_random_string_without_digits(),
        channel_url=generate_random_url(),
        video_url=generate_random_url(),
        resolution=144,
    )
    destination_path: str = mkdtemp()
    _file_descriptor, urls_file_path = mkstemp(dir=destination_path)
    with open(urls_file_path, "w") as urls_file:
        urls_file.write(generate_random_url() + "\n")

    download_errors, download_successes = DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=DummyYouTubeDownloader(
            download_from_url_return_value=downloaded_youtube_video
        )
    ).execute(
        urls_file_path=urls_file_path,
        destination_path=destination_path,
        videos_resolution=144,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Completed ..."),
    )

    assert len(download_errors) == 0
    assert len(download_successes) == 1
    assert download_successes[0] == downloaded_youtube_video


def test_invalid_urls_file_path_path() -> None:
    downloaded_youtube_video = DownloadedYouTubeVideo(
        video_title=generate_random_string_without_digits(),
        channel_id=generate_random_string_with_digits(),
        channel_title=generate_random_string_without_digits(),
        channel_url=generate_random_url(),
        video_url=generate_random_url(),
        resolution=144,
    )
    destination_path: str = mkdtemp()
    urls_file_path = "invalid"

    download_errors, download_successes = DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=DummyYouTubeDownloader(
            download_from_url_return_value=downloaded_youtube_video
        )
    ).execute(
        urls_file_path=urls_file_path,
        destination_path=destination_path,
        videos_resolution=144,
        on_progress_callback=lambda on_progress: print("Downloading ..."),
        on_complete_callback=lambda on_completion: print("Completed ..."),
    )

    assert len(download_errors) == 1
    assert len(download_successes) == 0
    assert (
        download_errors[0].invalid_entity.error_msg
        == f"This urls file path [{urls_file_path}] doesn't exist !"
    )
