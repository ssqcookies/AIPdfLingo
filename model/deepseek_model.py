from model import Model
from utils import LOG
from openai import OpenAI
import time


class DeepSeekModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def call_requestAI(self, prompt_text_text):
        retry_times = 0
        while retry_times < 3:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt_text_text}]
                )
                translation = response.choices[0].message.content.strip()
                return translation, True

            except Exception as e:
                retry_times += 1
                if retry_times < 3:
                    LOG.warning(f"DeepSeek调用失败，60秒后重试: {e}")
                    time.sleep(60)
                else:
                    raise Exception(f"DeepSeek调用失败，已达最大重试次数: {e}")

        return "", False
