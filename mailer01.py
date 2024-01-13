import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import csv
import ssl  # SSLのために追加
import my_gmail_account as gmail

load_dotenv()

class Mailer:
    def __init__(self, addr_to, subject, body):
        self.password = os.getenv('PASSWORD')
        self.addr_from = os.getenv('EMAIL')
        self.addr_to = addr_to
        self.charset = "UTF-8"
        self.subject = subject
        self.body = body

    def send(self):
        msg = MIMEText(self.body, 'plain', self.charset)
        msg['Subject'] = self.subject
        msg['From'] = self.addr_from
        msg['To'] = self.addr_to

        try:
            # SSLコンテキストを使用してセキュアなSMTP接続を作成
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.set_debuglevel(1)  # デバッグ情報を表示
                smtp.login(self.addr_from, self.password)
                # smtp.login(gmail.account, gmail.password)
                smtp.send_message(msg)
        except Exception as e:
            print(f"メール送信中にエラーが発生しました: {e}")

def create_mail_body(company, title, full_name):
    body = f"""
    {company}
    {title}
    {full_name}様

    お世話になっております。C-mindの柿です。
    こちらのメールはPythonによるGmailのテスト送信になります。

    よろしくお願いいたします。

    -----------------------
    パイソン 太郎
    株式会社Test
    Engineer
    Email: {os.getenv('EMAIL')}
    """
    return body

filename = './test01.csv'

with open(filename, 'r', encoding='shift_jis') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダー行を読み飛ばす

    for row in reader:
        if len(row) != 4:
            print(f"エラー: 予期しないフォーマットの行 - {row}")
            continue  # 次の行に進む

        company, title, full_name, email = row  # 新しいカラムに合わせて変更
        print(f"会社名: {company}, 役職名: {title}, 名前: {full_name}, メール: {email}")

        # メール送信の処理...
        addr_to = email.strip()
        subject = "Pythonによるテストメール"
        body = create_mail_body(company.strip(), title.strip(), full_name.strip())
        mailer = Mailer(addr_to, subject, body)
        mailer.send()
