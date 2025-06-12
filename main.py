
import os
import subprocess
import whisper
import datetime

# --- Configuration --- #
# Set the path to your FFmpeg executable here if it's not in your system's PATH.
# For example, on Windows: FFMPEG_PATH = r'C:\ffmpeg\bin\ffmpeg.exe'
# On macOS/Linux, if not in PATH: FFMPEG_PATH = '/usr/local/bin/ffmpeg'
FFMPEG_PATH = 'ffmpeg' # Default: assumes ffmpeg is in system PATH

# --- Functions --- #

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file using ffmpeg."""
    command = [
        FFMPEG_PATH,
        '-i', video_path,
        '-vn', # No video output
        '-acodec', 'pcm_s16le', # Audio codec
        '-ar', '16000', # Audio sample rate
        '-ac', '1', # Mono audio
        '-y', # Overwrite output files without asking
        audio_path
    ]
    try:
        # Check if FFMPEG_PATH is default and try to find ffmpeg if it is
        # This helps if ffmpeg is in PATH but not explicitly set
        effective_ffmpeg_path = FFMPEG_PATH
        if FFMPEG_PATH == 'ffmpeg':
            try:
                # Try to run ffmpeg -version to see if it's in PATH
                subprocess.run([FFMPEG_PATH, '-version'], check=True, capture_output=True, shell=True if os.name == 'nt' else False)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If not found in PATH, prompt user or use a known location
                print("FFmpeg not found in PATH. Please ensure it is installed and in your PATH, or set FFMPEG_PATH in the script.")
                # You could add a prompt here to ask the user for the path if desired
                # For now, we will raise the error to indicate it needs to be configured.
                raise FileNotFoundError("FFmpeg not found. Please set FFMPEG_PATH in the script or add FFmpeg to your system PATH.")

        print(f"Using FFmpeg from: {effective_ffmpeg_path}")
        process = subprocess.run(command, check=True, capture_output=True, text=True, shell=True if os.name == 'nt' else False)
        print(f"FFmpeg stdout: {process.stdout}")
        if process.stderr:
            print(f"FFmpeg stderr: {process.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio from {video_path}. FFmpeg command: {' '.join(command)}")
        print(f"FFmpeg stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print(f"Error: The FFmpeg executable was not found at the specified path: {FFMPEG_PATH}")
        print("Please ensure FFmpeg is installed and the FFMPEG_PATH variable in the script is set correctly, or that ffmpeg is in your system's PATH.")
        raise

def transcribe_audio(audio_path, model_name="base"):
    """Transcribes audio using OpenAI Whisper."""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

def format_timestamp(seconds):
    ms = int(seconds * 1000) % 1000
    dt = datetime.datetime.fromtimestamp(seconds, tz=datetime.timezone.utc)
    return dt.strftime("%H:%M:%S,") + f"{ms:03d}"

def generate_srt(transcription_result, output_path):
    """Generates an SRT file from Whisper transcription result with proper timestamping."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription_result["segments"]):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i + 1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def main():
    global FFMPEG_PATH # Allow main to modify FFMPEG_PATH if needed based on user input or config file in future

    # Check if FFMPEG_PATH needs to be set by the user if default 'ffmpeg' fails
    # This initial check can be done once
    if FFMPEG_PATH == 'ffmpeg':
        try:
            subprocess.run([FFMPEG_PATH, '-version'], check=True, capture_output=True, shell=True if os.name == 'nt' else False)
            print(f"FFmpeg found in PATH and will be used: {FFMPEG_PATH}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("FFmpeg not found in system PATH.")
            user_ffmpeg_path = input("Please enter the full path to your FFmpeg executable (e.g., C:\\ffmpeg\\bin\\ffmpeg.exe) or press Enter to skip if you've set it in the script: ").strip()
            if user_ffmpeg_path:
                if os.path.isfile(user_ffmpeg_path):
                    FFMPEG_PATH = user_ffmpeg_path
                    print(f"Using FFmpeg from user-provided path: {FFMPEG_PATH}")
                else:
                    print(f"Error: The provided FFmpeg path \"{user_ffmpeg_path}\" is not a valid file. Exiting.")
                    return
            else:
                print("No path provided, and FFmpeg not found in PATH. Please set FFMPEG_PATH at the top of the script. Exiting.")
                return
    elif not os.path.isfile(FFMPEG_PATH):
        print(f"Error: The FFMPEG_PATH \"{FFMPEG_PATH}\" set in the script is not a valid file. Exiting.")
        return
    else:
        print(f"Using FFmpeg from script-defined path: {FFMPEG_PATH}")


    folder_path = input("Enter the path to the folder containing your MP4 video files: ")
    
    if not os.path.isdir(folder_path):
        print(f"Error: Folder \'{folder_path}\' not found or is not a directory.")
        return

    mp4_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".mp4")]

    if not mp4_files:
        print(f"No MP4 files found in \'{folder_path}\'")
        return

    for video_file_name in mp4_files:
        video_path = os.path.join(folder_path, video_file_name)
        file_name_without_ext = os.path.splitext(video_file_name)[0]
        
        audio_file = os.path.join(folder_path, f"{file_name_without_ext}.wav")
        srt_file = os.path.join(folder_path, f"{file_name_without_ext}.srt")

        print(f"\nProcessing {video_file_name}...")

        print(f"Extracting audio from {video_file_name}...")
        try:
            extract_audio(video_path, audio_file)
            print("Audio extraction complete.")
        except Exception as e:
            print(f"Skipping {video_file_name} due to audio extraction error: {e}")
            continue

        print(f"Transcribing audio from {audio_file}...")
        try:
            transcription_result = transcribe_audio(audio_file)
            print("Transcription complete.")
        except Exception as e:
            print(f"Skipping {video_file_name} due to audio transcription error: {e}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
            continue

        print(f"Generating SRT file {srt_file}...")
        try:
            generate_srt(transcription_result, srt_file)
            print("SRT file generation complete.")
        except Exception as e:
            print(f"Skipping {video_file_name} due to SRT generation error: {e}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
            continue

        # Clean up audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Cleaned up audio file: {audio_file}")

        print(f"Subtitles generated successfully for {video_file_name} at: {srt_file}")

    print("\nAll MP4 files processed.")

if __name__ == "__main__":
    main()


