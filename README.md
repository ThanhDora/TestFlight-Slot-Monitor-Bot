# 🛩️ TestFlight Slot Monitor Bot

Bot Telegram tự động theo dõi slot TestFlight và thông báo khi có slot trống.

## ✨ Tính năng

- 🔍 Theo dõi nhiều link TestFlight cùng lúc
- 🔔 Thông báo ngay khi có slot (hoặc hết slot)
- ⏱️ Tùy chỉnh thời gian kiểm tra (theo giây)
- 🌐 Hỗ trợ song ngữ Tiếng Việt / English
- 🔘 Inline button để tham gia nhanh
- 🗑️ Tự động dọn tin nhắn sau 5 phút
- 💾 Lưu trữ MongoDB Atlas

## 🚀 Cài đặt

### 1. Cài dependencies

```bash
cd Tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Tạo Bot Telegram

1. Mở Telegram, tìm **@BotFather**
2. Gửi `/newbot` và làm theo hướng dẫn
3. Copy **Bot Token** được cấp

### 3. Lấy User ID

1. Mở Telegram, tìm **@userinfobot**
2. Gửi `/start`
3. Copy **User ID** của bạn

### 4. Cấu hình

```bash
cp .env.example .env
```

Mở file `.env` và điền:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
OWNER_ID=123456789
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
```

### 5. Chạy bot

```bash
source venv/bin/activate
python bot.py
```

## 📌 Các lệnh

| Lệnh | Mô tả |
|---|---|
| `/start` | Khởi động, xem hướng dẫn |
| `/add <link>` | Thêm link TestFlight |
| `/remove <id>` | Xóa link (dùng `/list` để xem ID) |
| `/list` | Xem danh sách link + trạng thái |
| `/check` | Kiểm tra tất cả ngay |
| `/interval <giây>` | Đặt thời gian kiểm tra (5-86400) |
| `/lang <vi/en>` | Chuyển ngôn ngữ |
| `/status` | Xem trạng thái bot |

## 📝 Ví dụ sử dụng

```
/add https://testflight.apple.com/join/AbCdEf
/interval 30
/list
/check
```

## 🔧 Chạy nền (Linux/macOS)

```bash
nohup python bot.py &
```

Hoặc dùng `screen`/`tmux`:
```bash
screen -S tfbot
python bot.py
# Ctrl+A, D để detach
```
