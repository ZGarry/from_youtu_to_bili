import whisper
import os
import torch
import warnings
from pathlib import Path

class SubtitleGenerator:
    def __init__(self, model_name="base"):
        """
        初始化字幕生成器
        
        参数:
            model_name: 要使用的模型名称 ("tiny", "base", "small", "medium", "large")
        """
        print("正在初始化Whisper模型...")
        
        # 检查是否有GPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")
        
        try:
            # 根据设备类型设置模型参数
            if self.device == "cpu":
                # CPU模式：使用FP32
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
                    self.model = whisper.load_model(model_name)
            else:
                # GPU模式：可以使用FP16
                self.model = whisper.load_model(model_name).to(self.device)
            
            print(f"成功加载 {model_name} 模型")
        except Exception as e:
            raise Exception(f"加载模型失败: {str(e)}")
    
    def generate(self, video_path):
        """
        为视频生成字幕
        
        参数:
            video_path: 视频文件路径
        返回:
            str: 生成的字幕文件路径
        """
        try:
            # 使用 Path 对象处理路径
            video_path = Path(video_path).resolve()
            
            if not video_path.exists():
                raise ValueError(f"视频文件不存在: {video_path}")
                
            print(f"开始为视频生成字幕: {video_path.name}")
            print(f"完整文件路径: {str(video_path)}")
            
            # 使用Whisper模型生成字幕
            print("正在处理音频...")
            
            # 设置转录参数
            transcribe_options = {
                "task": "translate",  # 翻译为目标语言
                "language": "zh",     # 指定目标语言为中文
                "fp16": False if self.device == "cpu" else True  # CPU使用FP32，GPU使用FP16
            }
            
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
                result = self.model.transcribe(str(video_path), **transcribe_options)
            
            # 保存字幕文件
            subtitle_path = video_path.with_suffix('.srt')
            print(f"正在保存字幕文件: {subtitle_path.name}")
            
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(result["segments"], 1):
                    f.write(f"{i}\n")
                    f.write(f"{self._format_timestamp(segment['start'])} --> {self._format_timestamp(segment['end'])}\n")
                    f.write(f"{segment['text'].strip()}\n\n")
            
            print(f"字幕生成完成: {str(subtitle_path)}")
            return str(subtitle_path)
            
        except Exception as e:
            raise Exception(f"生成字幕失败: {str(e)}")
    
    def _format_timestamp(self, seconds):
        """
        格式化时间戳为SRT格式
        
        参数:
            seconds: 秒数
        返回:
            str: 格式化的时间戳 (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

if __name__ == '__main__':
    # 测试字幕生成功能
    # try:
    # 获取用户输入
    video_path = input("请输入视频文件路径: ").strip()
    if not video_path:
        print("错误: 请提供视频文件路径")
        exit(1)
        
    # 检查文件是否存在
    video_path = Path(video_path).resolve()
    if not video_path.exists():
        print(f"错误: 文件不存在: {video_path}")
        exit(1)
    
    print(f"文件存在，完整路径: {str(video_path)}")
    
    # 选择模型
    print("\n可用模型: tiny, base, small, medium, large")
    print("注意: 模型越大，准确度越高，但处理速度越慢且需要更多内存")
    model_name = input("请选择模型 (直接回车使用base模型): ").strip() or "base"
        
    # 初始化生成器并生成字幕
    generator = SubtitleGenerator(model_name)
    subtitle_path = generator.generate(str(video_path))
    print(f"字幕生成成功! 保存路径: {subtitle_path}")
        
    # except KeyboardInterrupt:
    #     print("\n字幕生成已取消")
    # except Exception as e:
    #     print(f"字幕生成失败: {str(e)}")
    
    