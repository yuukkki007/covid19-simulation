import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
sh.setFormatter(sh_formatter)

logger.addHandler(sh)
