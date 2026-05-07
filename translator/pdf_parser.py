import os
import pdfplumber  # 用来读取PDF的库
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent  # 读取后的数据结构
from translator.pdf_exceptions import PageOutOfRangeException, PDFParseException
from utils import LOG


class PDFParser:
    def __init__(self):
        pass
      # 把 PDF 拆成文本 + 表格

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        # 校验输入文件是否正确
        if not pdf_file_path or pdf_file_path.strip() == "":
            raise PDFParseException("PDF 文件路径不能为空，请提供有效路径")

        if not os.path.exists(pdf_file_path):
            raise PDFParseException(f"文件不存在：{pdf_file_path}")

        if not pdf_file_path.lower().endswith(".pdf"):
            raise PDFParseException(f"仅支持PDF文件，当前文件：{pdf_file_path}")

        book = Book(pdf_file_path)  # 创建一本空 Book
        try:
            # 用 pdfplumber 打开 PDF，安全自动关闭
            with pdfplumber.open(pdf_file_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_parse = []
                # 页码越界处理
                if pages is not None and pages > len(pdf.pages):
                    raise PageOutOfRangeException(len(pdf.pages), pages)

                if pages is None:
                    pages_to_parse = pdf.pages  # 全部翻译

                elif isinstance(pages, int):
                    # 单个页码
                    if pages < 1 or pages > total_pages:
                        raise PageOutOfRangeException(total_pages, pages)
                    pages_to_parse = [pdf.pages[pages - 1]]

                elif isinstance(pages, (list, tuple)):
                    # 列表 [1,3,5] 或 范围 (2,6)
                    if len(pages) == 2 and isinstance(pages[0], int) and isinstance(pages[1], int):
                        # 范围 (start, end)
                        start, end = pages
                        if start < 1 or end > total_pages or start > end:
                            raise PageOutOfRangeException(
                                total_pages, f"{start}-{end}")
                        pages_to_parse = pdf.pages[start-1: end]
                    else:
                        # 列表 [2,4,6]
                        for p in pages:
                            if p < 1 or p > total_pages:
                                raise PageOutOfRangeException(total_pages, p)
                            pages_to_parse.append(pdf.pages[p-1])

                else:
                    raise PDFParseException(f"不支持的页码格式：{pages}")

                # 开始解析页面
                for pdf_page in pages_to_parse:
                    page = Page()  # 创建一页

                    raw_text = pdf_page.extract_text()  # 整页所有文字
                    tables = pdf_page.extract_tables()  # 整页所有表格

                    # 把表格里的每个字，从正文里删掉 → 正文就纯文本，表格单独处理
                    for table_data in tables:
                        for row in table_data:
                            for cell in row:
                                raw_text = raw_text.replace(cell, "", 1)

                    # 处理文本
                    if raw_text:
                        raw_text_lines = raw_text.splitlines()  # 去掉空行
                        cleaned_raw_text_lines = [
                            line.strip() for line in raw_text_lines if line.strip()]  # 去掉每行前后空格
                        cleaned_raw_text = "\n".join(
                            cleaned_raw_text_lines)  # 清理干净文本

                        text_content = Content(
                            content_type=ContentType.TEXT, original=cleaned_raw_text)
                        page.add_content(text_content)
                        LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                    # 把提取到的表格，单独存成一个内容块。
                    if tables:
                        table = TableContent(tables)
                        page.add_content(table)
                        LOG.debug(f"[table]\n{table}")

                    book.add_page(page)

            return book
        except Exception as e:
            raise PDFParseException(f"PDF 解析失败，文件可能损坏或加密：{str(e)}")
