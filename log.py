import logging

def setup_logger():
    # 创建logger对象
    logger = logging.getLogger('bili_login')
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 创建formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S')

    # 创建文件处理器并设置级别和格式
    file_handler = logging.FileHandler('debug.log', encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # 文件记录所有DEBUG及以上级别的日志
    file_handler.setFormatter(formatter)

    # 将处理器添加到logger
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()