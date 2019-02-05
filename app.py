from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
from temp import tem_min, tem_max  # ファイルから変数のimport

"""
スクレイピング
"""
# URLの取得
url_chiba = "https://www.jma.go.jp/jp/yoho/318.html"
res = requests.get(url_chiba)
res.encoding = res.apparent_encoding

soup = BeautifulSoup(res.text, "html.parser")

# table.forecastタグ取得
table_forecast = soup.select("table.forecast")[0]

# img_titleと天気画像の辞書
weather_img = {
    "晴れ時々曇り": "static/img/101.png",
    "晴れ": "static/img/100.png",
    "晴れ後曇り": "static/img/707.png",
    "曇り": "static/img/200.png",
    "晴れ一時雨": "static/img/102.png",
    "曇り一時雨": "static/img/212.png",
    "曇り後雨": "static/img/212.png",
    "雨後曇り": "static/img/313.png",
    "曇り時々晴れ": "static/img/201.png",
    "雨": "static/img/300.png",
    "雪": "static/img/400.png"
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


"""
Flaskの部分
"""
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("weather_today.html",
                           weather_img=weather_top_img,
                           img_title=img_title,
                           weather=weather_text,
                           tem_min=tem_min,
                           tem_max=tem_max,
                           rain_0_6=rain_per_0_6,
                           rain_6_12=rain_per_6_12,
                           rain_12_18=rain_per_12_18,
                           rain_18_24=rain_per_18_24,
                           fashion_img=fashion_img,
                           fashion_text1=fashion_text1,
                           fashion_text2=fashion_text2
                           )


if __name__ == '__main__':
    app.run()
