from pathlib import Path
import ffmpeg

from modules.logger import log
from modules.ffmpeg_config import get_ffmpeg_path

VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".avi", ".webm"}


def convert_video_to_audio(
        input_file: Path, 
        output_file: Path, 
        codec="mp3", 
        bitrate="192k"
    ):

    output_file.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = get_ffmpeg_path()

    (
        ffmpeg
        .input(str(input_file))
        .output(
            str(output_file),
            acodec=codec,
            audio_bitrate=bitrate
        )
        .overwrite_output()
        .run(cmd=ffmpeg_path, quiet=True)
    )

    return output_file


def iter_video_files(input_path: Path):
    if input_path.is_file():
        if input_path.suffix.lower() in VIDEO_EXTS:
            yield input_path
        return

    for file in input_path.rglob("*"):
        if file.is_file() and file.suffix.lower() in VIDEO_EXTS:
            yield file


def batch_convert(input_path: Path, output_dir: Path, codec="mp3", bitrate="192k"):
    files = list(iter_video_files(input_path))
    total = len(files)

    if total == 0:
        log("No video files found.")
        return []
    
    results = []

    for i, file in enumerate(files, start=1):
        base_path = input_path if input_path.is_dir() else input_path.parent
        relative_path = file.relative_to(base_path)
        output_file = (output_dir / relative_path).with_suffix(f".{codec}")

        log("")
        log(f"Converting file {i} of {total}")
        log(f"  FROM: {file}")
        log(f"  TO:   {output_file}")

        try:
            result = convert_video_to_audio(
                file,
                output_file,
                codec=codec,
                bitrate=bitrate
            )

            results.append(result)

            log(f"Finished file {i} of {total}")

        except Exception as e:
            log(f"ERROR on file {i} of {total}: {type(e).__name__}: {e}")

    return results