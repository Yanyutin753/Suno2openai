import json
import os
import threading

from util.config import DATA_PATH
from util.logger import logger

# 数据文件路径
file_path = DATA_PATH + '/data.txt'
# 创建一个同步锁
write_lock = threading.Lock()


# 初始化JSON文件
def initialize_json_file():
    # 检查文件是否存在
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            logger.info(f"文件 {file_path} 已存在且包含数据，跳过初始化。")
            return
        else:
            logger.info(f"文件 {file_path} 已存在但为空，进行初始化。")
    else:
        logger.info(f"文件 {file_path} 不存在，创建新文件。")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('')
    logger.info(f"文件 {file_path} 已初始化。")


# 添加json数据
def add_message_file(new_data):
    try:
        with write_lock:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    json_string = json.dumps(new_data, ensure_ascii=False)
                    file.write(json_string + '\n')
                    logger.info("新的JSON数据已成功追加到文件中")
            except Exception as e:
                logger.error(f"写入文件时出错: {e}")
    except Exception as e:
        logger.error(f"写入文件时出错: {e}")
