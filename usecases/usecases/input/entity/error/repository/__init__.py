from dataclasses import dataclass

from domain.entity.error.shared.generic_error import GenericError
from domain.entity.video.youtube import ToBeDownloadedYouTubeVideo


@dataclass(frozen=True, slots=True, kw_only=True)
class VideoTrackingRepositoryUpdateError(GenericError[ToBeDownloadedYouTubeVideo]):
    pass
