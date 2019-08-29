from config import crawler_info,crawler_debug
import logging
crawler_info.setLevel(logging.DEBUG)
for item in range(10):
    crawler_info.info("there is {}".format(item))
