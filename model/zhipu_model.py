from model import Model
from utils import LOG
from zhipuai import ZhipuAI
import time


class ZhipuModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = ZhipuAI(api_key=api_key)

    def call_requestAI(self, prompt_text):
        retry_times = 0
        while retry_times < 3:
            try:
                # 智谱统一调用格式
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt_text}]
                )
                translation = response.choices[0].message.content.strip()
                return translation, True

            except Exception as e:
                retry_times += 1
                if retry_times < 3:
                    LOG.warning(f"智谱API调用失败，60秒后重试: {e},{self.model}")
                    time.sleep(60)
                else:
                    raise Exception(f"智谱API调用失败，已达最大重试次数: {e}")

        return "", False
