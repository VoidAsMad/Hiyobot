import asyncio
from datetime import datetime
from pypixiv.client import PixivClient

async def main():
    async with PixivClient() as client:
        user = await client.illustinfo()
        for i in user.contents:
            print(i.rank)


def recompile_date(date: str):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y년 %m월 %d일")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
