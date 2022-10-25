# ※現在サーバーは停止しているため、webサイトの閲覧はできません。
# weather （プロジェクト名）
# 千葉県北西部の天気を表示するwebサイト
・目的：スクレイピングの練習、フレームワークを用いたwebサイト構築の練習

気象庁の千葉県の天気予報ページからpythonのスクレイピングを用いて、天気情報を抽出しています。  
@天気情報：　https://www.jma.go.jp/jma/index.html  
@気温情報：　https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsad00.html  

抽出したデータはpythonのwebフレームワーク「Flask」を用いて、webサイトとして表示しています。  
※現在情報を得るために、HTTPリクエスト時にスクレイピング処理が行われるので、サイトを開くのに10~20秒程度かかります。  
@webサイトのURL:  https://yakisoba88-weather.herokuapp.com/


サーバーはHerokuを用いました。

# ディレクトリ構成
```
weather/
├─ .idea
├─ static/
│    ├─ img                   # 画像フォルダ
│    └─ weather.css           # CSSファイル
├─ templates/
│    └─ weather_today.html    # HTMLファイル
├─ .gitignore                 
├─ Procfile                   # Heroku用ファイル（アプリのプロセス宣言ファイル）
├─ requirements.txt           # Heroku用ファイル（ライブラリ一覧）
├─ README.md
└─ app.py                     # Flaskのアプリファイル＆スクレイピング

.ideaフォルダはプロジェクト生成時に作られる自動設定フォルダです。
```
