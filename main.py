
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
        audio_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e.stderr.decode()}")
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
    video_file = input("Enter the path to your MP4 video file: ")
    
    if not os.path.exists(video_file):
        print(f"Error: Video file \'{video_file}\' not found.")
        return

    file_name_without_ext = os.path.splitext(os.path.basename(video_file))[0]
    output_dir = os.path.dirname(video_file) if os.path.dirname(video_file) else "."

    audio_file = os.path.join(output_dir, f"{file_name_without_ext}.wav")
    srt_file = os.path.join(output_dir, f"{file_name_without_ext}.srt")

    print(f"Extracting audio from {video_file}...")
    try:
        extract_audio(video_file, audio_file)
        print("Audio extraction complete.")
    except Exception as e:
        print(f"Failed to extract audio: {e}")
        return

    print(f"Transcribing audio from {audio_file}...")
    try:
        transcription_result = transcribe_audio(audio_file)
        print("Transcription complete.")
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        return

    print(f"Generating SRT file {srt_file}...")
    try:
        generate_srt(transcription_result, srt_file)
        print("SRT file generation complete.")
    except Exception as e:
        print(f"Failed to generate SRT: {e}")
        return

    # Clean up audio file
    if os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"Cleaned up audio file: {audio_file}")

    print(f"Subtitles generated successfully at: {srt_file}")

if __name__ == "__main__":
    main()


