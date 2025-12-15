from flask import Flask, request, jsonify
import datetime as dt
import json
import requests
import xml.etree.ElementTree as ET
from google import genai
from google.genai import types
from flask_cors import CORS

API_KEY = "YOUR_GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

# RSS一覧
RSS_LIST = {
    "top": [
        "https://www.nhk.or.jp/rss/news/cat0.xml",
    ],
    "business": [
        "https://news.yahoo.co.jp/rss/topics/business.xml",
    ],
    "world": [
        "https://www3.nhk.or.jp/rss/news/cat6.xml",
    ]
}

# User-Agent（Yahoo対策）
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_topics(rss_url):
    topics = []

    try:
        res = requests.get(rss_url, headers=HEADERS, timeout=5)

        if res.status_code != 200:
            return []

        root = ET.fromstring(res.text)

        for item in root.findall(".//item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            description = item.findtext("description", "")
            pub_date = item.findtext("pubDate", "")

            try:
                pub_date = dt.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
            except:
                pub_date = dt.datetime.now()

            topics.append({
                "title": title,
                "link": link,
                "description": description,
                "pub_date": pub_date.isoformat()
            })

    except Exception as e:
        print("RSS ERROR:", e)

    return topics

# Geminiタグ付け（改良版）
# 構造化出力版タグ付け：絶対 JSON が返る
def tag_topic(content):
    try:
        TAG_LIST = [
            "政治", "経済", "国際", "ビジネス", "IT", "科学",
            "スポーツ", "社会", "エンタメ", "環境", "金融",
            "災害", "医療", "軍事", "その他"
        ]

        prompt = f"""
        以下の記事内容に関連するタグを、次の中から最大3つ選び、
        JSON配列として返してください。

        {TAG_LIST}

        出力例:
        ["政治","経済"]

        記事内容:
        {content}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=64,
                temperature=0.2,
                response_mime_type="application/json"  # ←これが重要！
            ),
        )

        print("RAW TAG RESPONSE:", response.text)

        return json.loads(response.text)

    except Exception as e:
        print("TAG ERROR:", e)
        return ["その他"]





@app.route("/news")
def news_api():
    category = request.args.get("category", "top")

    if category not in RSS_LIST:
        return jsonify({"error": "invalid category"}), 400

    all_news = []
    for url in RSS_LIST[category]:
        all_news.extend(get_topics(url))

    all_news.sort(key=lambda x: x["pub_date"], reverse=True)
    all_news = all_news[:10]

    for n in all_news:
        n["tags"] = tag_topic(n["title"] + " " + n["description"])

    return jsonify(all_news)


if __name__ == "__main__":
    app.run(debug=True)


