# By @STARKTM1
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.seasons", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("+×△▲△©━┭╱═══╲┮━©△▲△×+\
╔══╩╬╩╡÷╱← 0 →╲÷╞╩╬╩══╗ \
╚═╗╭╫╮ợ╱┅┅┓┅┏┅┅╲ọ╭╫╮╔═╝ \
╒═╝╎║┊╱X╭─────╮X╲┊║╎╚═╕ \
││┐╎║┊╳╓╖ BOX ╥╖╳┊║╎┌││ \
└││╎║╰─╨╠═════╣╨─╯║╎││┘ \ 
│└│╞╝╔╗▞╟╱╲╳╱╲╢▚╔╗╚╡│┘│ \
╰─╥┧Y║║▞ ┳┳┳┳┳ ▚║║Y┟╥─╯ \
☐┌╢┗┛╠║▞┍╇╇Ø╇╇┑▚║╣┗┛╟┐ \
┃!╚══╝┎┐│━┵┼┶━│┌┒╚══╝!┃ \
 ┃└┐┼┃│┃╷└─────┘╷┃│┃┼┌┘┃ \
┃♪╿│▼▽┃╰───*───╯┃▽▼│╿√┃ \
 ╚╦╧╰─>┡ DRAWING ┩<─╯╧╦╝ \
╶I┉┉┉┭└┄┄┄┄┄┄┄┄┄┘┮┉┉┉I- \
╭──┬─┴   SOU┬RCE  ┴─┬──╮ \
┢━━┷━━━━╸CO┼DE╺━━━━┷━━┪ \
━━━┻╾╮←(┏┑PRO┍┓)→╭╼┻━━━ \
░▒▓▌─╯┯━┷└───┘┷━┯╰─▐▓▒░ \
z─────┘────¡────└───── ")
