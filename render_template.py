with open("footer.template", "r+") as f:
    footer = f.read()

with open("header.template", "r+") as f:
    header = f.read()
    
with open("projects.template", "r+") as f:
    projs = f.read()

syms = [
    "array-file",
    "for-each",
    "end-for",
    "out",
    "if-exists",
    "end-if",
]

tokens = []

while projs != "":
    idx = projs.find("!%")
    if idx == -1:
        tokens.append({"t":"plain" ,"val":projs.strip()})
        projs = ""
    else:
        end = projs.find("%!")
        if end == -1:
            raise SyntaxError
        if idx != 0:
            tokens.append({"t":"plain" ,"val":projs[:idx].strip()})
        tokens.append({"t":"template" ,"val":projs[idx+2:end].strip()})
        projs = projs[end+2:]

# print(tokens)

ast = {"root": []}

def parse_template_tok(t_val: str):
    elems = [proc.strip() for proc in t_val.split(" ")]
    if elems[0] == "for-each":
        tok_for = {"t":"for-each","iter_var": elems[1],"iter_arr": elems[3]}
        tok_stmts = []
        while len(tokens) > 0:
            next = parse_root()
            if next["t"] == "end-for":
                tok_for["stmts"] = tok_stmts
                return tok_for
            tok_stmts.append(next)
        raise SyntaxError
    elif elems[0] == "end-for":
        return {"t": "end-for"}
    elif elems[0] == "array-file":
        return {"t": "array-file", "file": elems[1], "arr": elems[3]}
    elif elems[0] == "out":
        return {"t": "out", "var": elems[1]}
    elif elems[0] == "if-exists":
        tok_if = {"t":"if-exists", "var": elems[1]}
        tok_stmts = []
        while len(tokens) > 0:
            next = parse_root()
            if next["t"] == "end-if":
                tok_if["stmts"] = tok_stmts
                return tok_if
            tok_stmts.append(next)
        raise SyntaxError
    elif elems[0] == "end-if":
        return {"t": "end-if"}
    else:
        print(t_val)
        raise SyntaxError


def parse_root():
    tok = tokens.pop(0)
    if tok["t"] == "plain":
        return tok
    elif tok["t"] == "template":
        return parse_template_tok(tok["val"])

while len(tokens) > 0:
    ast["root"].append(parse_root())

vars = {}

def check_var(v):
    if "." in v:
        parts = v.split(".")
        next_var = vars
        for part in parts:
            if part not in next_var:
                print(part)
                return False
            next_var = next_var[part]
        return True
    return v in vars

def get_var(v) -> dict | str | None:
    if "." in v:
        parts = v.split(".")
        next_var = vars
        for part in parts:
            if part not in next_var:
                return None
            next_var = next_var[part]
        return next_var
    return vars[v]

def gen_tok(tok) -> str:
    if tok["t"] == "root":
        return "\n".join(gen_tok_arr(tok["root"]))
    elif tok["t"] == "plain":
        return tok["val"]
    elif tok["t"] == "if-exists":
        if check_var(tok["var"]):
            return "".join(gen_tok_arr(tok["stmts"]))
        return ""
    elif tok["t"] == "array-file":
        import json
        vars[tok["arr"]] = json.load(open(tok["file"][1:-1], "r+"))
        return ""
    elif tok["t"] == "out":
        return str(get_var(tok["var"]))
    elif tok["t"] == "for-each":
        out_arr = []
        for val in get_var(tok["iter_arr"]):
            vars[tok["iter_var"]] = val
            out_arr += gen_tok_arr(tok["stmts"])
        return "\n".join(out_arr)
    else:
        print(tok)
        raise SyntaxError


def gen_tok_arr(arr) -> list[str]:
    out_arr = []
    for tok in arr:
        res = gen_tok(tok)
        if res is None:
            print(tok)
            raise SyntaxError
        out_arr.append(res)
    return out_arr

ast["t"] = "root"

projs = gen_tok(ast)
print(gen_tok(ast))
with open("projects.html", "w+") as f:
    f.write(header)
    f.write(projs)
    f.write(footer)