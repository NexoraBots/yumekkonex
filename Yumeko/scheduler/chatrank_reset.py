import asyncio
from datetime import datetime
import pytz

from Yumeko.database.chatrank_db import reset_daily, reset_weekly


IST = pytz.timezone("Asia/Kolkata")


async def chatrank_resets():

    while True:

        now = datetime.now(IST)

        # DAILY RESET 1 AM IST
        if now.hour == 1 and now.minute == 0:
            await reset_daily()
            await asyncio.sleep(60)

        # WEEKLY RESET SUNDAY 1 AM IST
        if now.weekday() == 6 and now.hour == 1 and now.minute == 0:
            await reset_weekly()
            await asyncio.sleep(60)

        await asyncio.sleep(20)
