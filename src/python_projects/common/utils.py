import logging

def setup_logger(name: str = "tracker_sim") -> logging.Logger:
    """
    配置并返回一个标准格式的日志记录器（Logger）。
    用于项目中统一格式输出，无 Emoji 字符。
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
