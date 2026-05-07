from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser  # ✅ 加上 translator 包路径
from translator.writer import Writer        # ✅ 加上 translator 包路径
from utils import LOG


class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()  # 创建PDF解析器
        self.writer = Writer()        # 创建文件保存器

    def translate_pdf(self, pdf_file_path: str, output_file_format: str = 'Markdown', target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        # 让PDF 解析器去把 PDF 拆成：一页一页、文本 + 表格，最后返回一个Book 对象
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)
        # 逐页、逐段翻译
        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                # 生成翻译提示词
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                # 调用 AI 进行翻译
                translation, status = self.model.call_requestAI(prompt)
                LOG.info(translation)

                # 把翻译好的文字，写回书本里对应的位置。
                self.book.pages[page_idx].contents[content_idx].set_translation(
                    translation, status)

        self.writer.save_translated_book(
            self.book, output_file_path, output_file_format)
