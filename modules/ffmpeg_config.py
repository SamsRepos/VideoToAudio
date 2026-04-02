import json
from pathlib import Path
import ffmpeg

from modules.logger import log

CONFIG_PATH = Path("config.json")

_ffmpeg_path = None 

def init_ffmpeg_path():
    global _ffmpeg_path

    if not CONFIG_PATH.exists():
        raise RuntimeError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    path = config.get("ffmpeg_path")

    if not path:
        raise RuntimeError("ffmpeg_path missing in config.json")

    path = Path(path)

    if not path.exists():
        raise RuntimeError(f"FFmpeg not found at: {path}")

    _ffmpeg_path = str(path)

    log(f"Using FFmpeg: {_ffmpeg_path}")

def get_ffmpeg_path():
    global _ffmpeg_path
    
    if _ffmpeg_path is None:
        init_ffmpeg_path()
    
    return _ffmpeg_path