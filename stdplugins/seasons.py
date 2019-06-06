# By @STARKTM1
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.seasons", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("╚═╗║╍╽┅╈╙─╖¡ ┆0┆╽╲╿┕━┓ \
                      ╚═╜╙━╹©╹╚═╱╳∙┕═┙╵=╹_└─┛ \
                      ╦┉╴╓─╮╓─ ╱╳¤╳╲┕ ┎─┎┬┬┒• \
                      ║ ╗║─╮╬(•╱∑╳ɔ╲¡ʻ┣╸ || ┒ \
                      ╙─©◊ ◊╙─╱╳╳⅓╳╳╲┆┖─:┗┛ ┸ \
                      ┎╲ ╷╭─┨?╱╳¿╳╳▲╲♪╔═╡**** \
                      ┃╲╲┃┃─╮╱↑╳╳╳ợ╳╳╲╚═╗from \
                      ╵ H┚╰─ᵒ╱╳╳∞╳╳╳¤╲╞═╝ the↓ \
                      ↓╎O┊◊ˈ╱╳◉╳%╳╳=╳╳╲◆╦═╦═] \
                      H╎L┊─╱♪╳╳ʷ╳ ∫╳ §╲┊ ║A║™] \
                      A╎I┊╍╱╳∂╳╳◆╳╳╳Ω╳ ╲┊D┊═╗ \
                      P─D──╱╳╳¶╳ ╳$╳  ¤╳┊O┊T║ \
                      P║A┊╱╳ Ø╳╳ƒ╳╳╳☑╳ ╲B ┊Y║ \
                      Y║Y┊╱¤╳╳œ╳╳╳Ṃ ╳╳|╲ E┊P║ \
                      │┐S╱╳╳╳ˣ╳╳×╳╳╳◆ ╳¤╳╲  ┊E│ \
                      ↓ !!┟╥─╯┍╇┯█┯╇┑▚│┇──┴─┊ \
                        v╶═╝┎┘│━┵┼┶━│┈╢TEAM<╯ \
                      ╺━│┃░▒▓▌!▐▓▒░┃││┼☑┘╳ ")
