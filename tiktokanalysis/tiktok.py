import typing
from pathlib import Path
import sys
import logging

from TikTokApi import TikTokApi as tiktok
import pandas as pd

from helpers import process_results

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler('logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

VERIFYFP = "verify_kx4kdsbb_khM5LQbS_OyA4_4Cui_8IVh_bsvwV5ocdVHV"
try:
    API = tiktok.get_instance(custom_verifyFp=VERIFYFP, count=2000, use_test_endpoints=True)
except Exception:
    logger.exception("Failed the instanciate the tiktok API.")
    raise Exception("The program failed to connect to the API.")
RETRY_LIMIT = 10


def get_data(hashtag: str, path_to_save: typing.Union[str, Path]) -> None:
    """This functions connects the API to get the data, formats and transforms the data into a csv."""
    got_data = False
    for _ in range(RETRY_LIMIT):
        if got_data:
            break
        try:
            trending = API.by_hashtag(hashtag)
            got_data = True
        except Exception:
            pass
    if not got_data:
        logger.error("Exceed the retry limit count., could not get the data.")
        raise Exception("Exceed the retry limit count., could not get the data.")
    flattened_data = process_results(trending)
    df = pd.DataFrame.from_dict(flattened_data, orient="index")
    df.to_csv(path_to_save, index=False)
    logger.info("The data was successfully loaded and written to disk.")


if __name__ == "__main__":
    get_data(sys.argv[1], sys.argv[2])
