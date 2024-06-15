#!/bin/env python

from argparse import ArgumentParser, Namespace

from domain.entity.error.video.youtube import YouTubeVideoDownloadError
from domain.entity.video.download_status import DownloadingStatus, OnCompletionStatus
from domain.entity.video.youtube import DownloadedYouTubeVideo
from gateways.implementations.repository.video_download_tracker.peewee_implementation import (
    PeeweeDownloadingTracker,
)
from gateways.implementations.video_downloader.youtube.yt_dlp import (
    YtDlpYouTubeDownloader,
)
from gateways.implementations.video_metadata_fetcher.youtube.yt_dlp import (
    YtDlpYouTubeVideoMetadataFetcher,
)
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_downloading.youtube.from_url_usecase import (
    DownloadYouTubeVideoFromUrlUseCase,
)
from usecases.output.video_metadata_fetching.youtube.from_url_usecase import (
    FetchYouTubeVideoMetadataFromUrlUseCase,
)
from usecases.output.video_persisting.video_download_tracking.update_video_download_tracking_usecase import (
    UpdateVideoDownloadTrackingUseCase,
)

from external_systems.utilities.functions import (
    print_in_cyan,
    print_in_green,
    print_in_red,
)


def parse_args() -> Namespace:
    parser = ArgumentParser("Download YouTube Video From An Url")
    parser.add_argument(
        "-u",
        "--url",
        help="The url of the video that needs to be downloaded",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-r",
        "--res",
        help="The video resolution that needs to be downloaded",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--dst",
        help="The destination where the video will be downloaded into",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-dt",
        "--download_timeout",
        help="The number of seconds to tomeout if there is an error while downloading",
        type=int,
        required=False,
    )
    parser.add_argument(
        "-dr",
        "--download_retries",
        help="The number of attempts to download if there is an error",
        type=int,
        required=False,
    )

    return parser.parse_args()


def download(
    *,
    video_url: str,
    video_resolution: int,
    video_title: str,
    destination_path: str,
    download_timeout: int,
    download_retries: int,
) -> UseCaseExecutionError[YouTubeVideoDownloadError] | DownloadedYouTubeVideo:
    UpdateVideoDownloadTrackingUseCase(
        download_tracking_repository=PeeweeDownloadingTracker(
            database_destination_path=destination_path
        )
    ).execute(
        video_url=video_url,
        video_resolution=video_resolution,
        video_title=video_title,
        destination_path=destination_path,
        downloading_status=DownloadingStatus.STARTED,
    )

    def __on_complete(on_completion: OnCompletionStatus) -> None:
        UpdateVideoDownloadTrackingUseCase(
            download_tracking_repository=PeeweeDownloadingTracker(
                database_destination_path=destination_path
            )
        ).execute(
            video_url=video_url,
            video_resolution=video_resolution,
            video_title=video_title,
            destination_path=destination_path,
            downloading_status=DownloadingStatus.FINISHED,
        )
        print_in_green(
            f"Completed Downloading [{on_completion.video_title}] and saved at [{on_completion.downloaded_file_path}]"
        )

    youtube_downloader = YtDlpYouTubeDownloader()
    return DownloadYouTubeVideoFromUrlUseCase(
        youtube_video_downloader=youtube_downloader
    ).execute(
        video_url=video_url,
        video_resolution=video_resolution,
        destination_path=destination_path,
        download_timeout=download_timeout,
        download_retries=download_retries,
        on_progress_callback=lambda on_progress: print_in_green(
            f"Downloaded [{on_progress.download_ratio}] of [{on_progress.video_title[:29]} ...] "
            + f"at [{on_progress.download_speed}] and ETA of [{on_progress.download_eta}] "
            + f"in [{on_progress.video_resolution}]"
        ),
        on_complete_callback=__on_complete,
    )


def main() -> None:
    args: Namespace = parse_args()
    url, resolution, dst, timeout, retries = (
        args.url,
        args.res,
        args.dst.strip(),
        args.download_timeout,
        args.download_retries,
    )

    metadata_fetch_status = FetchYouTubeVideoMetadataFromUrlUseCase(
        youtube_metadata_fetcher=YtDlpYouTubeVideoMetadataFetcher()
    ).execute(video_url=url)

    if isinstance(metadata_fetch_status, UseCaseExecutionError):
        print_in_red(
            f"Error downloading video ➙ [{url}] "
            + f"for the reason ➙ [{metadata_fetch_status.invalid_entity.error_msg}] ..."
        )
        exit(1)

    download_result: (
        UseCaseExecutionError[YouTubeVideoDownloadError] | DownloadedYouTubeVideo
    ) = download(
        video_url=url,
        video_resolution=resolution,
        video_title=metadata_fetch_status.video_title,
        destination_path=dst,
        download_timeout=timeout,
        download_retries=retries,
    )

    print()

    if isinstance(download_result, UseCaseExecutionError):
        print_in_red(
            f"Error downloading video ➙ [{download_result.invalid_entity.invalid_entity.video_url}] "
            + f"for the reason ➙ [{download_result.invalid_entity.error_msg}] ..."
        )
    else:
        print_in_cyan(
            f"Successfully downloaded video ➙ [{download_result.video_title}] ..."
        )


if __name__ == "__main__":
    main()
