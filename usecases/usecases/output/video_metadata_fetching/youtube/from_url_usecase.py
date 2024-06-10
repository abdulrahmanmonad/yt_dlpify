from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import YouTubeVideoMetadata

from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.input.interface.shared.generic_usecase import GenericUseCaseInterface
from usecases.input.interface.video_metadata_fetcher.youtube import (
    YouTubeVideoMetadataFetcherInterface,
)


class FetchYouTubeVideoMetadataFromUrlUseCase(GenericUseCaseInterface):
    def __init__(
        self, *, youtube_metadata_fetcher: YouTubeVideoMetadataFetcherInterface
    ) -> None:
        self.__youtube_metadata_fetcher = youtube_metadata_fetcher

    def execute(
        self, *, video_url: str
    ) -> (
        UseCaseExecutionError[YouTubeVideoMetadataFetchingError] | YouTubeVideoMetadata
    ):
        metadata_fetching_status: (
            YouTubeVideoMetadataFetchingError | YouTubeVideoMetadata
        ) = self.__youtube_metadata_fetcher.fetch_metadata_from_url(video_url=video_url)

        if isinstance(metadata_fetching_status, YouTubeVideoMetadataFetchingError):
            return UseCaseExecutionError(invalid_entity=metadata_fetching_status)
        return metadata_fetching_status
