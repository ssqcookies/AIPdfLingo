import requests
from model import Model
from utils import LOG
import time


class GLMModel(Model):
    def __init__(self, model_url: str, timeout=300):
        self.model_url = model_url
        self.timeout = timeout

    def call_requestAI(self, prompt_text):
        retry_times = 0
        while retry_times < 3:
            try:
                payload = {
                    "prompt": prompt_text,
                    "timeout": self.timeout
                }
                response = requests.post(
                    self.model_url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                translation = response.json()["response"].strip()
                return translation, True

            except requests.exceptions.RequestException as e:
                retry_times += 1
                if retry_times < 3:
                    LOG.warning(f"GLM调用失败，60秒后重试: {e}")
                    time.sleep(60)
                else:
                    raise Exception(f"GLM调用失败，已达最大重试次数: {e}")

        return "", False
