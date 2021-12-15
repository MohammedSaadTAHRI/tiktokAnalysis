import typing
from pathlib import Path

from TikTokApi import TikTokApi as tiktok
import pandas as pd

from tiktokanalysis.helpers import process_results

VERIFYFP = "verify_kx4kdsbb_khM5LQbS_OyA4_4Cui_8IVh_bsvwV5ocdVHV"


def get_data(hashtag: str, path_to_save: typing.Union[str, Path]):
    """This functions connects the API to get the data, formats and transforms the data into a csv."""
    api = tiktok.get_instance(custom_verifyFp=VERIFYFP, use_test_endpoints=True)
    trending = api.by_hashtag(hashtag)
    flattened_data = process_results(trending)
    df = pd.DataFrame.from_dict(flattened_data, orient="index")
    df.to_csv(path_to_save, index=False)
