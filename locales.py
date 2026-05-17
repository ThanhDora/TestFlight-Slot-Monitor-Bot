"""
Bilingual messages (Vietnamese / English) for the bot.
"""

MESSAGES = {
    "vi": {
        "welcome": (
            "🤖 <b>TestFlight Slot Monitor</b>\n\n"
            "Xin chào! Tôi sẽ giúp bạn theo dõi slot TestFlight.\n\n"
            "📌 <b>Các lệnh:</b>\n"
            "/add <code>&lt;link&gt;</code> — Thêm link TestFlight\n"
            "/remove <code>&lt;id&gt;</code> — Xóa link theo dõi\n"
            "/list — Xem danh sách link đang theo dõi\n"
            "/check — Kiểm tra tất cả link ngay\n"
            "/interval <code>&lt;giây&gt;</code> — Đặt thời gian kiểm tra\n"
            "/lang <code>&lt;vi/en&gt;</code> — Chuyển ngôn ngữ\n"
            "/status — Trạng thái bot"
        ),
        "add_usage": "⚠️ Sử dụng: /add <code>&lt;link TestFlight&gt;</code>\n\nVí dụ: /add https://testflight.apple.com/join/AbCdEf",
        "invalid_url": "❌ Link không hợp lệ! Link phải có dạng:\n<code>https://testflight.apple.com/join/xxxxx</code>",
        "link_added": (
            "✅ <b>Đã thêm link theo dõi!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "📊 Trạng thái: {status}\n\n"
            "Bot sẽ tự động kiểm tra định kỳ."
        ),
        "link_exists": "⚠️ Link này đã có trong danh sách theo dõi rồi!",
        "link_removed": "🗑️ Đã xóa link <b>#{link_id}</b> — <b>{app_name}</b> khỏi danh sách.",
        "link_not_found": "❌ Không tìm thấy link với ID <b>#{link_id}</b>.",
        "remove_usage": "⚠️ Sử dụng: /remove <code>&lt;id&gt;</code>\n\nDùng /list để xem danh sách và ID.",
        "list_empty": "📭 Chưa có link nào đang theo dõi.\n\nDùng /add để thêm link TestFlight.",
        "list_header": "📋 <b>Danh sách theo dõi ({count} link):</b>\n",
        "list_item": (
            "\n<b>#{id}</b> — {app_name}\n"
            "   📊 {status} | ⏰ Kiểm tra: {last_checked}"
        ),
        "checking": "🔍 Đang kiểm tra tất cả link...",
        "check_done": "✅ Đã kiểm tra xong <b>{count}</b> link.",
        "check_error": "⚠️ Lỗi khi kiểm tra <b>{app_name}</b>: {error}",
        "slot_available": (
            "🎉 <b>TESTFLIGHT CÓ SLOT!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "⏰ Phát hiện lúc: <b>{time}</b>\n\n"
            "👉 Nhanh tay tham gia trước khi hết slot!"
        ),
        "slot_full": (
            "😢 <b>TESTFLIGHT ĐÃ HẾT SLOT!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "⏰ Thời gian: <b>{time}</b>\n\n"
            "Bot sẽ tiếp tục theo dõi và báo khi có slot mới."
        ),
        "join_button": "Tham Gia TestFlight",
        "interval_set": "⏱️ Đã đặt thời gian kiểm tra: <b>{seconds} giây</b>.",
        "interval_usage": "⚠️ Sử dụng: /interval <code>&lt;số giây&gt;</code>\n\nVí dụ: /interval 30",
        "interval_invalid": "❌ Vui lòng nhập số giây hợp lệ (5-86400).",
        "lang_set": "🌐 Đã chuyển sang <b>Tiếng Việt</b> 🇻🇳",
        "lang_usage": "⚠️ Sử dụng: /lang <code>&lt;vi/en&gt;</code>",
        "lang_invalid": "❌ Ngôn ngữ không hợp lệ. Chọn: <code>vi</code> hoặc <code>en</code>",
        "status_info": (
            "📊 <b>Trạng thái Bot</b>\n\n"
            "🔗 Link theo dõi: <b>{link_count}</b>\n"
            "⏱️ Kiểm tra mỗi: <b>{interval} giây</b>\n"
            "🌐 Ngôn ngữ: <b>{language}</b>\n"
            "⏰ Thời gian: <b>{current_time}</b>"
        ),
        "status_available": "🟢 Có slot",
        "status_full": "🔴 Hết slot",
        "status_unknown": "⚪ Chưa kiểm tra",
        "status_error": "🟡 Lỗi",
        "never": "Chưa bao giờ",
        "unauthorized": "🚫 Bạn không có quyền sử dụng bot này.",
    },
    "en": {
        "welcome": (
            "🤖 <b>TestFlight Slot Monitor</b>\n\n"
            "Hello! I will help you monitor TestFlight slots.\n\n"
            "📌 <b>Commands:</b>\n"
            "/add <code>&lt;link&gt;</code> — Add TestFlight link\n"
            "/remove <code>&lt;id&gt;</code> — Remove monitored link\n"
            "/list — View monitored links\n"
            "/check — Check all links now\n"
            "/interval <code>&lt;seconds&gt;</code> — Set check interval\n"
            "/lang <code>&lt;vi/en&gt;</code> — Switch language\n"
            "/status — Bot status"
        ),
        "add_usage": "⚠️ Usage: /add <code>&lt;TestFlight link&gt;</code>\n\nExample: /add https://testflight.apple.com/join/AbCdEf",
        "invalid_url": "❌ Invalid link! Must be:\n<code>https://testflight.apple.com/join/xxxxx</code>",
        "link_added": (
            "✅ <b>Link added for monitoring!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "📊 Status: {status}\n\n"
            "Bot will check automatically."
        ),
        "link_exists": "⚠️ This link is already being monitored!",
        "link_removed": "🗑️ Removed link <b>#{link_id}</b> — <b>{app_name}</b> from the list.",
        "link_not_found": "❌ Link with ID <b>#{link_id}</b> not found.",
        "remove_usage": "⚠️ Usage: /remove <code>&lt;id&gt;</code>\n\nUse /list to see IDs.",
        "list_empty": "📭 No links being monitored.\n\nUse /add to add a TestFlight link.",
        "list_header": "📋 <b>Monitored Links ({count}):</b>\n",
        "list_item": (
            "\n<b>#{id}</b> — {app_name}\n"
            "   📊 {status} | ⏰ Checked: {last_checked}"
        ),
        "checking": "🔍 Checking all links...",
        "check_done": "✅ Finished checking <b>{count}</b> links.",
        "check_error": "⚠️ Error checking <b>{app_name}</b>: {error}",
        "slot_available": (
            "🎉 <b>TESTFLIGHT SLOT AVAILABLE!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "⏰ Detected at: <b>{time}</b>\n\n"
            "👉 Join quickly before slots run out!"
        ),
        "slot_full": (
            "😢 <b>TESTFLIGHT SLOTS FULL!</b>\n\n"
            "📱 App: <b>{app_name}</b>\n"
            "⏰ Time: <b>{time}</b>\n\n"
            "Bot will continue monitoring and notify when slots open."
        ),
        "join_button": "Join TestFlight",
        "interval_set": "⏱️ Check interval set to: <b>{seconds} seconds</b>.",
        "interval_usage": "⚠️ Usage: /interval <code>&lt;seconds&gt;</code>\n\nExample: /interval 30",
        "interval_invalid": "❌ Please enter a valid number (5-86400).",
        "lang_set": "🌐 Switched to <b>English</b> 🇺🇸",
        "lang_usage": "⚠️ Usage: /lang <code>&lt;vi/en&gt;</code>",
        "lang_invalid": "❌ Invalid language. Choose: <code>vi</code> or <code>en</code>",
        "status_info": (
            "📊 <b>Bot Status</b>\n\n"
            "🔗 Monitored links: <b>{link_count}</b>\n"
            "⏱️ Check every: <b>{interval} seconds</b>\n"
            "🌐 Language: <b>{language}</b>\n"
            "⏰ Current time: <b>{current_time}</b>"
        ),
        "status_available": "🟢 Available",
        "status_full": "🔴 Full",
        "status_unknown": "⚪ Not checked",
        "status_error": "🟡 Error",
        "never": "Never",
        "unauthorized": "🚫 You are not authorized to use this bot.",
    },
}


def get_message(key: str, lang: str = "vi") -> str:
    """Get a localized message by key."""
    if lang not in MESSAGES:
        lang = "vi"
    return MESSAGES.get(lang, MESSAGES["vi"]).get(key, f"[Missing: {key}]")


def get_status_text(status: str, lang: str = "vi") -> str:
    """Get localized status text."""
    status_map = {
        "available": "status_available",
        "full": "status_full",
        "unknown": "status_unknown",
        "error": "status_error",
    }
    key = status_map.get(status, "status_unknown")
    return get_message(key, lang)
