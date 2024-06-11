from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import YouTubeVideoMetadata

from usecases.input.interface.video_metadata_fetcher.youtube import (
    YouTubeVideoMetadataFetcherInterface,
)


class DummyYouTubeMetadataFetcher(YouTubeVideoMetadataFetcherInterface):
    def __init__(
        self,
        *,
        fetch_metadata_from_url_return_value: (
            YouTubeVideoMetadataFetchingError | YouTubeVideoMetadata
        )
    ) -> None:
        self.__fetch_metadata_from_url_return_value = (
            fetch_metadata_from_url_return_value
        )

    def fetch_metadata_from_url(
        self, *, video_url: str
    ) -> YouTubeVideoMetadataFetchingError | YouTubeVideoMetadata:
        return self.__fetch_metadata_from_url_return_value
