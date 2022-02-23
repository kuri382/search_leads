import csv
import re
from glob import glob

import chromedriver_binary
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

INPUT_DATA = "data/input.csv"
OUTPUT_DATA = "data/output.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}


def get_html(url, params=None):
    """get_html
    url: データを取得するサイトのURL
    [params]: 検索サイトのパラメーター {x: param}
    """
    try:
        # データ取得
        resp = requests.get(url, params=params, headers=headers)
        # 要素の抽出
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup
    except Exception as e:
        return None


def export_csv(data):
    output = open(OUTPUT_DATA, mode="a", newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(data)
    output.close()


def parse_search_list(tags, result, word):
    # 保存するファイル名を初期化
    file_number = 1
    title_lists = []
    url_lists = []
    for tag in tags:
        # 記事タイトルを取得
        current_title = tag.get_text()  # urlのhref以下を取得
        # current_title = soup.find('div', class_="uEierd")
        url = tag.get("href")  # 実行中の記事タイトル，URLを表示
        try:
            span = tag.get("span")
        except Exception as e:
            print(e)

        # csv出力
        output_list = [word, result, str(file_number), str(current_title), str(url)]
        export_csv(output_list)

        # ファイル名の繰り上げ
        file_number += 1
        title_lists.append(current_title)
        url_lists.append(url)


def google_search(word):
    # search_url = "https://www.google.co.jp/search" # google検索
    search_url = "https://www.google.co.jp/search?hl=ja&num=20&q"  # google検索
    search_params = {"q": word}
    soup = get_html(search_url, search_params)  # データ取得

    return soup, search_url


def search_rankings(word):
    """
    検索順位の表示
    """
    soup = google_search(word)

    tags = soup.select(".yuRUbf > a")  # クラスを指定し，aタグのもののみ抽出
    tags_ad = soup.select(".Krnil")  # 広告用css

    # tags_ad = soup.select(".uEierd > a") # 広告用css
    tags_ad_url = soup.select(".Zu0yb.LWAWHf.OSrXXb.qzEoUe")
    result_stats = soup.find("div", id="result-stats")

    print("organic_search")
    parse_search_list(tags, "organic", word)
    print("listing ads")
    parse_search_list(tags_ad, "ad", word)


def search_leads(word):
    """
    リード一覧から売上を検索する
    """
    info_company = word + " 売上"
    soup, search_url = google_search(info_company)
    tags = soup.select(".yuRUbf > a")  # クラスを指定し，aタグのもののみ抽出
    info_revenue = soup.find("div", class_="Z0LcW")

    pattern = "<div.*?>(.*?)</div>"

    
    if info_revenue is not None:
        results = re.findall(pattern, str(info_revenue), re.S)
    else:
        results = ["no data"]

    print(results[0])

    title_lists = []
    url_lists = []

    tag = tags[0]
    # 記事タイトルを取得
    current_title = tag.get_text()  # urlのhref以下を取得
    # current_title = soup.find('div', class_="uEierd")
    url = tag.get("href")  # 実行中の記事タイトル，URLを表示
    try:
        span = tag.get("span")
    except Exception as e:
        print(e)

    # csv出力
    output_list = [info_company, results[0], str(current_title), str(url)]

    output = open(OUTPUT_DATA, mode="a", newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(output_list)
    output.close()

    # ファイル名の繰り上げ
    file_number += 1
    title_lists.append(current_title)
    url_lists.append(url)


def main():
    with open(INPUT_DATA) as input:
        reader = csv.reader(input)
        for word in reader:
            print(word[0])
            # search_rankings(word[0]) #検索順位を表示する
            search_leads(word[0])
    print("csv file has exported")


main()
