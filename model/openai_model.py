import time
import openai
from model import Model
from utils import LOG
from openai import OpenAI


class OpenAIModel(Model):
    """
    OpenAI 接口连接器，负责调用接口进行翻译
    包含自动重试、异常处理、接口兼容逻辑
    """

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def call_requestAI(self, prompt_text):
        """
        调用 OpenAI 接口，带失败重试机制
        返回：翻译结果, 是否成功
        """
        retry_times = 0
        while retry_times < 3:
            try:
                if self.model == "gpt-3.5-turbo":
                    # 新版对话模型
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt_text}
                        ]
                    )
                    translation = response.choices[0].message.content.strip()
                else:
                    # 旧版补全模型
                    response = self.client.completions.create(
                        model=self.model,
                        prompt=prompt_text,
                        max_tokens=150,
                        temperature=0
                    )
                    translation = response.choices[0].text.strip()

                return translation, True
            except openai.RateLimitError as e:
              # 处理限流错误，等待60秒 → 重试
                retry_times += 1
                if retry_times < 3:
                    LOG.warning("调用频率超限，60秒后自动重试...")
                    time.sleep(60)
                else:
                    raise Exception("调用次数超限，已达到最大重试次数.")
            except openai.APIConnectionError as e:
                print("无法连接到 OpenAI 服务器，请检查网络")
                print(e.__cause__)
            except openai.APIStatusError as e:
                print("接口返回异常状态码")
                print(e.status_code)
                print(e.response)
            except Exception as e:
                raise Exception(f"接口调用发生未知错误：{e}")
        return "", False
