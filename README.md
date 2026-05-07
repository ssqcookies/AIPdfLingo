# AIPdfLingo

## 介绍
AIPdfLingo翻译器是一个使用 AI 技术将英文 PDF 书籍翻译成中文的工具。这个工具使用了大型语言模型 (LLMs)，内置几种模型OpenAI、智谱，deepseek等模型来进行翻译。
它是用Python构建的，并且具有灵活、模块化和面向对象的设计，多模型支持、自定义异常、完整防御校验。

本项目基于课程/开源GPL项目二次开发，仅作为个人学习项目作品。

## 特性

v1.0
- [X] 翻译方向: 目前仅支持英译中。使用大型语言模型 (LLMs) 将英文 PDF 书籍翻译成中文。
- [X] 输入格式: 支持PDF文件上传
- [X] 输出格式: 可导出markdown或PDF格式，默认markdown
- [X] 目前内置几种模型OpenAI、智谱，deepseek等模型
- [X] 配置方式: 通过 YAML 配置文件或命令行参数灵活配置。
- [X] 支持指定任意页码、页码列表、页码范围翻译（pages=3、pages=[2,4,6]、pages=(2,5) → 2～5 页、pages=None → 全部翻译）
- [X] 模块化和面向对象的设计，易于定制和扩展。
v2.0
- [ ] 实现图形用户界面 (GUI) 以便更易于使用。
- [ ] 添加对多个 PDF 文件的批处理支持。
- [ ] 创建一个网络服务或 API，以便在网络应用中使用。
- [ ] 添加对其他语言和翻译方向的支持。
- [ ] 添加对保留源 PDF 的原始布局和格式的支持。
- [ ] 通过使用自定义训练的翻译模型来提高翻译质量。


## 项目结构
AIPdfLingo/
├── config.yaml              # 模型配置文件，存放 API_KEY、模型名称等
├── config.example.yaml      # 模型配置示例文件，不含真实密钥
├── model_manager.py         # 多模型管理中心，根据配置自动创建并返回模型实例
├── book/
│   ├── __init__.py          # 模块导出入口，统一暴露 Book、Page、Content 等类
│   ├── book.py              # 书籍对象，承载整个 PDF 的结构、页面、内容
│   ├── content.py           # 内容基类，定义文本、表格、图片等统一数据结构
│   └── page.py              # 页面对象，管理一页内的所有文本、表格、图片
├── model/
│   ├── __init__.py          # 模型模块导出入口，对外提供所有模型接口
│   ├── model.py             # 模型抽象基类，定义统一翻译接口（所有模型必须继承）
│   ├── openai_model.py      # OpenAI 模型对接实现
│   ├── zhipu_model.py       # 智谱 AI 模型对接实现
│   ├── glm_model.py         # 本地 GLM 模型对接实现
│   └── deepseek_model.py    # DeepSeek 模型对接实现
├── utils/
│   ├── __init__.py          # 工具模块导出入口
│   └── logger.py            # 日志工具，统一输出日志格式，便于调试与排查
├── test/
│   └── test.pdf             # 测试用 PDF 文件，用于功能验证
├── translator/
│   ├── __init__.py          # 翻译模块导出入口，对外暴露核心翻译类
│   ├── pdf_parser.py        # PDF 解析器，负责提取文本、表格、分页处理
│   ├── pdf_translator.py    # PDF 翻译核心，调度解析、翻译、保存全流程
│   ├── writer.py            # 文档输出器，支持翻译结果导出为 PDF/Markdown/Docx
│   └── pdf_exceptions.py    # 自定义异常体系：页码越界、文件损坏、翻译失败、API 错误
├── main.py                  # 项目命令行入口，启动翻译任务
├── README.md                # 项目说明文档
└── requirements.txt         # 项目依赖清单，一键安装环境


## 开始使用

### 环境准备
1.AIPdfLingo翻译器 需要 Python 3.6 或更高版本。使用 `pip install -r requirements.txt` 安装依赖项。

### 配置说明

1. 仓库仅提供配置模板：`config.example.yaml`
2. 本地复制一份：
   cp config.example.yaml config.yaml
3. 自行在 `config.yaml` 中填入你的各类 API Key
4. **请勿将含真实密钥的 config.yaml 上传到代码仓库**
5. 本项目已通过 `.gitignore` 自动忽略真实配置文件

### 翻译文件

1.使用命令行 python main.py
2.根据提示输入需要翻译的文档名称
