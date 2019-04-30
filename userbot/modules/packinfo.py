#
# Copyright (c) TelegramCompanion | 2019
#

import urllib
import re
import emoji
import aiohttp
import bs4
from userbot.events import register
from telethon import events
from userbot import bot, HELPER
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (DocumentAttributeFilename,
                               InputMediaUploadedDocument,
                               InputStickerSetShortName,
                               MessageMediaPhoto,
                               InputStickerSetID)
from telethon.tl.types import DocumentAttributeSticker

@register(outgoing=True, pattern="^.packinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        await bot.update_message(event, PACKINFO_HELP)
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await bot.update_message(event, "`Reply to a sticker to get the pack details`")
        return
    stickerset_attr = rep_msg.document.attributes[1]
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await bot.update_message(event, "`Not a valid sticker`")
        return
    get_stickerset = await bot(GetStickerSetRequest(InputStickerSetID(id=stickerset_attr.stickerset.id, access_hash=stickerset_attr.stickerset.access_hash)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = f"**Sticker Title:** `{get_stickerset.set.title}\n`" \
             f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n" \
             f"**Official:** `{get_stickerset.set.official}`\n" \
             f"**Archived:** `{get_stickerset.set.archived}`\n" \
             f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n" \
             f"**Emojis In Pack:** {' '.join(pack_emojis)}"
    await event.edit(OUTPUT)

HELPER.update(
    {"packinfo": "send sticker packinfo"}
)
