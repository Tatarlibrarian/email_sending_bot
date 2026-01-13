import smtplib
import csv
import time
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# ================= 配置区域 =================
# Gmail 配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get('MY_EMAIL')
SENDER_PASSWORD = os.environ.get('MY_PASSWORD')

# 邮件内容配置
EMAIL_SUBJECT = 'Level Up Your Stream: Get Your AI Co-Host Free for 7 Days!'
CSV_FILE = 'streamers.csv'
HTML_TEMPLATE = 'template.html'

# === 发送策略配置 (针对 200 人名单优化) ===
BATCH_SIZE = 20         # 每发送 20 封邮件为一个批次
BATCH_PAUSE = 600       # 每个批次发完后，强制休息 600 秒 (10分钟)
MIN_DELAY = 20          # 单封邮件最小间隔 (秒) - 稍微调高了
MAX_DELAY = 40          # 单封邮件最大间隔 (秒) - 稍微调高了
# ===========================================

def read_template(filename):
    """读取模板文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"CRITICAL ERROR: 找不到模板文件 {filename}")
        return None

def get_server_connection():
    """建立并返回服务器连接"""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(">>> 邮件服务器连接成功")
        return server
    except Exception as e:
        print(f"!!! 服务器连接失败: {e}")
        return None

def send_invitations():
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("CRITICAL ERROR: 环境变量未配置！请检查 GitHub Secrets。")
        return

    html_content = read_template(HTML_TEMPLATE)
    if not html_content:
        return

    # 读取名单
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            streamers = list(reader)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: 找不到 CSV 文件 {CSV_FILE}")
        return

    total_count = len(streamers)
    print(f"=== 任务开始: 共有 {total_count} 封邮件待发送 ===")
    print(f"=== 策略: 每 {BATCH_SIZE} 封休息 {BATCH_PAUSE/60} 分钟 ===")

    server = None
    
    for index, row in enumerate(streamers):
        current_num = index + 1
        name = row.get('Name', '').strip()
        email = row.get('Email', '').strip()

        # 1. 连接检查：如果是刚开始，或者刚休息完，需要重新连接
        if server is None:
            server = get_server_connection()
            if not server:
                print("无法建立连接，任务终止。")
                break

        # 2. 发送邮件
        if email:
            print(f"[{current_num}/{total_count}] 正在发送 -> {name} <{email}>")
            
            try:
                # 替换名字
                personalized_html = html_content.replace('{name}', name)
                
                msg = MIMEMultipart()
                msg['From'] = formataddr(("Eugene from Tatalala", SENDER_EMAIL))
                msg['To'] = email
                msg['Subject'] = EMAIL_SUBJECT
                msg.attach(MIMEText(personalized_html, 'html', 'utf-8'))

                server.sendmail(SENDER_EMAIL, email, msg.as_string())
                print("   [OK] 发送成功")
            except Exception as e:
                print(f"   [ERR] 发送失败: {e}")

        # 3. 策略性休息逻辑
        
        # 如果这是最后一个人，直接结束，不需要休息
        if current_num == total_count:
            print("\n=== 所有邮件发送完毕! ===")
            break

        # 检查是否达到批次限制 (例如第 20, 40, 60 封)
        if current_num % BATCH_SIZE == 0:
            print(f"\n>>> 批次完成 ({BATCH_SIZE}封). 断开连接并休息 {BATCH_PAUSE/60} 分钟...")
            try:
                server.quit() # 主动断开，防止超时
            except:
                pass
            server = None # 标记为未连接
            time.sleep(BATCH_PAUSE) # 长休息
            print(">>> 休息结束，准备开始下一批...\n")
        
        else:
            # 普通的随机间隔 (模拟真人)
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"   ...等待 {delay} 秒")
            time.sleep(delay)

    # 最后的清理
    if server:
        try:
            server.quit()
        except:
            pass

if __name__ == '__main__':
    send_invitations()
