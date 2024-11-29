import yt_dlp
import os
import re

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best',  # 下载最佳质量
            'quiet': False,
            'no_warnings': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }

    @staticmethod
    def _is_valid_url(url):
        """验证YouTube URL格式"""
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
        
        # 更新下载配置
        self.ydl_opts.update({
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook]
        })
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 获取视频信息
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown Title')
                print(f"准备下载: {video_title}")
                
                # 开始下载
                ydl.download([url])
                
                # 构建输出文件路径
                output_file = os.path.join(output_path, f"{video_title}.mp4")
                if os.path.exists(output_file):
                    return output_file
                else:
                    # 尝试查找其他可能的扩展名
                    for ext in ['mkv', 'webm']:
                        alt_file = os.path.join(output_path, f"{video_title}.{ext}")
                        if os.path.exists(alt_file):
                            return alt_file
                            
                raise Exception("下载完成但未找到输出文件")
                
        except Exception as e:
            raise Exception(f"下载YouTube视频失败: {str(e)}")

    def _progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            if d.get('_percent_str'):
                print(f"\r下载进度: {d['_percent_str']}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n文件下载完成，正在处理...")

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
