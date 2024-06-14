from dataclasses import dataclass
from enum import Enum


class DownloadingStatus(Enum):
    STARTED = "STARTED"
    FINISHED = "FINISHED"


@dataclass(frozen=True, slots=True, kw_only=True)
class OnProgressStatus:
    video_title: str
    video_resolution: str
    video_size: str
    download_ratio: str
    download_eta: str
    download_speed: str


@dataclass(frozen=True, slots=True, kw_only=True)
class OnCompletionStatus:
    video_title: str
    downloaded_file_path: str
