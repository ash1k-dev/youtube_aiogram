from aiogram import Bot
from core.db.methods.request import (
    get_user_from_db,
    get_channels_from_db,
)
from core.db.methods.update import update_last_video
from core.youtube.services import get_last_video
from core.bot.keyboards.inline import get_new_video_menu


from sqlalchemy.ext.asyncio import async_sessionmaker


async def check_video_update(bot: Bot, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        all_users = await get_user_from_db(session=session)
        for user in all_users:
            channels = await get_channels_from_db(
                telegram_id=user.telegram_id, session=session
            )
            for channel in channels:
                updated_last_video = get_last_video(channel=channel.channel_id)
                if channel.last_video != updated_last_video:
                    await update_last_video(
                        channel=channel.channel_id,
                        last_video=updated_last_video,
                        session=session,
                    )
                    messages_with_update = (
                        f"https://www.youtube.com/watch?v={updated_last_video}"
                    )
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=messages_with_update,
                        reply_markup=get_new_video_menu(messages_with_update),
                    )