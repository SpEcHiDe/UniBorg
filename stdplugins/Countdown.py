# For @UniBorg
"""Countdown Commands
.timer
.fcd"""

from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd
import importlib.util
import asyncio
import random
import importlib.util


@borg.on(events.NewMessage(outgoing=True, pattern='^\.(f?t)imer '))
async def timer_blankx(e):
 txt=e.text[7:] + '\nDeleting in '
 j=10
 k=j
 for j in range(j):
  await e.edit(txt + str(k))
  k=k-1
  await asyncio.sleep(1)
 if e.pattern_match.group(1) == 't':
  await e.delete()
 else:
  await e.edit(txt + 'NaN')


@borg.on(events.NewMessage(outgoing=True, pattern='^\.(f?f)cd '))
async def timer_blankx(e):
 txt=e.text[5:] + '\n\n`Calling 911 in` '
 j=10
 k=j
 for j in range(j):
  await e.edit(txt + str(k))
  k=k-1
  await asyncio.sleep(1)
 if e.pattern_match.group(1) == 'f':
  await e.edit("`Successfully Called 911. They will be here in any minute. Get ready.` ")

