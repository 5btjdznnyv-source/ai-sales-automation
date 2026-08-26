"""
②リードスコアリング
data/leads.csv の各リードを興味関心・接触状況からスコアリングし、
一定以上を 'hot'（今すぐ販売アプローチすべき客）に自動昇格させる。
"""
import pandas as pd
import os

LEADS_PATH = "data/leads.csv"

# 興味関心キーワードごとの重み（自分の商材に合わせて調整）
INTEREST_WEIGHT = {
    "商品比較": 3,
    "コンサル相談": 3,
    "オンライン講座": 2,
}

STATUS_WEIGHT = {
    "new": 1,
    "contacted": 2,
    "hot": 3,
}

def score_row(row):
    score = INTEREST_WEIGHT.get(row["interest"], 1)
    score += STATUS_WEIGHT.get(row["status"], 0)
    return score

def main():
    if not os.path.exists(LEADS_PATH):
        print("leads.csv が見つかりません")
        return

    df = pd.read_csv(LEADS_PATH)
    df["score"] = df.apply(score_row, axis=1)

    # スコア4以上は自動的に hot（=今すぐ販売フォローすべき）にする
    df.loc[df["score"] >= 4, "status"] = "hot"

    df.to_csv(LEADS_PATH, index=False)
    print("✅ スコアリング完了")
    print(df[["name", "interest", "status", "score"]])

if __name__ == "__main__":
    main()
