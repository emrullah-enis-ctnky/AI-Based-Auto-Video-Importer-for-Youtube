import os
import subprocess
import shutil
from PIL import Image
from .logger import logger

def is_ffmpeg_installed():
    """
    Checks if ffmpeg is installed and available in the system path.
    """
    return shutil.which("ffmpeg") is not None

def compress_video_for_ai(input_path, output_path):
    """
    Compresses a video to a low-resolution (480p) version for AI analysis.
    """
    if not is_ffmpeg_installed():
        logger.warning("FFmpeg bulunamadı, video sıkıştırılamıyor.")
        return input_path

    logger.info(f"Video AI analizi için optimize ediliyor (480p): {os.path.basename(input_path)}")
    
    try:
        # Construct ffmpeg command
        # -i input: Input file
        # -vf scale=-1:480: Scale height to 480p, maintain aspect ratio
        # -c:v libx264: Use H.264 codec
        # -crf 28: Constant Rate Factor (28 is good for compression)
        # -preset fast: Balance between compression speed and quality
        # -an: No audio (not needed for visual analysis, saves space)
        # -y: Overwrite output file
        command = [
            "ffmpeg", "-i", input_path,
            "-vf", "scale=-2:480",
            "-c:v", "libx264", "-crf", "28", "-preset", "fast",
            "-an", "-y", output_path
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        orig_size = os.path.getsize(input_path) / (1024 * 1024)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.debug(f"Video optimize edildi: {orig_size:.1f}MB -> {new_size:.1f}MB")
        
        return output_path
    except Exception as e:
        logger.error(f"Video sıkıştırma hatası: {str(e)}")
        return input_path

def compress_image_for_ai(input_path, output_path):
    """
    Compresses and resizes an image for AI analysis.
    """
    logger.info(f"Görsel AI analizi için optimize ediliyor: {os.path.basename(input_path)}")
    
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (Alpha channel fix for JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too large (e.g., max 1024px width)
            max_size = (1024, 1024)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(output_path, "JPEG", quality=70, optimize=True)
            
            orig_size = os.path.getsize(input_path) / 1024
            new_size = os.path.getsize(output_path) / 1024
            logger.debug(f"Görsel optimize edildi: {orig_size:.1f}KB -> {new_size:.1f}KB")
            
        return output_path
    except Exception as e:
        logger.error(f"Görsel sıkıştırma hatası: {str(e)}")
        return input_path
