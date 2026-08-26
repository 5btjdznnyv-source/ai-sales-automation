"""
③販売フォローメール自動送信
status が 'hot' のリードに対して、AIが一人ひとりに合わせた
フォロー（クロージング）メールを生成し、自動送信する。
"""
import os
import smtplib
from email.mime.text import MIMEText
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

LEADS_PATH = "data/leads.csv"
OFFER = "AI自動集客・販売システムの個別コンサル（初回無料相談）"

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")


def generate_email(name: str, interest: str) -> str:
    prompt = f"""
あなたは信頼される営業パーソンです。以下の見込み客に向けて、
売り込み感を出さず、相手のメリットを中心にした
フォローメール本文を日本語で書いてください。

宛名: {name} 様
相手の興味関心: {interest}
案内したいオファー: {OFFER}

# 条件
- 300文字前後
- 冒頭で相手の興味に共感する一文
- 最後に軽いCTA（無料相談の日程調整リンクを想定した一文）を入れる
- 署名は「AI自動化サポートチーム」とする
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    return res.choices[0].message.content


def send_email(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASS:
        print(f"[DRY-RUN] {to_email} 宛メール（SMTP未設定のため送信スキップ）\n{body}\n")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(f"✅ 送信完了: {to_email}")


def main():
    df = pd.read_csv(LEADS_PATH)
    hot_leads = df[df["status"] == "hot"]

    for _, row in hot_leads.iterrows():
        body = generate_email(row["name"], row["interest"])
        send_email(row["email"], "【ご案内】あなたに合った自動化のご提案", body)

    print(f"対象リード数: {len(hot_leads)}")

if __name__ == "__main__":
    main()
