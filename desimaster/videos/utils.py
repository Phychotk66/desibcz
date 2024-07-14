import os
import subprocess

def transcode_video(input_video_path, output_dir):
    resolutions = [(640, 360), (854, 480), (1280, 720)]

    for resolution in resolutions:
        width, height = resolution
        output_filename = f"video_{width}x{height}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        command = [
            'ffmpeg',
            '-i', input_video_path,
            '-s', f'{width}x{height}',
            '-c:v', 'libx264',
            '-crf', '23',
            '-c:a', 'copy',
            output_path
        ]

        subprocess.run(command, check=True)