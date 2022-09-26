from typing import Any, Optional
from discord.embeds import Embed

from discord import Interaction, app_commands
from random import choice
from datetime import datetime
from discord import PartialMessageable
from bs4 import BeautifulSoup

from hiyobot.client import Hiyobot
from pypixiv.abc import BasePixiv


proxy_url = "https://api.saebasol.org/api/proxy/"


pixiv = app_commands.Group(name="픽시브", description="픽시브 일러스트를 가져옵니다.", nsfw=True)


def recompile_date(date: str):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y년 %m월 %d일")


def html2text(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text_parts = soup.findAll(text=True)
    return "".join(text_parts)


def pixiv_get_illustinfo(data: BasePixiv) -> Embed:
    data = data.body
    embed = Embed(
        title=data.title,
        url=f"https://www.pixiv.net/artworks/{data.id}",
        color=0x008AE6,
    )
    embed.add_field(name="설명", value=html2text(data.description), inline=True)
    embed.add_field(name="작가", value=data.userAccount, inline=True)
    embed.set_image(url=proxy_url + data.urls.original)
    embed.set_footer(
        text=f"👍 {data.likeCount} ❤️ {data.bookmarkCount} 👁️ {data.viewCount} • 업로드 날짜 {recompile_date(data.createDate)}"
    )
    return embed


def pixiv_make_illust_embed(data: BasePixiv) -> Embed:
    data = data.body
    embed = Embed(description=data.id, color=0x008AE6)
    embed.set_author(name=data.title, url=f"https://www.pixiv.net/artworks/{data.id}")
    embed.set_image(url=proxy_url + data.urls.original)
    embed.set_footer(text=f"Illust by {str(data.userAccount)}")
    return embed


@pixiv.command(
    name="뷰어",
    description="작품의 아이디로 작품을 열람합니다.",
)
@app_commands.describe(id="정보를 가져올 작품의 아이디입니다.", ephemeral="나에게만 보일지 선택하는 여부입니다.")
async def pixiv_view(
    interaction: Interaction, id: int, ephemeral: bool = False
) -> None:
    return await interaction.response.send_message(
        embed=pixiv_make_illust_embed(await Hiyobot.pypixiv.illustinfo(id)),
        ephemeral=ephemeral,
    )


@pixiv.command(
    name="정보",
    description="작품 번호를 입력하면 픽시브에서 해당 작품정보를 가져옵니다.",
)
@app_commands.describe(id="정보를 가져올 작품의 아이디입니다.", ephemeral="나에게만 보일지 선택하는 여부입니다.")
async def pixiv_info(
    interaction: Interaction, id: int, ephemeral: bool = False
) -> None:
    return await interaction.response.send_message(
        embed=pixiv_get_illustinfo(await Hiyobot.pypixiv.illustinfo(id)),
        ephemeral=ephemeral,
    )
