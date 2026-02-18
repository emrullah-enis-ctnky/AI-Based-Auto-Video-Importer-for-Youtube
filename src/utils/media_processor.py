import os
import subprocess
import shutil
from PIL import Image
from .logger import logger, console

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

    try:
        with console.status(f"[bold yellow]Video AI analizi için optimize ediliyor (480p)...[/bold yellow]") as status:
            # Construct ffmpeg command
            command = [
                "ffmpeg", "-i", input_path,
                "-vf", "scale=-2:480",
                "-c:v", "libx264", "-crf", "28", "-preset", "fast",
                "-an", "-y", output_path
            ]
            
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            orig_size = os.path.getsize(input_path) / (1024 * 1024)
            new_size = os.path.getsize(output_path) / (1024 * 1024)
            logger.success(f"Video optimize edildi: {orig_size:.1f}MB -> [bold green]{new_size:.1f}MB[/bold green]")
        
        return output_path
    except Exception as e:
        logger.error(f"Video sıkıştırma hatası: {str(e)}")
        return input_path

def compress_image_for_ai(input_path, output_path):
    """
    Compresses and resizes an image for AI analysis.
    """
    try:
        with console.status(f"[bold yellow]Görsel AI analizi için optimize ediliyor...[/bold yellow]") as status:
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
                logger.success(f"Görsel optimize edildi: {orig_size:.1f}KB -> [bold green]{new_size:.1f}KB[/bold green]")
            
        return output_path
    except Exception as e:
        logger.error(f"Görsel sıkıştırma hatası: {str(e)}")
        return input_path
