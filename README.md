# weather （プロジェクト名）
# 千葉県北東部の天気を表示するwebサイト
・目的：スクレイピングの練習、フレームワークを用いたwebサイト構築の練習

気象庁の千葉県の天気予報ページからpythonのスクレイピングを用いて、天気情報を抽出しています。(https://www.jma.go.jp/jma/index.html)  
抽出したデータはpythonのwebフレームワーク「Flask」を用いて、webサイトとして表示しています。  
@webサイトのURL:

サーバーはHerokuを用いました。

# ディレクトリ構成
```
weather/
├─ .idea
├─ __pycache__
├─ static/
│    ├─ img                   # 画像フォルダ
│    └─ weather.css           # CSSファイル
├─ templates/
│    └─ weather_today.html    # HTMLファイル
├─ app.py                     # Flaskのアプリファイル＆メインスクレイピング
└─ temp.py                    # 最高、最低気温のスクレイピング

.ideaフォルダはプロジェクト生成時に作られる自動設定フォルダです。
.__pycache__フォルダは自前のpythonファイル(temp.py)をapp.pyにimportした際の自動生成フォルダです。
temp.pyではapp.pyのスクレイピングページとは異なるページからスクレイピングを行っているのでファイルを分けました。
(URL:https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsad00.html)
```
