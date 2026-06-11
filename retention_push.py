"""
retention_push.py — догоняющие пуши лидам, которые открыли бота,
но ещё НЕ оставили email в мини-аппе.

Источник правды — таблица email_leads (persistent в Postgres), поэтому пуши
переживают редеплой. Сконвертившиеся (оставившие email) и заблокировавшие бота
исключаются автоматически.

Запуск разово:        python retention_push.py
Railway cron job:     python retention_push.py    (например, раз в час)

Тюнинг через env:
  RETENTION_MIN_AGE_H   через сколько часов после /start слать первый пуш (деф. 24)
  RETENTION_GAP_H       минимум часов между пушами одному лиду          (деф. 48)
  RETENTION_MAX_PUSHES  максимум пушей на лида                          (деф. 3)
  RETENTION_BATCH       сколько слать за один запуск                    (деф. 200)
"""
import os
import asyncio
import logging

from telegram import Bot
from telegram.error import Forbidden, RetryAfter, TimedOut, NetworkError

from config import BOT_TOKEN
from brand import BRAND
import emaildb
from messages import REPEAT_PUSH
from conversation import _open_btn, MINI_APP_URL

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("retention")

MIN_AGE_S = float(os.environ.get("RETENTION_MIN_AGE_H", "24")) * 3600
GAP_S     = float(os.environ.get("RETENTION_GAP_H", "48")) * 3600
MAX_PUSH  = int(os.environ.get("RETENTION_MAX_PUSHES", "3"))
BATCH     = int(os.environ.get("RETENTION_BATCH", "200"))


def _text_for(lang: str, push_idx: int) -> str:
    variants = REPEAT_PUSH.get(lang) or REPEAT_PUSH.get("en") or ["👇"]
    return variants[min(push_idx, len(variants) - 1)]


async def main():
    if not MINI_APP_URL.startswith("https://"):
        logger.warning("MINI_APP_URL is not https — the button will not open the mini-app.")

    leads = emaildb.leads_due_for_push(BRAND.id, MIN_AGE_S, GAP_S, MAX_PUSH, BATCH)
    if not leads:
        logger.info(f"[{BRAND.id}] no leads due for a retention push.")
        logger.info(f"lead stats: {emaildb.lead_counts(BRAND.id)}")
        return

    logger.info(f"[{BRAND.id}] {len(leads)} leads due — sending…")
    bot = Bot(BOT_TOKEN)
    sent = blocked = failed = 0
    async with bot:
        for lead in leads:
            tg_id = lead["tg_id"]
            lang = lead.get("lang") or "en"
            text = _text_for(lang, lead.get("pushes", 0))
            try:
                await bot.send_message(
                    chat_id=tg_id, text=text,
                    reply_markup=_open_btn(lang), disable_web_page_preview=True)
                emaildb.record_lead_push(BRAND.id, tg_id)
                sent += 1
                await asyncio.sleep(0.05)        # ~20 msg/s, мягко к лимитам Telegram
            except Forbidden:
                # Пользователь заблокировал бота / удалил чат — больше не пушим.
                emaildb.mark_lead_blocked(BRAND.id, tg_id)
                blocked += 1
            except RetryAfter as e:
                logger.warning(f"flood control, sleeping {e.retry_after}s")
                await asyncio.sleep(e.retry_after + 1)
            except (TimedOut, NetworkError):
                await asyncio.sleep(1)
                failed += 1
            except Exception as e:
                logger.warning(f"push failed tg_id={tg_id}: {e}")
                failed += 1

    logger.info(f"[{BRAND.id}] done — sent={sent} blocked={blocked} failed={failed}")
    logger.info(f"lead stats: {emaildb.lead_counts(BRAND.id)}")


if __name__ == "__main__":
    asyncio.run(main())
