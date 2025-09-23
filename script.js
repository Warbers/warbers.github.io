function onloaddo(f) {
    if (document.readyState == "loading") {
        document.addEventListener("DOMContentLoaded", f);
    } else {
        f();
    }
}

const finished = "finished";
const unfinished = "unfinished";

const github_uname = "warbers";
const github_repos = `https://github.com/${github_uname}/`;
const github_pages = `https://${github_uname}.github.com/`;

const rawContent = (base) => "https://raw.githubusercontent.com/Warbers/" + base + "/master/README.md";

function readTextFile(file, callback)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.setRequestHeader("Accept", "text/html, */*; q=0.01");
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                callback(rawFile.responseText)
            }
        }
    }
    rawFile.send(null);
}

function getTasks(el, fn) {
    readTextFile(rawContent(el.title), fn);
}

function gen_tasks(num_fin, num_unfin) {
    let tasks = [];
    for (let index = 0; index < num_fin; index++) {
        tasks.push({state: finished});
    }
    for (let index = 0; index < num_unfin; index++) {
        tasks.push({state: unfinished});
    }
    return tasks;
}

let projects = [
    // {
    //     title: "Github Pages", 
    //     link: "https://warbers.github.io",
    //     desc: "You are here right now",
    //     tasks: gen_tasks(3, 4),
    // },
    {
        title: "Github Pages",
        subtitle: "warbers.github.io",
        demo_link: github_pages,
        desc: "You are here right now",
        progress_p: 5,
    },
    {
        title: "Lexer",
        repo_link: github_repos + "lexer",
        desc: "My lexer that still needs a lot of work",
        progress_p: 30,
    },
    {
        title: "RISC16",
        repo_link: github_repos + "risc16",
        demo_link: "/cpu.html",
        desc: "RiSC 16 emulator written is javascript",
        progress_p: 25,
    },
    // {
    //     title: "idk", 
    //     link: "https://google.com",
    //     desc: "You are here right now",
    //     tasks: gen_tasks(2, 3),
    // },
];

function compareTask(a, b) {
    if (a.state == b.state) {
        return 0;
    }
    if (a.state == unfinished) {
        return 1;
    }
    return -1;
}

function createProgressBarB(e) {
    let base = document.createElement("div");
    base.className = "bprogress-bar";
    getTasks(e, (t) => {
        let tasks = t.split("\n")
                        .filter((s) => s.startsWith("- ["))
                        .map(s => {
                            return {
                                state: (s.toLowerCase().startsWith("- [x") ? finished : unfinished),
                                desc: s.substring(s.indexOf("]") + 1),
                            }
                        })
                        .sort(compareTask);
        tasks.forEach((task) => {
            let prog = document.createElement("div");
            prog.className = task.state;
            prog.title = task.desc;
            base.appendChild(prog);
        });
    });
    return base;
    e.tasks.forEach((task) => {
        let prog = document.createElement("div");
        prog.className = task.state;
        base.appendChild(prog);
    });
    return base;
    
    const numTasks = e.numTasks;
    const tasksDone = e.tasksDone;
    for (let index = 0; index < tasksDone; index++) {
        let prog = document.createElement("div");
        prog.className = "finished";
        base.appendChild(prog);
    }
    for (let index = tasksDone; index < numTasks; index++) {
        let prog = document.createElement("div");
        prog.className = "unfinished";
        base.appendChild(prog);
    }
    return base;
}

function createSimpleProgressBar(progress) {
    let prog = document.createElement("div");
    prog.style.width = progress + "%";
    let base = document.createElement("div");
    base.className = "progress-bar";
    base.appendChild(prog);
    return base;
}

onloaddo(() => {
    let card_cont = document.getElementById("card-container");
    projects.forEach((el) => {
        let header = document.createElement("h2");
        header.innerText = el.title;
        let desc = document.createElement("p");
        desc.innerText = el.desc;
        let card = document.createElement("div");
        card.className = "card";
        card.appendChild(header);
        if (el.subtitle) {
            let subt = document.createElement("h3");

            subt.innerText = el.subtitle;
            card.appendChild(subt);
        }
        if (el.demo_link) {
            let demo_txt = document.createElement("p");
            demo_txt.innerHTML = "Link to demo: <a href = \"" + el.demo_link + "\">" + el.demo_link + "</a>";
            card.appendChild(demo_txt);
        }
        card.appendChild(desc);
        if (el.repo_link) {
            let repo_txt = document.createElement("p");
            repo_txt.innerHTML = "Repository: <a href = \"" + el.repo_link + "\">" + el.repo_link + "</a>";
            card.appendChild(repo_txt);
        }
        if (el.progress_p) {
            card.appendChild(createSimpleProgressBar(el.progress_p));
        }
        card_cont.appendChild(card);
    });
});