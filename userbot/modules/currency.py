#
# Copyright (c) UniBorg | 2019
#
from telethon import events
import asyncio
from datetime import datetime
import requests
from userbot.events import register
from userbot import CMD_HELP

#Using this module:-
#To use , type - .currency {ammount} {currency u typed} {currency u wanted }

@register(outgoing=True, pattern="^.currency (.*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(currency_from)
            current_response = requests.get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(number, currency_from, rebmun, currency_to))
            else:
                await event.edit("IDEKNOWTDWTT")
        except e:
            await event.edit(str(e))
    else:
        await event.edit("`.currency number from to`")
    end = datetime.now()
    ms = (end - start).seconds

CMD_HELP.update(
    {'currency': 'syntax : .currency {ammount} {currency_from} {currency_to} \n Just a converter'}
)
