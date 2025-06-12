# MP4 Subtitle Generator

This project provides a Python script to extract audio from MP4 video files, transcribe the audio using OpenAI's Whisper model, and generate an SRT subtitle file with proper punctuation and timestamps. All processing is done locally.

## Features

*   **Local Processing:** No external API calls are made for transcription.
*   **Accurate Transcription:** Leverages OpenAI's Whisper model for high-quality speech-to-text conversion.
*   **Proper Punctuation:** Generates subtitles with correct punctuation.
*   **SRT Output:** Creates industry-standard SRT subtitle files with precise timestamps.
*   **Batch Processing:** Processes all MP4 files within a specified folder.
*   **Overwrites Intermediate Files:** Automatically overwrites intermediate audio (.wav) and subtitle (.srt) files in the same folder.
*   **Flexible FFmpeg Path:** Allows specifying the FFmpeg executable path directly in the script or via user input if not in system PATH.
*   **Easy to Use:** Designed for straightforward execution on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+:** You can download it from [python.org](https://www.python.org/downloads/).
*   **uv:** A fast Python package installer and resolver. If you don't have it, you can install it using pip:
    ```bash
    pip install uv
    ```
*   **FFmpeg:** A complete, cross-platform solution to record, convert and stream audio and video. Download it from [ffmpeg.org](https://ffmpeg.org/download.html).
    *   **Important:** It's highly recommended to add FFmpeg to your system's PATH environment variable for seamless operation. If you don't, the script will prompt you to enter the path to the FFmpeg executable.

## Project Setup

1.  **Clone or Download:** Download the project files to your local machine.

2.  **Navigate to Project Directory:** Open your terminal or command prompt and navigate to the `subtitle_generator` directory:

    ```bash
    cd path/to/subtitle_generator
    ```

3.  **Install Dependencies:** Use `uv` to install the required Python packages:

    ```bash
    uv pip install -r requirements.txt
    ```

    This will install `openai-whisper` and `ffmpeg-python`.

## How to Run the Script

1.  **Place your MP4 files:** Put all the MP4 video files you want to subtitle into a single folder.

2.  **Run the script:** Execute the `main.py` script from your terminal:

    ```bash
    python main.py
    ```

3.  **FFmpeg Path (if prompted):** If FFmpeg is not found in your system's PATH, the script will prompt you to enter the full path to your FFmpeg executable (e.g., `C:\ffmpeg\bin\ffmpeg.exe` on Windows or `/usr/local/bin/ffmpeg` on macOS/Linux). You can also set the `FFMPEG_PATH` variable directly in `main.py` if you prefer.

4.  **Enter folder path:** The script will then prompt you to enter the path to the folder containing your MP4 video files. You can drag and drop the folder into the terminal window to automatically paste its path, or type it manually.

5.  **Output:** For each MP4 file in the specified folder, an SRT file with the same name (e.g., `your_video.srt`) will be created in the same directory. Any existing `.wav` or `.srt` files with matching names will be overwritten.

## Playing Subtitles in Windows Media Player

Windows Media Player (WMP) can play SRT subtitle files if they are named correctly and placed in the same directory as the video file.

1.  **Name Convention:** Ensure your SRT file has the exact same name as your MP4 video file, with only the extension differing. For example:
    *   `my_video.mp4`
    *   `my_video.srt`

2.  **Placement:** Both the MP4 video file and the SRT subtitle file must be in the same folder.

3.  **Open with WMP:** Open the MP4 video file with Windows Media Player. The subtitles should automatically appear.

    *   If subtitles don't appear, ensure they are enabled in WMP settings:
        *   Right-click on the video playback area.
        *   Go to `Lyrics, captions, and subtitles`.
        *   Select `On if available` or `On`.


