from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
import time
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def weather_index():
    """ メインページの解析 """
    url_main = "https://www.jma.go.jp/jp/yoho/318.html"
    res = requests.get(url_main)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    # table.forecastタグ取得
    table_forecast = soup.select("table.forecast")[0]

    # img_titleと天気画像の辞書
    weather_img = {
        "晴れ時々曇り": "static/img/101.png",
        "晴れ": "static/img/100.png",
        "晴れ後曇り": "static/img/101.png",
        "曇り": "static/img/200.png",
        "晴れ一時雨": "static/img/102.png",
        "曇り一時雨": "static/img/212.png",
        "曇り後雨": "static/img/212.png",
        "曇り後晴れ": "static/img/201.png",
        "雨後曇り": "static/img/313.png",
        "曇り時々晴れ": "static/img/201.png",
        "雨": "static/img/300.png",
        "雪": "static/img/400.png",
        "晴れ後一時雨": "static/img/102.png",
        "曇り後一時雨": "static/img/212.png",
        "曇り時々雨": "static/img/212.png",
        "晴れ時々雨": "static/img/102.png"
    }
    count = 0  # カウント変数
    # trタグ取得
    for tr in table_forecast.select("tr"):
        rain_per_list = []
        # weatherタグ取得＆空白タグループスキップ
        weather = tr.select("th.weather")
        if not weather:
            continue
        # 北東部の今日のみ表示（countで調整）
        count += 1
        if count >= 2:
            break
        # weather内部
        weather = weather[0]
        weather_text = weather.text.strip()
        img = weather.find("img")
        img_title = img["title"]
        # 降水確率取得
        for rain_per in tr.select("td[align='right']"):
            rain_per_list.append(rain_per.text.strip())
        rain_per_0_6 = rain_per_list[0]
        rain_per_6_12 = rain_per_list[1]
        rain_per_12_18 = rain_per_list[2]
        rain_per_18_24 = rain_per_list[3]

    # 表示する天気図を決める
    weather_top_img = weather_img[img_title]

    """ 最低気温ページの解析 """
    time.sleep(1)
    url_min = "https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mntemsad00.html#a11"
    res = requests.get(url_min)
    res.encoding = res.apparent_encoding

    soup = BeautifulSoup(res.text, "html.parser")

    # tr.mtxタグ取得
    for tr_mtx in soup.select("tr.mtx"):
        # 千葉市中央区を含むtr.mtxタグのみに絞り、最低気温取得
        if tr_mtx.find_all('td', style='white-space:nowrap', string='千葉市中央区'):
            tem_min = tr_mtx.select('td[style="text-align:right;white-space:nowrap;"]')[0].text.strip()
            tem_min = tem_min.replace(" ]", "")
            tem_min = tem_min.replace(")", "")
    
    """ 最高気温ページの解析 """
    time.sleep(1)
    url_max = "https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsad00.html#a45"
    res = requests.get(url_max)
    res.encoding = res.apparent_encoding

    soup = BeautifulSoup(res.text, "html.parser")

    # tr.mtxタグ取得
    for tr_mtx in soup.select("tr.mtx"):
        # 千葉市中央区を含むtr.mtxタグのみに絞り、最高気温取得
        if tr_mtx.find_all('td', style='white-space:nowrap', string='千葉市中央区'):
            tem_max = tr_mtx.select('td[style="text-align:right;white-space:nowrap;"]')[0].text.strip()
            tem_max = tem_max.replace(" ]", "")
            tem_max = tem_max.replace(")", "")

    # 表示するおすすめの服装を決める
    fashion_dic = {
        "-7": ("static/img/samui_man1.png",
               "ちょー寒い！",
               "マフラーを2つ付けよう！"),
        "7-13": ("static/img/samui_man2.png",
                 "少し肌寒いなぁ",
                 "厚めのアウターの時期！"),
        "13-20": ("static/img/nagasode_man.png",
                  "過ごしやすくてハッピー!",
                  "春、秋の服装がいいかも"),
        "20-25": ("static/img/summer_man.png",
                  "少し暑くなってきたかも～",
                  "夏服を着よう！"),
        "25-": ("static/img/atsui_man.png",
                "死ぬほど暑い...",
                "熱中症に気を付けよう！")
    }
    temp_ave = (float(tem_max) + float(tem_min)) / 2
    if temp_ave <= 7:
        fashion_img, fashion_text1, fashion_text2 = fashion_dic["-7"]
    elif 7 < temp_ave <= 13:
        fashion_img, fashion_text1, fashion_text2 = fashion_dic["7-13"]
    elif 13 < temp_ave <= 20:
        fashion_img, fashion_text1, fashion_text2 = fashion_dic["13-20"]
    elif 20 < temp_ave <= 25:
        fashion_img, fashion_text1, fashion_text2 = fashion_dic["20-25"]
    elif temp_ave > 25:
        fashion_img, fashion_text1, fashion_text2 = fashion_dic["25-"]

    """スクレイピング時間取得"""
    now = datetime.now()
    now_day = now.strftime("%Y/%m/%d")
    now_min = now.strftime("%H:%M")
    get_time = "（" + now_day + " " + now_min + " " + "取得）"

    return render_template("weather_today.html",
                           weather_img=weather_top_img,
                           img_title=img_title,
                           weather_text=weather_text,
                           tem_min=tem_min,
                           tem_max=tem_max,
                           rain_0_6=rain_per_0_6,
                           rain_6_12=rain_per_6_12,
                           rain_12_18=rain_per_12_18,
                           rain_18_24=rain_per_18_24,
                           fashion_img=fashion_img,
                           fashion_text1=fashion_text1,
                           fashion_text2=fashion_text2,
                           get_time=get_time
                           )


if __name__ == '__main__':
    app.run()
