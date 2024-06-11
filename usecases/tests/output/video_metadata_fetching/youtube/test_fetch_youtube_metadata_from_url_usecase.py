from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import (
    ToBeMetadataFetchedYouTubeVideo,
    YouTubeVideoMetadata,
)

from tests.utilities.shared.functions import (
    generate_random_string_without_digits,
    generate_random_url,
)
from tests.utilities.video_metadata_fetcher.youtube import DummyYouTubeMetadataFetcher
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_metadata_fetching.youtube.from_url_usecase import (
    FetchYouTubeVideoMetadataFromUrlUseCase,
)


def test_happy_path() -> None:
    video_url = generate_random_url()
    youtube_video_metadata = YouTubeVideoMetadata(
        video_formats=[],
        video_thumbnail_url=generate_random_url(),
        video_title=generate_random_string_without_digits(),
        video_url=video_url,
    )
    fetching_video_metadata_status = FetchYouTubeVideoMetadataFromUrlUseCase(
        youtube_metadata_fetcher=DummyYouTubeMetadataFetcher(
            fetch_metadata_from_url_return_value=youtube_video_metadata
        )
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
        youtube_metadata_fetcher=DummyYouTubeMetadataFetcher(
            fetch_metadata_from_url_return_value=fetching_metadata_error
        )
    ).execute(video_url=to_be_metadata_fetched.video_url)

    assert isinstance(fetching_video_metadata_status, UseCaseExecutionError)
    assert isinstance(
        fetching_video_metadata_status.invalid_entity, YouTubeVideoMetadataFetchingError
    )
    assert fetching_video_metadata_status.invalid_entity == fetching_metadata_error
