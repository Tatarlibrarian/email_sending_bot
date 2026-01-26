# Email Sending Bot | 邮件发送机器人

这是一个自动化邮件发送系统,用于向主播批量发送个性化的推广邮件。

## 📋 项目简介

本项目是一个基于 Python 的邮件营销机器人,主要用于向 Twitch 和 Kick 平台的主播批量发送产品推广邮件。该机器人通过 GitHub Actions 实现自动化定时发送,并具有以下特点:

- ✅ 支持 HTML 格式的精美邮件模板
- ✅ 从 CSV 文件读取收件人名单
- ✅ 智能批次发送策略(每20封邮件暂停10分钟)
- ✅ 随机延迟发送,模拟真人操作
- ✅ 通过 GitHub Actions 定时自动执行
- ✅ 支持测试模式,可单独测试邮件发送

## 📁 项目结构

```
email_sending_bot/
├── .github/
│   └── workflows/
│       ├── send_email.yml      # 正式发送的 GitHub Actions 工作流
│       └── test_email.yml      # 测试发送的 GitHub Actions 工作流
├── send_mail.py                # 主邮件发送脚本
├── test_mail.py                # 测试邮件发送脚本
├── template.html               # HTML 邮件模板
├── streamers.csv               # 正式发送的主播名单
├── streamers_test.csv          # 测试用的主播名单
└── README.md                   # 项目说明文档(本文件)
```

## 🔑 需要重新配置的秘钥

**如果您通过 ZIP 方式获得本项目,需要在新的 GitHub 仓库中重新配置以下环境变量:**

### 1. GitHub Secrets 配置

前往仓库的 `Settings` → `Secrets and variables` → `Actions` → `New repository secret`,添加以下两个秘钥:

| 秘钥名称 | 说明 | 获取方式 |
|---------|------|---------|
| `MY_EMAIL` | 发件人的 Gmail 邮箱地址 | 使用您的 Gmail 账号 |
| `MY_PASSWORD` | Gmail 应用专用密码 | 参见下方"获取 Gmail 应用密码"说明 |

### 2. 获取 Gmail 应用专用密码

> ⚠️ **重要**: 不要使用您的 Gmail 登录密码,必须使用"应用专用密码"

1. 登录您的 Google 账号
2. 前往 [Google 账户安全设置](https://myaccount.google.com/security)
3. 确保已启用 **两步验证**
4. 在"两步验证"下方找到 **应用专用密码** (App Passwords)
5. 选择"邮件"和"其他",输入名称(如 "Email Bot")
6. 复制生成的 16 位密码(不含空格)
7. 将此密码配置到 GitHub Secrets 的 `MY_PASSWORD` 中

## ⚙️ 使用说明

### 方式一: 通过 GitHub Actions 自动发送(推荐)

1. **配置秘钥** (参见上方"需要重新配置的秘钥"章节)
2. **准备收件人名单**
   - 编辑 `streamers.csv` 文件
   - 格式为: `Name,Email`
   - 示例:
     ```csv
     Name,Email
     Alice,alice@example.com
     Bob,bob@example.com
     ```
3. **设置定时任务**(可选)
   - 编辑 `.github/workflows/send_email.yml` 文件
   - 修改 `cron` 表达式(默认为 UTC 时间 1月13日 14:30)
   - Cron 格式: `分 时 日 月 星期` (使用 UTC 时间)
4. **手动触发**
   - 前往仓库的 `Actions` 标签页
   - 选择 "Scheduled Email Sender" 工作流
   - 点击 `Run workflow` 按钮

### 方式二: 本地运行

1. **安装依赖**
   ```bash
   # 本项目仅使用 Python 标准库,无需额外安装依赖
   ```

2. **设置环境变量**
   ```bash
   # Linux/Mac
   export MY_EMAIL="your-email@gmail.com"
   export MY_PASSWORD="your-app-password"

   # Windows (PowerShell)
   $env:MY_EMAIL="your-email@gmail.com"
   $env:MY_PASSWORD="your-app-password"
   ```

3. **测试发送**
   ```bash
   # 编辑 test_mail.py,修改测试收件人信息
   python test_mail.py
   ```

4. **正式发送**
   ```bash
   python send_mail.py
   ```

## 🎨 自定义邮件内容

### 修改邮件模板

编辑 `template.html` 文件,您可以:
- 修改邮件的文字内容
- 调整样式和布局
- 更改 Logo 和图片链接

### 修改邮件主题

编辑 `send_mail.py` 文件,找到:
```python
EMAIL_SUBJECT = 'Level Up Your Stream: Get Your AI Co-Host Free for 7 Days!'
```
将其修改为您想要的主题。

### 修改发件人显示名称

编辑 `send_mail.py` 文件,找到:
```python
msg['From'] = formataddr(("Eugene from Tatalala", SENDER_EMAIL))
```
将 `"Eugene from Tatalala"` 修改为您想要的显示名称。

## 📊 发送策略配置

在 `send_mail.py` 中可以调整以下参数:

```python
BATCH_SIZE = 20         # 每发送 20 封邮件为一个批次
BATCH_PAUSE = 600       # 每个批次发完后,休息 600 秒 (10分钟)
MIN_DELAY = 20          # 单封邮件最小间隔 (秒)
MAX_DELAY = 40          # 单封邮件最大间隔 (秒)
```

这些参数用于模拟真人发送行为,避免被 Gmail 识别为垃圾邮件发送者。

## ⚠️ 注意事项

1. **Gmail 发送限制**
   - Gmail 免费账户每天有发送限制(约 500 封/天)
   - 建议分批发送,避免触发限制

2. **邮件内容合规**
   - 确保邮件内容符合反垃圾邮件法规
   - 建议在邮件中提供退订链接

3. **收件人隐私**
   - 请确保您有权向名单中的收件人发送邮件
   - 不要滥用此工具发送垃圾邮件

4. **GitHub Actions 运行时间**
   - 默认最大运行时间为 360 分钟(6小时)
   - 如果名单较长,请注意调整 `timeout-minutes` 参数

## 🧪 测试建议

在正式发送大量邮件前,建议:

1. 使用 `test_mail.py` 向您自己的邮箱发送测试邮件
2. 检查邮件是否被识别为垃圾邮件
3. 确认邮件格式和内容显示正常
4. 使用 `streamers_test.csv` 进行小批量测试

## 📝 更新日志

- **初始版本**: 完成基本的批量邮件发送功能
- 支持 GitHub Actions 定时触发
- 添加智能批次发送策略
- 支持 HTML 邮件模板

## 📄 许可证

本项目仅供学习和个人使用,请勿用于非法或背德用途。
