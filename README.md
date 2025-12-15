・フロントエンド（index.html）

Vue.js（CDN版）を使用
カテゴリ選択（総合 / ビジネス / 国際）
カテゴリ変更時に API へリクエストを送信
取得したニュースを一覧表示

・バックエンド（res.py）

Flask による Web API
RSS フィードからニュースを取得
Google Gemini API を用いてニュース内容からタグを生成
JSON 形式でフロントエンドへ返却

・処理の流れ（カテゴリ変更 → 画面表示）

ユーザーがカテゴリ選択ボックスを変更
（v-model="category"）
@change="fetchNews" により fetchNews() が実行される
fetch() を使い、以下の URL にリクエストを送信
http://127.0.0.1:5000/news?category=選択カテゴリ
Flask（res.py）がカテゴリに対応した RSS を取得
各ニュースのタイトル・本文を Gemini API に送信
Gemini がニュース内容に応じたタグを生成
ニュースデータ（タイトル・本文・リンク・タグ）を JSON で返却
Vue.js が articles に代入し、画面に一覧表示される

・index.html の役割
category
→ 選択中のニュースカテゴリ（top / business / world）

fetchNews()
→ バックエンド API からニュースを取得する関数

mounted()
→ ページ表示時に自動でニュースを取得

・必要な環境
Python 3.10 以上
インターネット接続
Google Gemini API キー

・必要なライブラリのインストール
python -m pip install flask flask-cors requests google-generativeai
※ pip が使えない場合は必ず python -m pip を使用してください。

・APIキーの設定
res.py 内で Google Gemini API キーを設定します。
API_KEY = "あなたのAPIキー"
※ 実運用では環境変数の使用を推奨します。

・起動手順
① Flask（バックエンド）の起動
python res.py
以下が表示されれば成功です：
Running on http://127.0.0.1:5000

② フロントエンドの起動
方法1（簡単）
index.html をブラウザで直接開く

方法2（推奨）
python -m http.server

ブラウザで以下にアクセス：
http://localhost:8000/index.html

機能要件にある
カテゴリの変更に応じて、ニュース一覧の内容が動的に切り替わること。
ニュース一覧は最低10件以上表示し、リアルタイムの内容であること。
ニュース1つ1つに対して「Gemini API」が生成したタグが付与されていること。
ができていない
