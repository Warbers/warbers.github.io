github_uname = f"warbers"
github_repos = f"https://github.com/{github_uname}/"
github_pages = f"https://{github_uname}.github.io/"

projects = [
    {
        "title": "Github Pages",
        "subtitle": "warbers.github.io",
        "demo_link": github_pages,
        "desc": "You are here right now",
        "progress_p": 5,
    },
    {
        "title": "Lexer",
        "repo_link": github_repos + "lexer",
        "desc": "My lexer that still needs a lot of work",
        "progress_p": 30,
    },
    {
        "title": "RISC16",
        "repo_link": github_repos + "risc16",
        "demo_link": "/cpu.html",
        "desc": "RiSC 16 emulator written is javascript",
        "progress_p": 25
    }
]

import json

with open("projects.json", "w+") as f:
    json.dump(projects, f)