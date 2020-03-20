import asyncio
import git
import heroku3

## Setup - start ##
strings = {
    "bot up to date": "Bot is up to Date!",
    "temp branch": "temp_branch",
    "heroku api key": Config.HEROKU_API_KEY,
    "repo link": Config.REPO_LINK,
    "refspec": "HEAD:refs/heads/master",
    "main branch": "master"
}

objects = {"branch made": False}
try:
    objects["repo"] = git.Repo()
except git.exc.InvalidGitRepositoryError:
    objects["branch made": True]
    objects["repo"] = git.Repo.init()
    origin = repo.create_remote(strings["temp branch"], strings["repo link"])
    origin.fetch()
    repo.create_head(strings["main branch"], origin.refs.master)
    repo.heads.master.checkout(True)
## Setup - end ##
