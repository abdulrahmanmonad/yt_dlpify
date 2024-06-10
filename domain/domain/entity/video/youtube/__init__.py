from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class ToBeDownloadedYouTubeVideo:
    video_url: str
    resolution: int


@dataclass(frozen=True, slots=True, kw_only=True)
class ToBeMetadataFetchedYouTubeVideo:
    video_url: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DownloadedYouTubeVideo:
    video_title: str
    video_url: str
    channel_title: str
    channel_id: str
    channel_url: str
    resolution: int


@dataclass(frozen=True, slots=True, kw_only=True)
class YouTubeVideoFormat:
    video_bit_rate: str
    video_width: str
    video_height: str
    video_fps: str
    video_format_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class YouTubeVideoMetadata:
    video_title: str
    video_url: str
    video_formats: list[YouTubeVideoFormat]
    video_thumbnail_url: str
