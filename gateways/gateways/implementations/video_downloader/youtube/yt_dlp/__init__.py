from os import path
from typing import Any, Callable

from domain.entity.error.video.youtube import YouTubeVideoDownloadError
from domain.entity.video.download_status import (OnCompletionStatus,
                                                 OnProgressStatus)
from domain.entity.video.youtube import (DownloadedYouTubeVideo,
                                         ToBeDownloadedYouTubeVideo)
from usecases.input.interface.video_downloader.youtube import \
    YouTubeVideoDownloaderInterface
from yt_dlp import YoutubeDL


class YtDlpYouTubeDownloader(YouTubeVideoDownloaderInterface):
    def __init__(self) -> None:
        pass

    def download_from_url(
        self,
        *,
        video_url: str,
        video_resolution: int = 1080,
        destination_path: str,
        download_retries: int = 3,
        download_timeout: int = 9,
        on_progress_callback: Callable[[OnProgressStatus], Any],
        on_complete_callback: Callable[[OnCompletionStatus], Any],
    ) -> YouTubeVideoDownloadError | DownloadedYouTubeVideo:
        to_be_downloaded_youtube_video = ToBeDownloadedYouTubeVideo(
            video_url=video_url, resolution=video_resolution
        )
        
        def __on_progress_hook(status_obj) -> None:
            if status_obj["status"] == "downloading":
                video_size_bytes = status_obj.get(
                    "total_bytes", status_obj.get("total_bytes_estimate", "NA")
                )
                downloaded_bytes = status_obj.get("downloaded_bytes", "1")
                on_progress_callback(
                    OnProgressStatus(
                        video_title=path.basename(status_obj.get("filename", "NA")),
                        video_size=video_size_bytes,
                        video_resolution=f"{video_resolution}P",
                        download_speed=f"{(status_obj.get("speed", 1)) / 1000000:.2f} Mb",
                        download_eta=f"{status_obj.get("eta", 0):.2f} seconds",
                        download_ratio=f"{(downloaded_bytes / video_size_bytes) * 100:.2f} %",
                    )
                )
            elif status_obj["status"] == "finished":
                on_complete_callback(
                    OnCompletionStatus(
                        video_title=path.basename(status_obj.get("filename", "NA")),
                        downloaded_file_path=status_obj.get("filename", "NA"),
                    )
                )

        yt_options: dict[str, Any] = dict(
            format=f"bv*[height<={video_resolution}]+ba",
            socket_timeout=download_timeout,
            extractor_retries=download_retries,
            progress_hooks=[__on_progress_hook],
            postprocessor_hooks=[],
            paths=dict(home=destination_path),
            outtmpl="%(title)s.%(ext)s",
            merge_output_format="mkv",
            noprogress=True,
            consoletitle=True,
        )
        with YoutubeDL(yt_options) as yt:
            try:
                youtube_video_info = yt.extract_info(url=video_url, download=True)
                assert youtube_video_info is not None
                return DownloadedYouTubeVideo(
                    video_title=youtube_video_info.get("title", "NA"),
                    video_url=video_url,
                    channel_id=youtube_video_info.get("channel_id", "NA"),
                    channel_title=youtube_video_info.get("channel", 'NA'),
                    channel_url=youtube_video_info.get("channel_url", 'NA'),
                    resolution=video_resolution,
                )
            except Exception as ex:
                if "Failed to extract any player response" in str(ex):
                    return YouTubeVideoDownloadError( 
                        error_msg="There is no internet connectivity !", 
                        invalid_entity=to_be_downloaded_youtube_video,
                    )
                elif "Video unavailable" in str(ex):
                    return YouTubeVideoDownloadError(
                        error_msg=f"This url [{video_url}] doesn't exist !",
                        invalid_entity=to_be_downloaded_youtube_video
                    )
                elif "Requested format is not available" in str(ex):
                    return YouTubeVideoDownloadError(
                        error_msg=f"This video resolution [{video_resolution}] is not available for this video !",
                        invalid_entity=to_be_downloaded_youtube_video
                    )
                
                return YouTubeVideoDownloadError(
                    error_msg=str(ex), invalid_entity=to_be_downloaded_youtube_video
                )
