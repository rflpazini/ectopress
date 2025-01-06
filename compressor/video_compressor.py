import logging
import subprocess
from datetime import datetime
from compressor.utils import (
    check_file_exists,
    create_output_dir,
    make_dimensions_even,
    get_creation_date_with_ffprobe,
    set_file_timestamps,
)

logging.getLogger("moviepy").setLevel(logging.ERROR)


def compress_video(input_path, output_path, target_resolution=(1280, 720), target_bitrate="2M"):
    """
    Compress an MP4 video to a lower size while keeping high quality,
    ensuring valid dimensions, and preserving original creation date.

    :param input_path: Path to the input MP4 video file.
    :param output_path: Path to the output compressed video file.
    :param target_resolution: Desired resolution for the output video (default: 1280x720).
    :param target_bitrate: Desired bitrate for the output video (default: 2 Mbps).
    """
    if not check_file_exists(input_path):
        print(f"❌ Input file does not exist: {input_path}")
        return

    try:
        # Get creation date from metadata
        creation_timestamp = get_creation_date_with_ffprobe(input_path)

        # Log the compression process
        print(f"🎥 Compressing {input_path}")

        # Ensure the output directory exists
        create_output_dir(output_path.rsplit("/", 1)[0])

        # Adjust resolution to maintain aspect ratio
        target_resolution = make_dimensions_even(*target_resolution)

        # Build FFmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", f"scale={target_resolution[0]}:{target_resolution[1]}",
            "-c:v", "libx264",
            "-preset", "slow",
            "-b:v", target_bitrate,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-metadata", f"creation_time={datetime.utcfromtimestamp(creation_timestamp).isoformat()}",
            "-y",  # Overwrite output file if exists
            "-loglevel", "error",  # Suppress logs except for errors
            output_path
        ]

        # Execute FFmpeg command
        subprocess.run(ffmpeg_command, check=True)

        # Update file timestamps to match the original
        set_file_timestamps(output_path, creation_timestamp)

        print(f"✅ Compression successful! Output saved at: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error compressing {input_path}: {e}")
    except Exception as e:
        print(f"❌ Error compressing {input_path}: {e}")
