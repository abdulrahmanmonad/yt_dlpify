from abc import ABCMeta, abstractmethod

from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import YouTubeVideoMetadata


class YouTubeVideoMetadataFetcherInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("This suppose to be an abstract function !")

    @abstractmethod
    def fetch_metadata_from_url(
        self, *, video_url: str
    ) -> YouTubeVideoMetadataFetchingError | YouTubeVideoMetadata:
        raise NotImplementedError("This suppose to be an abstract function !")
