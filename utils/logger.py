from loguru import logger # 基于Python原生logging模块，使用loguru库增强功能
import os
import sys

LOG_FILE = "translation.log" #日志文件前缀为"translation_log"
ROTATION_TIME = "02:00" # 每2小时轮转日志文件（凌晨2点生成新文件）

class Logger:
    def __init__(self, name="translation", log_dir="logs", debug=False):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        # Remove default loguru handler
        logger.remove()

        # 开发模式默认级别为DEBUG，生产环境可设置为WARNING级别
        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG")
        self.logger = logger

LOG = Logger(debug=True).logger

if __name__ == "__main__":
    log = Logger().logger

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
