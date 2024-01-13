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

# 以下は以前のコードと変わらず...

def create_mail_body(full_name):
    body = f"""
    {full_name}様

    お世話になっております。C-mindの柿です。
    ことらのメールはPythonによるGmailのテスト送信になります。

    よろしくお願いいたします。

    -----------------------
    パイソン 太郎
    株式会社Test
    Engineer
    Email: {os.getenv('EMAIL')}
    """
    return body

filename = './test.csv'


# with open(filename, 'r', encoding='utf-8') as f:  # エンコーディングを指定
with open(filename, 'r', encoding='shift_jis') as f:  # または使用しているエンコーディングに応じて変更
    reader = csv.reader(f, delimiter='\t')  # タブ区切りを指定
    header = next(reader)  # ヘッダー行を読み飛ばす

    for row in reader:
        print(row)  # デバッグ用：読み込まれた行を表示
        if len(row) < 2:  # 行に少なくとも2つの要素があるか確認
            continue  # 要素が不足している場合は、次の行に進む

        full_name = row[0]
        email = row[1]
        addr_to = email
        subject = "Pythonによるテストメール"
        body = create_mail_body(full_name)
        mailer = Mailer(addr_to, subject, body)
        mailer.send()
