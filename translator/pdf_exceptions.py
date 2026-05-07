class PageOutOfRangeException(Exception):
    """页码超出范围异常"""
    def __init__(self, total_pages: int, requested_pages: int):
        self.total_pages = total_pages
        self.requested_pages = requested_pages
        super().__init__(
            f"页码超出范围：PDF 共 {total_pages} 页，请求了 {requested_pages} 页"
        )


class PDFParseException(Exception):
    """PDF 文件解析失败异常"""
    def __init__(self, message: str = "PDF 文件解析失败，文件可能损坏或格式不正确"):
        super().__init__(message)


class TranslationException(Exception):
    """翻译过程失败异常"""
    def __init__(self, message: str = "翻译失败，请检查模型接口或网络"):
        super().__init__(message)


class APIKeyInvalidException(Exception):
    """API Key 无效或未配置异常"""
    def __init__(self, model_name: str = None):
        if model_name:
            super().__init__(f"模型 {model_name} 的 API Key 无效、未填写或权限不足")
        else:
            super().__init__("API Key 无效、为空或权限配置错误")