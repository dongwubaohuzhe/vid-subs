
import os
import subprocess
import whisper
import datetime

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file using ffmpeg."""
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        '-y', # Overwrite output files without asking
        audio_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio from {video_path}: {e.stderr.decode()}")
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
    folder_path = input("Enter the path to the folder containing your MP4 video files: ")
    
    if not os.path.isdir(folder_path):
        print(f"Error: Folder \'{folder_path}\' not found or is not a directory.")
        return

    mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

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


