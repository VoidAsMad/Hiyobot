from typing import Any

from mintchoco.model.info import Info

from hiyobot.discord.embeds import Embed
from hiyobot.handler.app import HiyobotRequest


async def is_nsfw(request: HiyobotRequest):
    assert request.ctx.interaction.channel_id

    return await request.app.ctx.http.channel_is_nsfw(
        request.ctx.interaction.channel_id
    )


def available_only_on_nsfw_channel(f: Any):
    async def inner(request: HiyobotRequest, *args: Any, **kwargs: Any):
        if not await is_nsfw(request):
            return await request.ctx.response.send(
                "연령 제한 채널 설정이 되어있지 않습니다. 연령 제한 채널을 설정해주세요.",
                ephemeral=True,
            )

        return await f(request, *args, **kwargs)

    return inner


def make_embed_with_info(info: Info):
    tags_join = ", ".join(info.tags) if info.tags else "없음"
    embed = Embed(
        title=info.title,
    )
    embed.set_thumbnail(url=f"https://api.saebasol.org/api/proxy/{info.thumbnail}")
    embed.add_field(
        name="번호",
        value=f"[{info.id}](https://hitomi.la/reader/{info.id}.html)",
        inline=False,
    )
    embed.add_field(
        name="타입",
        value=info.type,
        inline=False,
    )
    embed.add_field(
        name="작가", value=",".join(info.artist) if info.artist else "없음", inline=False
    )
    embed.add_field(
        name="그룹", value=",".join(info.group) if info.group else "없음", inline=False
    )
    embed.add_field(
        name="원작", value=",".join(info.series) if info.series else "없음", inline=False
    )
    embed.add_field(
        name="캐릭터",
        value=",".join(info.character) if info.character else "없음",
        inline=False,
    )
    embed.add_field(
        name="태그",
        value=tags_join if len(tags_join) <= 1024 else "표시하기에는 너무 길어요.",
        inline=False,
    )
    return embed
