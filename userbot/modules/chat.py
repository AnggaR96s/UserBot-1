# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing userid, chatid and log commands"""

from time import sleep

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """
    if target.text[0].isalpha() or target.text[0] in ("/", "#", "@", "!"):
        return
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"

        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit(
            "**Name:** {} \n**User ID:** `{}`"
            .format(name, user_id)
        )


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    if not chat.text[0].isalpha() and chat.text[0] not in ("/", "#", "@", "!"):
        await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern="^.log")
async def log(log_text):
    """ For .log command, forwards a message or the command argument to the bot logs group """
    if log_text.text[0].isalpha() or log_text.text[0] in ("/", "#", "@", "!"):
        return

    textx = await log_text.get_reply_message()
    message = textx
    message = str(message.message)
    if BOTLOG:
        await (await log_text.get_reply_message()).forward_to(BOTLOG_CHATID)
        await log_text.edit("`Logged Successfully`")
    else:
        await log_text.edit("`This feature requires Logging to be enabled!`")
    sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    if not leave.text[0].isalpha() and leave.text[0] not in ("/", "#", "@", "!"):
        await leave.edit("`Nope, no, no, I go away`")
        await bot(LeaveChannelRequest(leave.chat_id))


CMD_HELP.update({
    "chatid": "Fetches the current chat's ID"
})
CMD_HELP.update({
    "userid": "Fetches the ID of the user in reply, if its a \
forwarded message, finds the ID for the source."
})
CMD_HELP.update({
    "log": "Forwards the message you've replied to in your \
bot logs group."
})
CMD_HELP.update({
    "kickme": "Leave from a targeted group."
})
