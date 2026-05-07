import yaml    # 读取 config.yaml 配置文件用
import os      # 读取环境变量（上线时用）
from typing import Dict, Any  # 给代码加类型提示
from model.openai_model import OpenAIModel
from model.zhipu_model import ZhipuModel
from model.glm_model import GLMModel
from model.deepseek_model import DeepSeekModel


class ModelManager:
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.current_model = self._get_current_model_config()

    def _load_config(self, path):
        """加载配置文件"""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _get_current_model_config(self) -> Dict[str, Any]:
        """
        自动获取当前模型配置
        优先级：
        1. 环境变量（上线用）
        2. 配置文件（本地开发用）
        """
        use_model = os.getenv(
            "USE_MODEL") or self.config["settings"]["use_model"]
        model_config = self.config["models"][use_model]

        # 环境变量覆盖 key（上线部署专用）
        env_key = os.getenv(f"{use_model.upper()}_API_KEY")
        if env_key:
            model_config["api_key"] = env_key

        return {
            "name": use_model,
            **model_config
        }

    def get_model(self):
        """根据配置创建并返回对应的模型实例"""
        config = self._get_current_model_config()
        model_name = config["name"]
        model = config["model"]
        api_key = config["api_key"]

        # 根据模型名称创建实例
        if model_name == "openai":
            return OpenAIModel(model, api_key)
        elif model_name == "zhipu":
            return ZhipuModel(model, api_key)
        elif model_name == "glm":
            return GLMModel(model, api_key)

        elif model_name == "deepseek":
            return DeepSeekModel(model, api_key)
        else:
            raise ValueError(f"不支持的模型类型: {model_name}")

    def get_api_key(self):
        return self.current_model["api_key"]

    def get_model_name(self):
        return self.current_model["model"]

    def get_output_format(self):
        return self.config["settings"]["output_format"]
