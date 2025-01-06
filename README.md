# EctoPress

**EctoPress** is a video compression tool inspired by the ghostly precision and power of the Ghostbusters' universe. It efficiently compresses large video files into smaller, high-quality outputs while preserving metadata like the original creation date and aspect ratio. With automatic folder monitoring and customizable settings, EctoPress is ideal for media optimization workflows.

---

## Features

### 🔥 High-Quality Video Compression
- Compresses MP4 videos to smaller sizes while retaining excellent quality.
- Customizable target resolution and bitrate for fine-tuned compression.

### 🕒 Metadata Preservation
- Automatically extracts and retains the original creation date for compressed files.

### 📐 Aspect Ratio Handling
- Ensures videos maintain their original aspect ratio during resizing.
- Special handling for specific resolutions like 2160x3840, adjusting to 1080x1920 when necessary.

### ⚙️ Automation
- Monitors a specified source folder for new video files and compresses them automatically.

### 🛠 Customizable Settings
- Use environment variables to define target resolution, bitrate, and source/target directories.

### 🧹 Clean Logs
- Suppresses unnecessary FFmpeg logs for a streamlined user experience.

---

## Installation

### Prerequisites
- Docker

### Clone the Repository
```bash
git clone https://github.com/<your-username>/ectopress.git
cd ectopress
```

### Build the Docker Image
```bash
docker build -t ectopress .
```

---

## Usage

### Environment Variables

| Variable            | Default Value          | Description                           |
|---------------------|------------------------|---------------------------------------|
| `SOURCE_DIR`        | `/usr/src/app/upload`  | Directory for input video files.      |
| `TARGET_DIR`        | `/usr/src/app/converted` | Directory for compressed videos.      |
| `TARGET_RESOLUTION` | `1280x720`            | Resolution for the compressed videos. |
| `TARGET_BITRATE`    | `2M`                  | Bitrate for the compressed videos.    |

### Running the Container

```bash
docker run -d \
  -e TARGET_RESOLUTION=1920x1080 \
  -e TARGET_BITRATE=3M \
  -v /path/to/upload:/usr/src/app/upload \
  -v /path/to/converted:/usr/src/app/converted \
  ectopress
```

### Automatic Compression
1. Place your videos in the `/path/to/upload` directory.
2. Compressed videos will be automatically saved in the `/path/to/converted` directory.

---

## How It Works

1. **Monitor Folder**: Watches the `SOURCE_DIR` for new video files.
2. **Compress Video**: Processes each new file, resizing and compressing it to the specified resolution and bitrate.
3. **Preserve Metadata**: Copies the original creation date to the compressed file.
4. **Output**: Saves the compressed video in the `TARGET_DIR`.

---

## Example Logs

```plaintext
📅 Original Creation Date: 2025-01-05T23:07:00
🎥 Compressing /usr/src/app/upload/video1.mp4
✅ File timestamps updated: /usr/src/app/converted/video1_compressed.mp4
✅ Compression successful! Output saved at: /usr/src/app/converted/video1_compressed.mp4
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](http://rflpazini.mit-license.org/) file for details.

---

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request to help improve EctoPress.

---

## Acknowledgments

Special thanks to the Ghostbusters universe for the inspiration behind EctoPress's name and theme.
