from bs4 import BeautifulSoup
import requests
import time


"""
千葉市中央区（北西部）の最低＆最高気温取得
"""
# URL
url_min = "https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mntemsad00.html#a11"
url_max = "https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsad00.html#a45"

""" 最低気温の取得 """
res = requests.get(url_min)
res.encoding = res.apparent_encoding

soup = BeautifulSoup(res.text, "html.parser")

# tr.mtxタグ取得
for tr_mtx in soup.select("tr.mtx"):
    # 千葉市中央区を含むtr.mtxタグのみに絞り、最低気温取得
    if tr_mtx.find_all('td', style='white-space:nowrap', string='千葉市中央区'):
        tem_min = tr_mtx.select('td[style="text-align:right;white-space:nowrap;"]')[0].text.strip()
        tem_min = tem_min.replace(" ]", "")

# アクセス間隔を数秒あける
time.sleep(1)

""" 最高気温の取得 """
res = requests.get(url_max)
res.encoding = res.apparent_encoding

soup = BeautifulSoup(res.text, "html.parser")

# tr.mtxタグ取得
for tr_mtx in soup.select("tr.mtx"):
    # 千葉市中央区を含むtr.mtxタグのみに絞り、最高気温取得
    if tr_mtx.find_all('td', style='white-space:nowrap', string='千葉市中央区'):
        tem_max = tr_mtx.select('td[style="text-align:right;white-space:nowrap;"]')[0].text.strip()
        tem_max = tem_max.replace(" ]", "")




