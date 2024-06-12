from dataclasses import dataclass

from domain.entity.error.shared.generic_error import GenericError
from domain.entity.video.youtube import (
    ToBeDownloadedYouTubeVideo,
    ToBeDownloadedYouTubeVideos,
    ToBeMetadataFetchedYouTubeVideo,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class YouTubeVideoDownloadError(GenericError[ToBeDownloadedYouTubeVideo]):
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class YouTubeVideosDownloadError(GenericError[ToBeDownloadedYouTubeVideos]):
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class YouTubeVideoMetadataFetchingError(GenericError[ToBeMetadataFetchedYouTubeVideo]):
    pass
