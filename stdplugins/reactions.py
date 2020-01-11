# For UniBorg
# By Priyam Kalra
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types


@borg.on(admin_cmd(pattern="oof ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    for _ in range(10):
        await event.edit(";_;")
        await event.edit("_;;")
        await event.edit(";;_")
    await event.edit(";_;")
    
@borg.on(admin_cmd(pattern="sed ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    for _ in range(10):
        await event.edit(":/")
        await event.edit(":|")
        await event.edit(":\\")
    await event.edit(":/")

@borg.on(admin_cmd(pattern="emoji ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input_str = event.pattern_match.group(1)
        if input_str == "yee":
            await event.edit("""ツ""")
        elif input_str == "happy":
            await event.edit("""
(ʘ‿ʘ)
""")
        elif input_str == "veryhappy":
            await event.edit("""
=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾
""")
        elif input_str == "amazed":
            await event.edit("""
ヾ(o✪‿✪o)ｼ
""")
        elif input_str == "crying":
            await event.edit("""
༎ຶ‿༎ຶ
""")
        elif input_str == "dicc":
            await event.edit("""
╰U╯☜(◉ɷ◉ )
""")
        elif input_str == "fek":
            await event.edit("""
╰U╯\n(‿ˠ‿)
""")
        elif input_str == "ded":
            await event.edit("""
✖‿✖
""")
        elif input_str == "sad":
            await event.edit("""
⊙︿⊙
""")
        elif input_str == "lenny":
            await event.edit("""
( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)
""")
        elif input_str == "idc":
            await event.edit("""
¯\_(ツ)_/¯
""")
        else:
            await event.edit("variable not defined.")
            
@borg.on(admin_cmd(pattern="ascii ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input_str = event.pattern_match.group(1)
        if input_str == "mf":
            await event.edit("""
......................................../´¯/) 
......................................,/¯../ 
...................................../..../ 
..................................../´.¯/
..................................../´¯/
..................................,/¯../ 
................................../..../ 
................................./´¯./
................................/´¯./
..............................,/¯../ 
............................./..../ 
............................/´¯/
........................../´¯./
........................,/¯../ 
......................./..../ 
....................../´¯/
....................,/¯../ 
.................../..../ 
............./´¯/'...'/´¯¯·¸ 
........../'/.../..../......./¨¯\ 
........('(...´...´.... ¯~/'...') 
.........\.................'...../ 
..........''...\.......... _.·´ 
............\..............( 
..............\.............\...`
    """)

            
