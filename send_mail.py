import smtplib
import csv
import time
import os  # 新增：用于读取环境变量
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# ================= 配置区域 =================
# 敏感信息改为从环境变量读取
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get('MY_EMAIL')        # 从 GitHub Secrets 读取
SENDER_PASSWORD = os.environ.get('MY_PASSWORD')  # 从 GitHub Secrets 读取

EMAIL_SUBJECT = '【邀请】Level Up Your Stream: Get Your AI Co-Host Free for 7 Days!'
CSV_FILE = 'streamers.csv'
HTML_TEMPLATE = 'template.html'
# ===========================================

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def send_invitations():
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("错误: 未找到邮箱或密码的环境变量配置！")
        return

    try:
        html_content = read_template(HTML_TEMPLATE)
    except FileNotFoundError:
        print(f"错误: 找不到模板文件 {HTML_TEMPLATE}")
        return

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(">>> 成功连接到邮件服务器")
    except Exception as e:
        print(f"无法连接服务器: {e}")
        return

    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                name = row['Name'] # 确保 CSV 表头是 Name
                email = row['Email'] # 确保 CSV 表头是 Email

                if not email:
                    continue

                print(f"正在发送给: {name} ({email})...")

                # 这里对应你 HTML 里的 {name}
                personalized_html = html_content.replace('{name}', name)

                msg = MIMEMultipart()
                msg['From'] = formataddr(("Eugene from Tatalala", SENDER_EMAIL))
                msg['To'] = email
                msg['Subject'] = EMAIL_SUBJECT

                msg.attach(MIMEText(personalized_html, 'html', 'utf-8'))

                try:
                    server.sendmail(SENDER_EMAIL, email, msg.as_string())
                    print(f"SUCCESS: 已发送给 {name}")
                except Exception as e:
                    print(f"FAILED: 发送给 {name} 失败. 原因: {e}")

                time.sleep(5) # 稍微延长一点间隔，更安全

    except FileNotFoundError:
        print(f"错误: 找不到 CSV 文件 {CSV_FILE}")
    finally:
        try:
            server.quit()
        except:
            pass
        print(">>> 任务结束")

if __name__ == '__main__':
    send_invitations()
