header = """\
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
    <!-- <script src="script.js"></script> -->
</head>
<body>
"""

footer = """\
    <div class="card">
        <h1>Pledge of Bloatfree Software</h1>
        <p>
            I hereby pledge that I will, to the best of my ability:
            <ul>
                <li>- try to actively and continuously reduce bloat and;</li>
                <li>- be mindful of efficiency, speed, and environmental and material cost</li>
            </ul>
                In all of:
            <ul>
                <li>- the software that I write and;</li>
                <li>- the hardware I design and;</li>
                <li>- the specifications that I write.</li>
            </ul>
        </p>
        <p>This is not lawfully binding of course, the point of this pledge is to put my mind at ease about the waste that occurs in our finite world. You are welcome to scrutinise me and offer (kind) criticism, and feedback, for all the materials and stuff that I produce. I know that I have much to learn.</p>
        <p>This pledge is part of my beginnings of acting instead of just thinking.</p>
        <p>We not only have to think about how much we waste, we also have to do something about it.</p>
    </div>
</body>
</html>
"""

import json

projects = json.load(open("projects.json", "r+"))

proj_html = ""

indent_spacing = 1

default_indent = "    "

base_spacing = default_indent * indent_spacing
proj_html += f"{base_spacing}<div id=\"card-container\">\n"

def get_project_card(project, indent):
    spacing = default_indent * indent
    out_html = []
    out_html.append(f"<h2>{project["title"]}</h2>")
    if "subtitle" in project:
        out_html.append(f"<h3>{project["subtitle"]}</h3>")
    if "demo_link" in project:
        out_html.append(f"<p>Link to demo: <a href=\"{project["demo_link"]}\">{project["demo_link"]}</a></p>")
    out_html.append(f"<p>{project["desc"]}</p>")
    if "repo_link" in project:
        out_html.append(f"<p>Repository link: <a href=\"{project["repo_link"]}\">{project["repo_link"]}</a></p>")
    if "progress_p" in project:
        out_html.append(f"""<div class="progress-bar"><div style="width:{project["progress_p"]}%;"></div></div>""")

    return f"\n".join([f"{spacing}{ele}" for ele in out_html])


def get_project_card_div(project, indent):
    spacing = default_indent * indent
    out_html = []
    out_html.append(f"<div class=\"card\">")
    out_html.append(get_project_card(project, indent + 1))
    out_html.append("</div>")
    return f"\n".join([f"{spacing}{ele}" for ele in out_html])


for project in projects:
    proj_html += get_project_card_div(project, indent_spacing + 1)

proj_html += f"{base_spacing}</div>\n"

print(header)
print(proj_html)
print(footer)

a_proj_html = """\
!% for-each project in projects %!
    <div class="card">
    <h2>!% out project.title %!</h2>

    !% if-exists project.subtitle %!
        <h3>!% out project.subtitle %!</h3>
    !% end-if %!

    !% if-exists project.demo_link %!
        <p>Link to demo: <a href="!% out project.demo_link %!">!% out project.demo_link %!</a></p>
    !% end-if %!

    <p>!% out project.desc %!</p>

    !% if-exists project.repo_link %!
        <p>Repository link: <a href="!% out project.repo_link %!">!% out project.repo_link %!</a></p>
    !% end-if %!
    !% if-exists project.progress_p %!
        <div class="progress-bar">
            <div style="width:!% out project.progress_p%!%;"></div>
        </div>
    !% end-if %!

    </div>
!% end-for %!

</div>
"""