#!/bin/env python

from argparse import ArgumentParser, Namespace

from domain.entity.error.video.youtube import (
    YouTubeVideoDownloadError,
    YouTubeVideosDownloadError,
)
from domain.entity.video.download_status import DownloadingStatus
from domain.entity.video.youtube import DownloadedYouTubeVideo
from gateways.implementations.repository.video_download_tracker.peewee_implementation import (
    PeeweeDownloadingTracker,
)
from gateways.implementations.video_downloader.youtube.yt_dlp import (
    YtDlpYouTubeDownloader,
)
from usecases.input.entity.error.generic_usecase import UseCaseExecutionError
from usecases.output.video_downloading.youtube.from_urls_file_usecase import (
    DownloadYouTubeVideoFromUrlsFileUseCase,
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
    parser = ArgumentParser("Download YouTube Video From An URLS File")
    parser.add_argument(
        "-uf",
        "--urls-file",
        help="The urls file of the video(s) that needs to be downloaded",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-r",
        "--res",
        help="The video(s) resolution that needs to be downloaded",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--dst",
        help="The destination where the video(s) will be downloaded into",
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
    parser.add_argument(
        "-pd",
        "--parallel_downloads",
        help="The number of parallel downloads",
        type=int,
        required=False,
    )

    return parser.parse_args()


def download(
    *,
    urls_file_path: str,
    videos_resolution: int,
    destination_path: str,
    download_timeout: int,
    download_retries: int,
    parallel_downloads: int,
) -> tuple[
    list[UseCaseExecutionError[YouTubeVideosDownloadError]]
    | list[UseCaseExecutionError[YouTubeVideoDownloadError]],
    list[DownloadedYouTubeVideo],
]:
    youtube_downloader = YtDlpYouTubeDownloader()
    return DownloadYouTubeVideoFromUrlsFileUseCase(
        youtube_video_downloader=youtube_downloader
    ).execute(
        urls_file_path=urls_file_path,
        videos_resolution=videos_resolution,
        destination_path=destination_path,
        download_timeout=download_timeout,
        download_retries=download_retries,
        parallel_downloads=parallel_downloads,
        on_progress_callback=lambda on_progress: print_in_green(
            f"Downloaded [{on_progress.download_ratio}] of [{on_progress.video_title[:29]} ...] "
            + f"at [{on_progress.download_speed}] and ETA of [{on_progress.download_eta}] "
            + f"in [{on_progress.video_resolution}]"
        ),
        on_complete_callback=lambda on_completion: print_in_green(
            f"Completed Downloading [{on_completion.video_title}] and saved at [{on_completion.downloaded_file_path}]"
        ),
    )


def main() -> None:
    args: Namespace = parse_args()
    urls_file, resolution, dst, timeout, retries, parallel_downloads = (
        args.urls_file.strip(),
        args.res,
        args.dst.strip(),
        args.download_timeout,
        args.download_retries,
        args.parallel_downloads,
    )

    download_errors, download_successes = download(
        urls_file_path=urls_file,
        videos_resolution=resolution,
        destination_path=dst,
        download_timeout=timeout,
        download_retries=retries,
        parallel_downloads=parallel_downloads,
    )

    print()

    if len(download_errors) > 0:
        print_in_red("Downloading Errors ⬎")
        for error in download_errors:
            if isinstance(error.invalid_entity, YouTubeVideoDownloadError):
                UpdateVideoDownloadTrackingUseCase(
                    download_tracking_repository=PeeweeDownloadingTracker(
                        database_destination_path=dst
                    )
                ).execute(
                    video_url=error.invalid_entity.invalid_entity.video_url,
                    video_resolution=resolution,
                    video_title="NA",
                    destination_path=dst,
                    downloading_status=DownloadingStatus.STARTED,
                )

            print_in_red(
                f"\tError downloading video ➙ [{error.invalid_entity.invalid_entity}] "
                + f"for the reason ➙ [{error.invalid_entity.error_msg}] ..."
            )

        print()

    if len(download_successes) > 0:
        print_in_cyan("Downloading Successes ⬎")
        for success in download_successes:
            UpdateVideoDownloadTrackingUseCase(
                download_tracking_repository=PeeweeDownloadingTracker(
                    database_destination_path=dst
                )
            ).execute(
                video_url=success.video_url,
                video_resolution=success.resolution,
                video_title=success.video_title,
                destination_path=dst,
                downloading_status=DownloadingStatus.FINISHED,
            )

            print_in_cyan(
                f"\tSuccessfully downloaded video ➙ [{success.video_title}] ..."
            )

        print()


if __name__ == "__main__":
    main()
