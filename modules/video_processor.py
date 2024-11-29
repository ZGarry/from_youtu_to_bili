import subprocess
import os
from pathlib import Path

class VideoProcessor:
    def __init__(self):
        pass

    def _format_path(self, path):
        """格式化路径为ffmpeg可用的格式"""
        # 将Windows路径转换为ffmpeg可用的格式
        return str(path).replace('\\', '/').replace(':', '\\:')

    def burn_subtitle(self, video_path, subtitle_path, output_path=None):
        """
        将字幕烧录到视频中，保留原视频的音频
        
        参数:
            video_path: 视频文件路径
            subtitle_path: 字幕文件路径
            output_path: 输出文件路径，如果为None则自动生成
        """
        try:
            # 使用Path处理路径
            video_path = Path(video_path).resolve()
            subtitle_path = Path(subtitle_path).resolve()
            
            if not video_path.exists():
                raise ValueError(f"视频文件不存在: {video_path}")
            if not subtitle_path.exists():
                raise ValueError(f"字幕文件不存在: {subtitle_path}")
                
            # 如果没有指定输出路径，则在原视频同目录下创建新文件
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}_with_subtitle{video_path.suffix}"
            else:
                output_path = Path(output_path).resolve()
                
            print(f"开始处理视频: {video_path.name}")
            print("正在合成视频和字幕...")

            # 格式化路径
            # 构建字幕滤镜参数
            xs =  str(subtitle_path).replace(':','\\:').replace('\\','/')
            subtitle_filter = f"subtitles={xs}"
            
            # 构建ffmpeg命令
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vf', subtitle_filter,
                '-c:a', 'copy',
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-y',
                str(output_path)
            ]

            print("执行命令:", ' '.join(cmd))  # 打印完整命令以便调试

            # 执行命令
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # 获取输出
            stdout, stderr = process.communicate()
            
            # 检查是否成功
            if process.returncode != 0:
                print("FFmpeg错误:")
                print("stdout:", stdout)
                print("stderr:", stderr)
                raise Exception("ffmpeg 处理失败")
            
            if not output_path.exists():
                raise Exception("输出文件未生成")
            
            print(f"处理完成，输出文件: {output_path}")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            print("FFmpeg错误:")
            print("stdout:", e.stdout)
            print("stderr:", e.stderr)
            raise Exception(f"合成视频和字幕失败: {str(e)}")
        except Exception as e:
            raise Exception(f"处理视频失败: {str(e)}")

if __name__ == '__main__':
    # 测试代码
    try:
        # 获取用户输入
        video_path = input("请输入视频文件路径: ").strip()
        subtitle_path = input("请输入字幕文件路径: ").strip()
        
        processor = VideoProcessor()
        output_path = processor.burn_subtitle(video_path, subtitle_path)
        print(f"测试成功! 输出文件: {output_path}")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")