from .page import Page

class Book:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path # 存储PDF文件路径用于溯源
        self.pages = [] # 存储文档所有页面的列表

    def add_page(self, page: Page):
        self.pages.append(page) #向book对象中添加page对象