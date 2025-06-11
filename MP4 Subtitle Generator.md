# MP4 Subtitle Generator

This project provides a Python script to extract audio from MP4 video files, transcribe the audio using OpenAI's Whisper model, and generate an SRT subtitle file with proper punctuation and timestamps. All processing is done locally.

## Features

*   **Local Processing:** No external API calls are made for transcription.
*   **Accurate Transcription:** Leverages OpenAI's Whisper model for high-quality speech-to-text conversion.
*   **Proper Punctuation:** Generates subtitles with correct punctuation.
*   **SRT Output:** Creates industry-standard SRT subtitle files with precise timestamps.
*   **Easy to Use:** Designed for straightforward execution on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+:** You can download it from [python.org](https://www.python.org/downloads/).
*   **uv:** A fast Python package installer and resolver. If you don't have it, you can install it using pip:
    ```bash
    pip install uv
    ```
*   **FFmpeg:** A complete, cross-platform solution to record, convert and stream audio and video. Download it from [ffmpeg.org](https://ffmpeg.org/download.html) and ensure it's added to your system's PATH.




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

1.  **Place your MP4 file:** Put the MP4 video file you want to subtitle in the same directory as the `main.py` script, or provide the full path to the video file when prompted.

2.  **Run the script:** Execute the `main.py` script from your terminal:

    ```bash
    python main.py
    ```

3.  **Enter video path:** The script will prompt you to enter the path to your MP4 video file. You can drag and drop the file into the terminal window to automatically paste its path, or type it manually.

4.  **Output:** After processing, an SRT file with the same name as your video file (e.g., `your_video.srt`) will be created in the same directory as your video.




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



