from domain.entity.error.video.youtube import YouTubeVideoMetadataFetchingError
from domain.entity.video.youtube import (
    ToBeMetadataFetchedYouTubeVideo,
    YouTubeVideoFormat,
    YouTubeVideoMetadata,
)
from usecases.input.interface.video_metadata_fetcher.youtube import (
    YouTubeVideoMetadataFetcherInterface,
)
from yt_dlp import YoutubeDL


class YtDlpYouTubeVideoMetadataFetcher(YouTubeVideoMetadataFetcherInterface):
    def __init__(self) -> None:
        pass

    def fetch_metadata_from_url(
        self, *, video_url: str
    ) -> YouTubeVideoMetadataFetchingError | YouTubeVideoMetadata:
        with YoutubeDL() as yt:
            try:
                to_be_metadata_fetched_video = ToBeMetadataFetchedYouTubeVideo(
                    video_url=video_url
                )
                youtube_video_info = yt.extract_info(
                    url=to_be_metadata_fetched_video.video_url, download=False
                )
                assert youtube_video_info is not None

                formats: list[YouTubeVideoFormat] = []
                for format in youtube_video_info.get("formats", []):
                    if "(" not in format.get("format"):
                        formats.append(
                            YouTubeVideoFormat(
                                video_format_id=str(format.get("format_id", "NA")),
                                video_bit_rate=str(format.get("vbr", "NA")),
                                video_fps=str(format.get("fps", "NA")),
                                video_height=str(format.get("height", "NA")),
                                video_width=str(format.get("width", "NA")),
                            )
                        )

                return YouTubeVideoMetadata(
                    video_url=to_be_metadata_fetched_video.video_url,
                    video_title=youtube_video_info.get("title", "NA"),
                    video_thumbnail_url=youtube_video_info.get("thumbnail", "NA"),
                    video_formats=formats,
                )
            except Exception as ex:
                if "Failed to extract any player response" in str(ex):
                    return YouTubeVideoMetadataFetchingError(
                        error_msg="There is no internet connectivity !",
                        invalid_entity=to_be_metadata_fetched_video,
                    )
                elif "is not a valid URL" in str(ex):
                    return YouTubeVideoMetadataFetchingError(
                        error_msg=f"This url [{video_url}] doesn't exist !",
                        invalid_entity=to_be_metadata_fetched_video,
                    )

                return YouTubeVideoMetadataFetchingError(
                    error_msg=str(ex), invalid_entity=to_be_metadata_fetched_video
                )
