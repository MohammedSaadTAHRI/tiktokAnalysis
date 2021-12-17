import typing
from pathlib import Path
import sys

from TikTokApi import TikTokApi as tiktok
import pandas as pd

from helpers import process_results

VERIFYFP = "verify_kx4kdsbb_khM5LQbS_OyA4_4Cui_8IVh_bsvwV5ocdVHV"
api = tiktok.get_instance(custom_verifyFp=VERIFYFP, count=2000, use_test_endpoints=True)
RETRY_LIMIT = 10


def get_data(hashtag: str, path_to_save: typing.Union[str, Path]) -> None:
    """This functions connects the API to get the data, formats and transforms the data into a csv."""
    got_data = False
    for _ in range(RETRY_LIMIT):
        if got_data:
            break
        try:
            trending = api.by_hashtag(hashtag)
            got_data = True
        except Exception:
            pass
    if not got_data:
        raise Exception("Exceed the retry limit count., could not get the data.")
    flattened_data = process_results(trending)
    df = pd.DataFrame.from_dict(flattened_data, orient="index")
    print(df.head())
    df.to_csv(path_to_save, index=False)


if __name__ == "__main__":
    get_data(sys.argv[1], sys.argv[2])
