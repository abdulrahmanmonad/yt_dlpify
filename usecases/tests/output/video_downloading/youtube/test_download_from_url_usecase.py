from tempfile import mkdtemp

from domain.entity.error.video.youtube import (
    ToBeDownloadedYouTubeVideo,
    YouTubeVideoDownloadError,
)
from domain.entity.video.youtube import DownloadedYouTubeVideo

from tests.utilities.shared.functions import (
    generate_random_string_with_digits,
    generate_random_string_without_digits,
    generate_random_url,
)
from tests.utilities.video_downloader.youtube import DummyYouTubeDownloader
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_downloading.youtube.from_url_usecase import (
    DownloadYouTubeVideoFromUrlUseCase,
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
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=DummyYouTubeDownloader(
            download_from_url_return_value=downloaded_youtube_video
        )
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


def test_invalid_destination_path_path() -> None:
    destination_path: str = "invalid"
    to_be_downloaded_video = ToBeDownloadedYouTubeVideo(
        video_url=generate_random_url(),
        resolution=144,
        destination_path=destination_path,
    )
    download_error = YouTubeVideoDownloadError(
        error_msg=f"This destination path [{destination_path}] doesn't exist !",
        invalid_entity=to_be_downloaded_video,
    )
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=DummyYouTubeDownloader(
            download_from_url_return_value=download_error
        )
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
        video_url=generate_random_url(),
        resolution=144,
        destination_path=destination_path,
    )
    download_error = YouTubeVideoDownloadError(
        error_msg=f"This url [{to_be_downloaded_video.video_url}] doesn't exist !",
        invalid_entity=to_be_downloaded_video,
    )
    download_status = DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=DummyYouTubeDownloader(
            download_from_url_return_value=download_error
        )
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
