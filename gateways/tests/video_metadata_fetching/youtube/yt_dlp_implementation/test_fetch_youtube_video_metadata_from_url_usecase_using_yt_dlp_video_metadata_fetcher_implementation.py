from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import (
    ToBeMetadataFetchedYouTubeVideo,
    YouTubeVideoMetadata,
)
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_metadata_fetching.youtube.from_url_usecase import (
    FetchYouTubeVideoMetadataFromUrlUseCase,
)

from gateways.implementations.video_metadata_fetcher.youtube.yt_dlp import (
    YtDlpYouTubeVideoMetadataFetcher,
)
from tests.utilities.constants import (
    valid_downloaded_youtube_video,
    valid_video_metadata,
)


def test_happy_path() -> None:
    video_url = valid_downloaded_youtube_video.video_url
    youtube_video_metadata = valid_video_metadata
    fetching_video_metadata_status = FetchYouTubeVideoMetadataFromUrlUseCase(
        youtube_metadata_fetcher=YtDlpYouTubeVideoMetadataFetcher()
    ).execute(video_url=video_url)

    assert isinstance(fetching_video_metadata_status, YouTubeVideoMetadata)
    assert fetching_video_metadata_status == youtube_video_metadata


def test_invalid_url_path() -> None:
    to_be_metadata_fetched = ToBeMetadataFetchedYouTubeVideo(video_url="invalid")
    fetching_metadata_error = YouTubeVideoMetadataFetchingError(
        error_msg=f"This url [{to_be_metadata_fetched.video_url}] doesn't exist !",
        invalid_entity=to_be_metadata_fetched,
    )
    fetching_video_metadata_status = FetchYouTubeVideoMetadataFromUrlUseCase(
        youtube_metadata_fetcher=YtDlpYouTubeVideoMetadataFetcher()
    ).execute(video_url=to_be_metadata_fetched.video_url)

    assert isinstance(fetching_video_metadata_status, UseCaseExecutionError)
    assert isinstance(
        fetching_video_metadata_status.invalid_entity, YouTubeVideoMetadataFetchingError
    )
    assert fetching_video_metadata_status.invalid_entity == fetching_metadata_error
