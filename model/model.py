from book import ContentType


class Model:
    # 文本翻译提示模板：翻译为{target_language}:{text}
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"翻译为{target_language}：{text}"
    # 表格翻译提示模板：翻译为{target_language},保持间距（空格，分隔符），以表格形式返回：\n{table}

    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f"翻译为{target_language}，以空格和换行符表示表格：\n{table}"
    # 内容类型判断：根据ContentType选择对应的提示词构造方法

    def translate_prompt(self, content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), target_language)

    def call_requestAI(self, prompt):
        raise NotImplementedError("子类必须实现 call_requestAI 方法")
