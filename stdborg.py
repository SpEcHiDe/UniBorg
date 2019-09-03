# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
import sys
from pathlib import Path
from uniborg import Uniborg
from uniborg.storage import Storage
from telethon.sessions import StringSession


logging.basicConfig(level=logging.INFO)

# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Development as Config
    else:
        logging.warning("No config.py Found!")
        logging.info("Please run the command, again, after creating config.py similar to README.md")
        sys.exit(1)


if Config.DB_URI is None:
    logging.warning("No DB_URI Found!")


if len(Config.SUDO_USERS) >= 0:
    Config.SUDO_USERS.add("me")


if Config.HU_STRING_SESSION is not None:
    # for Running on Heroku
    session_name = str(Config.HU_STRING_SESSION)
    borg = Uniborg(
        StringSession(session_name),
        n_plugin_path="stdplugins/",
        db_plugin_path="dbplugins/",
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    borg.run_until_disconnected()
elif len(sys.argv) == 2:
    # for running on GNU/Linux
    session_name = str(sys.argv[1])
    borg = Uniborg(
        session_name,
        n_plugin_path="stdplugins/",
        db_plugin_path="dbplugins/",
        connection_retries=None,
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    borg.run_until_disconnected()
else:
    # throw error
    logging.error("USAGE EXAMPLE:\n"
                  "python3 -m stdborg <SESSION_NAME>"
                  "\n 👆👆 Please follow the above format to run your userbot."
                  "\n Bot quitting.")
