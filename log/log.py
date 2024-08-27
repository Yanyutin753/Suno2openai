import asyncio
import json
import os

import aiofiles

from util.config import DATA_PATH
from util.logger import logger

# 数据文件路径
file_path = DATA_PATH + '/data.txt'
# 创建一个锁，用于保证数据一致性
write_lock = asyncio.Lock()


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
async def add_message_file(new_data):
    async with write_lock:
        try:
            async with aiofiles.open(file_path, 'a', encoding='utf-8') as file:
                json_string = json.dumps(new_data, ensure_ascii=False)
                await file.write(json_string + '\n')
                logger.info("新的JSON数据已成功追加到文件中。")
        except Exception as e:
            logger.error(f"写入文件时出错: {e}")

# test
# async def main():
#     new_data1 = {"key1": "value1"}
#     new_data2 = {"key2": "value2"}
#
#     # 异步地添加 JSON 数据
#     await asyncio.gather(
#         add_message_file(new_data1),
#         add_message_file(new_data2)
#     )
#
#
# # 如果你在一个脚本中执行，可以使用以下代码来运行异步主函数
# if __name__ == "__main__":
#     asyncio.run(main())
