import yt_dlp
import os
from pathlib import Path

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # 优先选择最佳mp4格式
            'merge_output_format': 'mp4',  # 确保输出mp4格式
            'quiet': False,
            'no_warnings': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }

    @staticmethod
    def _is_valid_url(url):
        """验证YouTube URL格式"""
        import re
        return bool(re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/', url))

    def download(self, url, output_path='downloads'):
        """
        从YouTube下载视频
        
        参数:
            url: YouTube视频URL
            output_path: 保存目录路径
        返回:
            str: 下载文件的完整路径
        """
        if not self._is_valid_url(url):
            raise ValueError("无效的YouTube URL")
            
        # 创建输出目录
        os.makedirs(output_path, exist_ok=True)
        
        try:
            # 更新下载选项
            self.ydl_opts.update({
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook]
            })
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 获取视频信息
                print("正在获取视频信息...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
                print(f"视频标题: {video_title}")
                
                # 清理文件名中的非法字符
                video_title = "".join(x for x in video_title if x.isalnum() or x in (' ', '-', '_'))
                output_file = os.path.join(output_path, f"{video_title}.mp4")
                
                # 下载视频
                print("开始下载视频...")
                ydl.download([url])
                
                # 检查文件是否存在
                if os.path.exists(output_file):
                    print(f"下载完成: {output_file}")
                    return output_file
                else:
                    # 尝试查找其他可能的文件名
                    files = os.listdir(output_path)
                    for file in files:
                        if file.startswith(video_title) and file.endswith('.mp4'):
                            output_file = os.path.join(output_path, file)
                            print(f"找到下载文件: {output_file}")
                            return output_file
                            
                raise Exception("下载完成但未找到输出文件")
                
        except Exception as e:
            raise Exception(f"下载YouTube视频失败: {str(e)}")

    def _progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                print(f"\r下载进度: {percent} 速度: {speed}", end='', flush=True)
            except:
                print("\r正在下载...", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n下载完成，正在处理...")

if __name__ == '__main__':
    # 测试下载功能
    downloader = YouTubeDownloader()
    try:
        # 获取用户输入
        url = input("请输入YouTube视频URL (直接回车使用默认测试URL): ").strip() or "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        path = input("请输入保存路径 (直接回车使用默认downloads目录): ").strip() or 'downloads'
        
        # 开始下载
        video_path = downloader.download(url, path)
        print(f"视频下载成功! 保存路径: {video_path}")
    except KeyboardInterrupt:
        print("\n下载已取消")
    except Exception as e:
        print(f"下载失败: {str(e)}")
