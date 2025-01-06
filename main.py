import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from compressor.video_compressor import compress_video

# Fixed paths for source (input) and target (output) directories
SOURCE_DIR = "/usr/src/app/upload"
TARGET_DIR = "/usr/src/app/converted"

class VideoHandler(FileSystemEventHandler):
    """
    Watchdog event handler for processing new video files.
    """
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if file_path.lower().endswith(".mp4"):
            print(f"New file detected: {file_path}")

            # Wait until the file is fully written
            for _ in range(10):  # Retry for up to 10 seconds
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    break
                time.sleep(1)
            else:
                print(f"❌ Skipping {file_path} - File write incomplete.")
                return

            filename = os.path.basename(file_path)
            output_path = os.path.join(TARGET_DIR, filename)

            compress_video(file_path, output_path, TARGET_RESOLUTION, TARGET_BITRATE)

def main():
    global TARGET_RESOLUTION, TARGET_BITRATE
    TARGET_RESOLUTION = os.getenv("TARGET_RESOLUTION", "1920x1080")
    TARGET_BITRATE = os.getenv("TARGET_BITRATE", "3M")

    TARGET_RESOLUTION = tuple(map(int, TARGET_RESOLUTION.split("x")))

    os.makedirs(TARGET_DIR, exist_ok=True)

    print(f"Source Directory: {SOURCE_DIR}")
    print(f"Target Directory: {TARGET_DIR}")
    print(f"Target Resolution: {TARGET_RESOLUTION}")
    print(f"Target Bitrate: {TARGET_BITRATE}")

    # Monitor the source directory for changes
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_DIR, recursive=True)

    try:
        print("👀 Watching for new files...")
        observer.start()
        while True:
            time.sleep(5)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Stopping the watcher...")
    observer.join()

if __name__ == "__main__":
    main()
