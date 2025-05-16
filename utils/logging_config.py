import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s - %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
