from hiyobot.discord.embeds import Embed
from hiyobot.handler.app import HiyobotRequest
from hiyobot.handler.register import CommandArgument, RegisterCommand
from hiyobot.pagenator import Pagenator
from hiyobot.utils import is_nsfw, make_embed_with_info

hitomi = RegisterCommand(name="히토미", description="히토미 관련 명령어입니다.")


@hitomi.sub_command(
    name="정보",
    description="번호로 정보를 가져옵니다.",
    options=[
        CommandArgument(
            name="번호",
            description="정보를 가져올 번호입니다.",
            type=4,
            required=True,
        ),
        CommandArgument(
            name="나만보기",
            description="나에게만 보일지 선택하는 여부입니다.",
            type=5,
            required=False,
        ),
    ],
)
@is_nsfw
async def hitomi_info(request: HiyobotRequest, number: int, ephemeral: bool = False):
    info = await request.app.ctx.mintchoco.info(number)
    if info:
        embed = make_embed_with_info(info)
        return await request.ctx.response.send(embed=embed, ephemeral=ephemeral)

    await request.ctx.response.send("정보를 찾을수 없어요.", ephemeral=ephemeral)


@hitomi.sub_command(
    name="리스트",
    description="최신 작품 목록을 가져옵니다.",
    options=[
        CommandArgument(
            name="페이지",
            description="가져올 페이지입니다.",
            value=1,
            type=4,
            required=False,
        ),
        CommandArgument(
            name="나만보기",
            description="나에게만 보일지 선택하는 여부입니다.",
            type=5,
            required=False,
        ),
    ],
)
@is_nsfw
async def hitomi_list(request: HiyobotRequest, number: int, ephemeral: bool = False):
    user_id = int(request.json["member"]["user"]["id"])
    infos = await request.app.ctx.mintchoco.list(number)
    assert infos

    embeds = [make_embed_with_info(info) for info in infos.list]

    pagenator = Pagenator(user_id, embeds)

    await request.ctx.response.send(
        embed=embeds[0],
        component=pagenator,
    )


@hitomi.sub_command(
    name="뷰어",
    description="디스코드 내에서 작품을 감상합니다.",
    options=[
        CommandArgument(
            name="번호",
            description="감상할 번호입니다.",
            type=4,
            required=True,
        ),
        CommandArgument(
            name="나만보기",
            description="나에게만 보일지 선택하는 여부입니다.",
            type=5,
            required=False,
        ),
    ],
)
@is_nsfw
async def hitomi_viewer(request: HiyobotRequest, number: int, ephemeral: bool = False):
    async def coro():
        images = await request.app.ctx.mintchoco.image(number)
        user_id = int(request.json["member"]["user"]["id"])
        if images:
            page = 0
            total = len(images.files)
            embeds: list[Embed] = []

            for file in images.files:
                page += 1
                embed = Embed()
                embed.set_image(
                    url=f"{request.app.ctx.mintchoco.BASE_URL}/proxy/{file.url}"
                )
                embed.set_footer(text=f"{page}/{total}")
                embeds.append(embed)

            pagenator = Pagenator(user_id, embeds)
            await request.ctx.response.follow_up_send(
                embed=embeds[0], component=pagenator
            )
        else:
            await request.ctx.response.follow_up_send(
                "정보를 찾을수 없어요.", ephemeral=ephemeral
            )

    await request.ctx.response.wait(coro)


@hitomi.sub_command(
    name="검색",
    description="작품을 찾습니다.",
    options=[
        CommandArgument(
            name="쿼리",
            description="검색할 제목 또는 태그입니다.",
            type=3,
            required=True,
        ),
        CommandArgument(
            name="페이지",
            description="가져올 페이지입니다.",
            value=1,
            type=4,
            required=False,
        ),
        CommandArgument(
            name="나만보기",
            description="나에게만 보일지 선택하는 여부입니다.",
            type=5,
            required=False,
        ),
    ],
)
@is_nsfw
async def hitomi_search(request: HiyobotRequest, query: str, ephemeral: bool = False):
    querys = query.split(" ")
    user_id = int(request.json["member"]["user"]["id"])
    search = await request.app.ctx.mintchoco.search(querys)
    if search:
        if search.result:
            embeds = [make_embed_with_info(info) for info in search.result]

            pagenator = Pagenator(user_id, embeds)

            return await request.ctx.response.send(
                embed=embeds[0],
                component=pagenator,
            )

    await request.ctx.response.send("정보를 찾을수 없어요.", ephemeral=ephemeral)
