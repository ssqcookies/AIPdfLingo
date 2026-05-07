import os
from model_manager import ModelManager
from translator.pdf_translator import PDFTranslator
from translator.pdf_exceptions import PDFParseException

# 1. 加载模型配置
model = ModelManager()

# 2. 实例化翻译器
translator = PDFTranslator(model.get_model())

# 3. 文件路径动态传入（你可以改成 input 或者 GUI 传入）
file_path = input("请输入要翻译的 PDF 文件路径：").strip()

# 👇 第一层：空值校验
if not file_path:
    print("❌ 错误：文件路径不能为空")
    exit(1)

# 👇 第二层：文件存在校验
if not os.path.exists(file_path):
    print(f"❌ 错误：文件不存在 - {file_path}")
    raise PDFParseException("文件不存在，请检查路径是否正确")

# 👇 第三层：格式校验
if not file_path.lower().endswith(".pdf"):
    print(f"❌ 错误：文件不是 PDF 格式 - {file_path}")
    raise PDFParseException("只支持 PDF 文件格式")

# 4. 调用翻译方法
translator.translate_pdf(
    pdf_file_path=file_path,
    output_file_format=model.get_output_format()
)
