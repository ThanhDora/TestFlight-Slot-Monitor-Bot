"""
TestFlight Slot Monitor — Telegram Bot
Main entry point with command handlers and periodic checker.
"""
import re
import asyncio
import logging
from datetime import datetime
from functools import wraps

# pyrefly: ignore [missing-import]
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# pyrefly: ignore [missing-import]
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN, OWNER_ID, DEFAULT_INTERVAL, MONGO_URI, MONGO_DB_NAME
from database import Database
from checker import check_testflight
from locales import get_message, get_status_text

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

db = Database(MONGO_URI, MONGO_DB_NAME)

TESTFLIGHT_RE = re.compile(r"https?://testflight\.apple\.com/join/\w+")


# ─── Auth decorator ───────────────────────────────────────────────
def owner_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID:
            lang = db.get_setting("language", "vi")
            await update.message.reply_text(get_message("unauthorized", lang))
            return
        return await func(update, context)
    return wrapper


def _lang() -> str:
    return db.get_setting("language", "vi")


def _now_str() -> str:
    return datetime.now().strftime("%H:%M %d/%m/%Y")


AUTO_DELETE_SECONDS = 300  # 5 minutes


async def _delete_msg_job(context: ContextTypes.DEFAULT_TYPE):
    """Job callback to delete a message."""
    try:
        await context.bot.delete_message(
            chat_id=context.job.data["chat_id"],
            message_id=context.job.data["message_id"],
        )
    except Exception:
        pass


def _schedule_delete(context: ContextTypes.DEFAULT_TYPE, msg, delay: int = AUTO_DELETE_SECONDS):
    """Schedule a message to be deleted after `delay` seconds."""
    context.job_queue.run_once(
        _delete_msg_job,
        when=delay,
        data={"chat_id": msg.chat_id, "message_id": msg.message_id},
    )


async def _delete_user_cmd(update: Update):
    """Try to delete the user's command message."""
    try:
        await update.message.delete()
    except Exception:
        pass


# ─── /start ───────────────────────────────────────────────────────
@owner_only
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(get_message("welcome", _lang()), parse_mode="HTML")
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /add ─────────────────────────────────────────────────────────
@owner_only
async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()

    if not context.args:
        msg = await update.message.reply_text(get_message("add_usage", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    url = context.args[0].strip()
    if not TESTFLIGHT_RE.fullmatch(url):
        msg = await update.message.reply_text(get_message("invalid_url", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    # First check to get app name and current status
    result = check_testflight(url)
    app_name = result.app_name
    status = result.status

    if not db.add_link(url, app_name, status):
        msg = await update.message.reply_text(get_message("link_exists", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    status_text = get_status_text(status, lang)
    text = get_message("link_added", lang).format(
        app_name=app_name, status=status_text,
    )

    keyboard = [[InlineKeyboardButton(
        f"🚀 {get_message('join_button', lang)}", url=url,
    )]]
    msg = await update.message.reply_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /remove ──────────────────────────────────────────────────────
@owner_only
async def cmd_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()

    if not context.args:
        msg = await update.message.reply_text(get_message("remove_usage", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    try:
        link_id = int(context.args[0].lstrip("#"))
    except ValueError:
        msg = await update.message.reply_text(get_message("remove_usage", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    removed = db.remove_link(link_id)
    if removed:
        text = get_message("link_removed", lang).format(
            link_id=removed["id"], app_name=removed["app_name"],
        )
    else:
        text = get_message("link_not_found", lang).format(link_id=link_id)

    msg = await update.message.reply_text(text, parse_mode="HTML")
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /list ────────────────────────────────────────────────────────
@owner_only
async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()
    links = db.get_all_links()

    if not links:
        msg = await update.message.reply_text(get_message("list_empty", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    text = get_message("list_header", lang).format(count=len(links))
    buttons = []

    for link in links:
        checked = link["last_checked"]
        if checked:
            try:
                dt = datetime.fromisoformat(checked)
                checked = dt.strftime("%H:%M %d/%m")
            except ValueError:
                pass
        else:
            checked = get_message("never", lang)

        text += get_message("list_item", lang).format(
            id=link["id"],
            app_name=link["app_name"],
            status=get_status_text(link["status"], lang),
            last_checked=checked,
        )
        buttons.append([InlineKeyboardButton(
            f"🔗 {link['app_name']}", url=link["url"],
        )])

    msg = await update.message.reply_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /check ──────────────────────────────────────────────────────
@owner_only
async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()
    links = db.get_all_links()

    if not links:
        msg = await update.message.reply_text(get_message("list_empty", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    checking_msg = await update.message.reply_text(get_message("checking", lang), parse_mode="HTML")
    await _run_checks(context)

    # Delete the "checking..." message
    try:
        await checking_msg.delete()
    except Exception:
        pass

    # Build status report
    links = db.get_all_links()  # refresh after check
    text = get_message("check_done", lang).format(count=len(links))
    text += "\n"
    buttons = []

    for link in links:
        status_icon = get_status_text(link["status"], lang)
        text += f"\n{status_icon} — <b>{link['app_name']}</b>"

        buttons.append([InlineKeyboardButton(
            f"🔗 {link['app_name']}", url=link["url"],
        )])

    msg = await update.message.reply_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /interval ────────────────────────────────────────────────────
@owner_only
async def cmd_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()

    if not context.args:
        msg = await update.message.reply_text(get_message("interval_usage", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    try:
        seconds = int(context.args[0])
        if not 5 <= seconds <= 86400:
            raise ValueError
    except ValueError:
        msg = await update.message.reply_text(get_message("interval_invalid", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    db.set_setting("interval", str(seconds))

    # Reschedule the job
    _reschedule_job(context, seconds)

    msg = await update.message.reply_text(
        get_message("interval_set", lang).format(seconds=seconds), parse_mode="HTML",
    )
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /lang ────────────────────────────────────────────────────────
@owner_only
async def cmd_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()

    if not context.args:
        msg = await update.message.reply_text(get_message("lang_usage", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    new_lang = context.args[0].lower()
    if new_lang not in ("vi", "en"):
        msg = await update.message.reply_text(get_message("lang_invalid", lang), parse_mode="HTML")
        _schedule_delete(context, msg)
        await _delete_user_cmd(update)
        return

    db.set_setting("language", new_lang)
    msg = await update.message.reply_text(get_message("lang_set", new_lang), parse_mode="HTML")
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── /status ──────────────────────────────────────────────────────
@owner_only
async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang()
    interval = db.get_setting("interval", str(DEFAULT_INTERVAL))
    lang_display = "Tiếng Việt 🇻🇳" if lang == "vi" else "English 🇺🇸"

    text = get_message("status_info", lang).format(
        link_count=db.get_link_count(),
        interval=interval,
        language=lang_display,
        current_time=_now_str(),
    )
    msg = await update.message.reply_text(text, parse_mode="HTML")
    _schedule_delete(context, msg)
    await _delete_user_cmd(update)


# ─── Periodic checker ────────────────────────────────────────────
async def _run_checks(context: ContextTypes.DEFAULT_TYPE):
    """Check all monitored links and send notifications on status change."""
    links = db.get_all_links()
    lang = _lang()

    for link in links:
        result = check_testflight(link["url"])
        new_status = result.status
        old_status = link["status"]
        app_name = result.app_name if result.app_name != "Unknown App" else link["app_name"]

        # Handle errors
        if new_status == "error":
            db.update_link_checked(link["id"])
            logger.warning(
                "Error checking %s (%s): %s", link["app_name"], link["url"], result.error,
            )
            continue

        # Detect status change
        has_changed = old_status != new_status and old_status != "unknown"

        # Update DB (only mark status_changed when it actually changed)
        db.update_link_status(link["id"], new_status, app_name, status_changed=has_changed)

        # Notify on status change
        if not has_changed:
            continue

        if new_status == "available":
            keyboard = [[InlineKeyboardButton(
                f"🚀 {get_message('join_button', lang)}", url=link["url"],
            )]]
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=get_message("slot_available", lang).format(
                    app_name=app_name, time=_now_str(),
                ),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif new_status == "full":
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=get_message("slot_full", lang).format(
                    app_name=app_name, time=_now_str(),
                ),
                parse_mode="HTML",
            )


async def periodic_check(context: ContextTypes.DEFAULT_TYPE):
    """Job callback for periodic checks."""
    logger.info("Running periodic check...")
    await _run_checks(context)
    logger.info("Periodic check complete.")


def _reschedule_job(context: ContextTypes.DEFAULT_TYPE, seconds: int):
    """Remove existing check job and create a new one with updated interval."""
    jobs = context.job_queue.get_jobs_by_name("check_all")
    for job in jobs:
        job.schedule_removal()
    context.job_queue.run_repeating(
        periodic_check,
        interval=seconds,
        first=10,
        name="check_all",
    )


# ─── Main ─────────────────────────────────────────────────────────
def main():
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        print("❌ BOT_TOKEN chưa được cấu hình!")
        print("   Tạo file .env từ .env.example và điền token.")
        return

    if OWNER_ID == 0:
        print("❌ OWNER_ID chưa được cấu hình!")
        print("   Thêm Telegram User ID vào file .env.")
        return

    if not MONGO_URI:
        print("❌ MONGO_URI chưa được cấu hình!")
        print("   Thêm MongoDB connection string vào file .env.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("add", cmd_add))
    app.add_handler(CommandHandler("remove", cmd_remove))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("check", cmd_check))
    app.add_handler(CommandHandler("interval", cmd_interval))
    app.add_handler(CommandHandler("lang", cmd_lang))
    app.add_handler(CommandHandler("status", cmd_status))

    # Setup periodic check job
    interval = int(db.get_setting("interval", str(DEFAULT_INTERVAL)))
    app.job_queue.run_repeating(
        periodic_check,
        interval=interval,
        first=10,
        name="check_all",
    )

    logger.info("🚀 Bot started! Checking every %d seconds.", interval)

    # Python 3.14+: must create event loop explicitly
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
