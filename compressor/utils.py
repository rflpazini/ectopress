import os
from datetime import datetime
import subprocess

def check_file_exists(filepath):
    """
    Utility function to check if a file exists.
    """
    return os.path.exists(filepath)

def create_output_dir(directory):
    """
    Create the output directory if it does not exist.
    """
    os.makedirs(directory, exist_ok=True)

def make_dimensions_even(width, height):
    """
    Adjust dimensions to ensure they are divisible by 2.
    """
    if width % 2 != 0:
        width -= 1
    if height % 2 != 0:
        height -= 1
    return width, height

def get_creation_date_with_ffprobe(file_path):
    """
    Extract the creation date from the input file's metadata using FFprobe.

    :param file_path: Path to the video file.
    :return: Creation date as a UNIX timestamp, or None if not found.
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        metadata = eval(result.stdout)  # Parse JSON-like output
        creation_time = metadata["format"].get("tags", {}).get("creation_time", None)
        if creation_time:
            creation_timestamp = datetime.fromisoformat(creation_time.replace("Z", "+00:00")).timestamp()
            return creation_timestamp
    except Exception as e:
        print(f"❌ Error retrieving creation date with FFprobe: {e}")
    return None

def set_file_timestamps(file_path, creation_timestamp):
    """
    Set the creation and modification timestamps for a file.

    :param file_path: Path to the file.
    :param creation_timestamp: UNIX timestamp to set as the creation/modification date.
    """
    try:
        os.utime(file_path, (creation_timestamp, creation_timestamp))
        print(f"✅ File timestamps updated: {file_path}")
    except Exception as e:
        print(f"❌ Error setting file timestamps: {e}")

def adjust_resolution(original_width, original_height, target_resolution):
    """
    Adjust the target resolution to maintain the aspect ratio.

    :param original_width: Original width of the video.
    :param original_height: Original height of the video.
    :param target_resolution: Desired resolution as (width, height).
    :return: Adjusted resolution as (width, height).
    """
    target_width, target_height = target_resolution
    aspect_ratio = original_width / original_height

    if round(aspect_ratio, 2) != round(target_width / target_height, 2):
        target_height = int(target_width / aspect_ratio)
    return make_dimensions_even(target_width, target_height)
