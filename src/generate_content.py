"""
①集客コンテンツ自動生成
SNS投稿文・ブログ記事のネタをAIで自動生成し、data/generated_content.md に保存する。
GitHub Actionsで毎日実行すれば、ネタ切れせずに集客コンテンツを量産できる。
"""
import os
import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ▼ここを自分の商品・サービスに書き換える
TOPIC = "AIを使った副業・自動化ノウハウ"
OFFER = "AI自動集客・販売システムの個別コンサル"

PROMPT = f"""
あなたは敏腕マーケターです。以下のテーマで、SNS(X/Instagram)投稿用の
バズりやすい投稿文を3パターンと、ブログ記事の見出し構成を1つ作成してください。

テーマ: {TOPIC}
最終的に誘導したいオファー: {OFFER}

# 出力条件
- 投稿文は120文字以内、フックの強い1行目から始める
- 絵文字は控えめに1-2個
- 最後に{OFFER}へ自然に誘導する一文を入れる
- ブログ見出しはSEOを意識したH2を5つ
"""

def main():
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.9,
    )
    content = res.choices[0].message.content
    today = datetime.date.today().isoformat()

    os.makedirs("data", exist_ok=True)
    with open("data/generated_content.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n---\n## {today}\n{content}\n")

    print("✅ コンテンツ生成完了:", today)

if __name__ == "__main__":
    main()
