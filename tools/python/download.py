"""Download a CSV file of KdB data.
"""
from typing import Optional, TypedDict

import argparse
import requests


class PostDict(TypedDict):
    """Dict for requesting with POST to KdB.
    """
    index: str
    locale: str
    nendo: int
    termCode: str
    dayCode: str
    periodCode: str
    campusCode: str
    hierarchy1: str
    hierarchy2: str
    hierarchy3: str
    hierarchy4: str
    hierarchy5: str
    freeWord: str
    _orFlg: int
    _andFlg: int
    _gaiyoFlg: int
    _risyuFlg: int
    _excludeFukaikoFlg: int
    _eventId: Optional[str]
    outputFormat: Optional[int]


class KdbDownloader():
    """Download a CSV file of KdB data.
    """

    def __init__(self, year: int = 2023) -> None:
        """Initializer.

        Args:
            year (int, optional): A year of syllabus. Defaults to 2023.
        """
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH"
        self.year = year
        self.post: PostDict = {
            "index": "",
            "locale": "",
            "nendo": year,
            "termCode": "",
            "dayCode": "",
            "periodCode": "",
            "campusCode": "",
            "hierarchy1": "",
            "hierarchy2": "",
            "hierarchy3": "",
            "hierarchy4": "",
            "hierarchy5": "",
            "freeWord": "",
            "_orFlg": 1,
            "_andFlg": 1,
            "_gaiyoFlg": 1,
            "_risyuFlg": 1,
            "_excludeFukaikoFlg": 1,
            "_eventId": None,
            "outputFormat": None
        }

    def get_post(self) -> PostDict:
        """Get a copy of PostDict.

        Returns:
            PostDict: An Dict for requesting with POST to KdB.
        """
        return self.post.copy()

    def download(self, filename: str) -> None:
        """Download KdB data.

        Args:
            filename (str): A save file path.
        """
        self.__download()
        open(filename, "w", encoding="utf-8").write(self.response_text)

    def __download(self) -> None:
        """Helper for downloading.
        """
        self.__start_session()
        self.__search_kdb()
        self.__download_csv()

    def __start_session(self) -> None:
        """Helper for starting session to KdB.
        """
        kdb_url = "https://kdb.tsukuba.ac.jp/"
        self.session = requests.session()
        self.response = self.session.get(kdb_url)
        if self.response.status_code != 200:
            raise ValueError('System failure on KdB.')

    def __search_kdb(self) -> None:
        """Helper for searching.
        """
        search_post = self.get_post()
        search_post["_eventId"] = "searchOpeningCourse"
        self.response = self.session.post(self.response.url, data=search_post)
        self.do_url = self.response.url

    def __download_csv(self) -> None:
        """Helper for downloading CSV.
        """
        csv_post = self.get_post()
        csv_post["_eventId"] = "output"
        csv_post["outputFormat"] = 0
        res = self.session.post(self.do_url, data=csv_post).text
        if len(res) == 0:
            raise ValueError('Response text is empty.')
        elif 'sys-err-head' in res:
            raise ValueError('System failure on KdB.')
        else:
            self.response_text = res


def main() -> None:
    """Main.
    """
    import datetime
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="the output directory")
    args = parser.parse_args()

    date = datetime.datetime.now()
    filename = "%s/kdb-%04d%02d%02d.csv" % (args.output_dir,
                                            date.year, date.month, date.day)

    os.makedirs(args.output_dir, exist_ok=True)
    KdbDownloader().download(filename)


if __name__ == '__main__':
    main()
