# AI Sales Automation（集客 → リード獲得 → 自動フォロー → 販売）

OpenAI APIを使い、以下を自動化するシステムです。

1. **集客**: SNS投稿・ブログ記事をAIが自動生成（`generate_content.py`）
2. **リード獲得**: フォーム送信されたリード情報を蓄積・スコアリング（`lead_scorer.py`）
3. **販売（自動フォロー）**: スコアに応じてAIが個別最適化したフォローメールを自動生成・送信（`nurture_email.py`）
4. **GitHub Actionsで完全自動化**（毎日決まった時間に自動実行、サーバー不要）

## セットアップ

1. このリポジトリをGitHubにpush
2. GitHubの `Settings > Secrets and variables > Actions` に以下を登録
   - `OPENAI_API_KEY` : OpenAIのAPIキー
   - `SMTP_USER` / `SMTP_PASS` : メール送信用（Gmailなら[アプリパスワード](https://myaccount.google.com/apppasswords)）
   - `SMTP_HOST` (例: smtp.gmail.com) / `SMTP_PORT` (例: 587)
3. `data/leads.csv` に見込み客情報を追加していく（名前, メール, 興味関心, ステータス）
4. `.github/workflows/automation.yml` によって毎日自動実行されます（手動実行も可能）

## ローカルで試す場合

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-xxxx
python src/generate_content.py
python src/lead_scorer.py
python src/nurture_email.py
