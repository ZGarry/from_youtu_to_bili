import argparse
from modules.youtube_downloader import YouTubeDownloader
from modules.subtitle_generator import SubtitleGenerator
from modules.bilibili_uploader import BilibiliUploader
from modules.config_loader import load_config

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='YouTube视频搬运到Bilibili工具')
    parser.add_argument('--url', required=True, help='YouTube视频URL')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    try:
        # 下载YouTube视频
        downloader = YouTubeDownloader()
        video_path = downloader.download(args.url)
        
        # 生成字幕
        subtitle_generator = SubtitleGenerator()
        subtitle_path = subtitle_generator.generate(video_path)
        
        # 上传到Bilibili
        uploader = BilibiliUploader(config['bilibili'])
        video_info = uploader.upload(video_path, subtitle_path)
        
        print(f"上传成功！视频地址: {video_info['url']}")
        
    except Exception as e:
        print(f"处理失败: {str(e)}")

if __name__ == '__main__':
    main() 