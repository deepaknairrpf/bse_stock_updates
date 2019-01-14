import requests
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import datetime
import csv
import pandas as pd

class EquityInfo:

    def __init__(self, code, name, group, type_abbr, open, high, low, close,
                 last, prev_close, no_of_trades, no_of_shares, net_turnov):
        self.code = code
        self.name = name
        self.group = group
        self.type = type_abbr
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.last = last
        self.prev_close = prev_close
        self.no_of_trades = no_of_trades
        self.no_of_shares = no_of_shares
        self.net_turnov = net_turnov


equity_info_list = []

class EquityDownloader:
    href_pattern = "/download/BhavCopy/Equity/EQ{0}_CSV.ZIP"

    @staticmethod
    def get_href_for_latest_equity_data():
        bse_page = requests.get("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
        soup = BeautifulSoup(bse_page.content, features="html.parser")
        href = soup.find(id="ContentPlaceHolder1_btnhylZip")['href']
        return href

    @staticmethod
    def get_zip_file_url_for_specific_date(date):
        date_format = date.strftime('%d%m%y')
        return __class__.href_pattern.format(date_format)

    @staticmethod
    def get_equity_data(date=None):

        if date is None:
            equity_data_zip_file_url = __class__.get_href_for_latest_equity_data()
        else:
            equity_data_zip_file_url = __class__.get_zip_file_url_for_specific_date(date)

        url = urllib.request.urlopen(equity_data_zip_file_url)

        with ZipFile(BytesIO(url.read())) as my_zip_file:
            for contained_file in my_zip_file.namelist():
                with my_zip_file.open(contained_file) as csv_file:
                    df = pd.read_csv(csv_file)
                    for idx, row in df.iterrows():
                        code = row['SC_CODE']
                        name = row['SC_NAME']
                        group = row['SC_GROUP']
                        type_abbr = row['SC_TYPE']
                        open = row['OPEN']
                        high = row['HIGH']
                        low = row['LOW']
                        close = row['CLOSE']
                        last = row['LAST']
                        prev_close = row['PREVCLOSE']
                        no_of_trades = row['NO_TRADES']
                        no_of_shares = row['NO_OF_SHRS']
                        net_turnov = row['NET_TURNOV']

                        equity_info = EquityInfo(code, name, group, type_abbr, open, high, low, close, last,
                                                 prev_close, no_of_trades, no_of_shares, net_turnov)
                        equity_info_list.append(equity_info)

        import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    print(EquityDownloader.get_equity_data())