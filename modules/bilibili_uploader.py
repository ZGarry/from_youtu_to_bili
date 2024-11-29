from bilibili_api import video, Credential

class BilibiliUploader:
    def __init__(self, config):
        self.credential = Credential(
            sessdata=config['sessdata'],
            bili_jct=config['bili_jct'],
            buvid3=config['buvid3']
        )
    
    def upload(self, video_path, subtitle_path):
        try:
            # 创建视频对象
            v = video.VideoUploader(self.credential)
            
            # 读取字幕
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                subtitle_content = f.read()
            
            # 上传视频
            video_info = v.upload_with_subtitle(
                video_path,
                subtitle_content,
                title="自动搬运的视频",
                tid=122,  # 野生技术协会分区
                tag=["技术", "科技", "编程"],
                desc="这是一个自动搬运的视频"
            )
            
            return video_info
        except Exception as e:
            raise Exception(f"上传到Bilibili失败: {str(e)}") 