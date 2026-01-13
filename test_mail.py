import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# ================= 测试配置 =================
# 这里的配置和你主脚本一样，确保测试环境一致
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get('MY_EMAIL')
SENDER_PASSWORD = os.environ.get('MY_PASSWORD')

HTML_TEMPLATE = 'template.html'

# === 测试收件人信息 ===
TEST_TARGET_NAME = "Eugene"
TEST_TARGET_EMAIL = "islandofkurlandi@gmail.com" # 请确认邮箱后缀是否正确
# ===========================================

def read_template(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: 找不到模板文件 {filename}")
        return None

def send_test_email():
    print(f">>> 开始测试脚本...")
    print(f">>> 目标收件人: {TEST_TARGET_NAME} <{TEST_TARGET_EMAIL}>")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: 环境变量未读取到，请检查 Secrets 配置！")
        return

    # 1. 读取模板
    html_content = read_template(HTML_TEMPLATE)
    if not html_content:
        return

    # 2. 连接服务器
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(">>> 服务器连接成功 (Login Success)")
    except Exception as e:
        print(f"!!! 服务器连接失败: {e}")
        return

    # 3. 发送邮件
    try:
        # 替换名字
        personalized_html = html_content.replace('{name}', TEST_TARGET_NAME)

        msg = MIMEMultipart()
        msg['From'] = formataddr(("Eugene from Tatalala (Test)", SENDER_EMAIL)) #以此区分是测试邮件
        msg['To'] = TEST_TARGET_EMAIL
        msg['Subject'] = '【TEST】Testing Email Script Configuration'

        msg.attach(MIMEText(personalized_html, 'html', 'utf-8'))

        server.sendmail(SENDER_EMAIL, TEST_TARGET_EMAIL, msg.as_string())
        print(f">>> 测试邮件已发送给 {TEST_TARGET_EMAIL}")
        print(">>> 测试成功！环境配置正常。")

    except Exception as e:
        print(f"!!! 发送过程中出错: {e}")
    finally:
        server.quit()

if __name__ == '__main__':
    send_test_email()
