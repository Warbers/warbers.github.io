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

def get_prettyfied_plaintext(txt: str):
    spl = txt.split("\n")
    remain = [el.strip() for el in spl if el.strip() != ""]
    return "\n".join(remain)

while projs != "":
    idx = projs.find("!%")
    if idx == -1:

        tokens.append({"t":"plain" ,"val":projs})
        projs = ""
    else:
        end = projs.find("%!")
        if end == -1:
            raise SyntaxError
        if idx != 0:
            tokens.append({"t":"plain" ,"val":projs[:idx]})
        tokens.append({"t":"template" ,"val":projs[idx+2:end].strip()})
        projs = projs[end+2:]

# print(tokens)

ast = {"root": []}

def parse_template_tok(t_val: str):
    elems = [proc.strip() for proc in t_val.split(" ")]
    if elems[0] == "for-each":
        for_tok = {"t":"for-each","iter_var": elems[1],"iter_arr": elems[3], "stmts": []}
        while len(tokens) > 0:
            tok = parse_single()
            if tok["t"] == "end-for":
                return for_tok
            for_tok["stmts"].append(tok)
        raise SyntaxError("missing end-for")
    elif elems[0] == "if-exists":
        if_tok = {"t":"if-exists","var": elems[1], "stmts": []}
        while len(tokens) > 0:
            tok = parse_single()
            if tok["t"] == "end-if":
                return if_tok
            if_tok["stmts"].append(tok)
        raise SyntaxError("missing end-if")
    elif elems[0] == "end-for":
        return {"t":"end-for"}
    elif elems[0] == "end-if":
        return {"t":"end-if"}
    elif elems[0] == "out":
        return {"t": "out", "var": elems[1]}
    elif elems[0] == "array-file":
        return {"t": "array-file", "file": elems[1], "arr": elems[3]}
    raise SyntaxError("Unknown syntax " + elems[0])

def parse_single():
    tok = tokens.pop(0)
    if tok["t"] == "plain":
        return tok
    elif tok["t"] == "template":
        return parse_template_tok(tok["val"])
    else:
        raise SyntaxError


def parse_root():
    outp = []
    while len(tokens) > 0:
        outp.append(parse_single())
    return outp

eval_vars = {}

def get_var(v: str):
    parts = v.split(".")
    next_lvl = eval_vars
    for part in parts:
        if part not in next_lvl:
            return None
        next_lvl = next_lvl[part]
    return next_lvl

import json

def eval_single(el):
    if el["t"] == "plain":
        return [el["val"]]
    elif el["t"] == "array-file":
        eval_vars[el["arr"]] = json.load(open(el["file"], "r+"))
        return ["<!-- included '" + el["file"] + "' -->"]
    elif el["t"] == "out":
        return [str(get_var(el["var"]))]
    elif el["t"] == "for-each":
        eval_stmts = []
        iter_arr = get_var(el["iter_arr"])
        for iter_var in iter_arr: # type: ignore
            eval_vars[el["iter_var"]] = iter_var
            eval_stmts += eval_arr(el["stmts"])
        return eval_stmts
    elif el["t"] == "if-exists":
        eval_stmts = []
        eval_var = get_var(el["var"])
        if eval_var != None:
            return eval_arr(el["stmts"])
        return []

    else:
        raise NotImplementedError


def eval_arr(ast):
    out_p = []
    for el in ast:
        out_p += eval_single(el)
    return out_p

base_stmts = parse_root()
ast["root"] = parse_root()

strs = eval_arr(base_stmts)
strs = "".join(strs).split("\n")
strs = [el for el in strs if el.strip() != ""]


with open("raw.html", "w+") as f:
    f.write(get_prettyfied_plaintext("".join(strs)))

with open("raw.json", "w+") as f:
    json.dump(strs, f, indent=4)

with open("lexer.json", "w+") as f:
    json.dump(base_stmts, f, indent=4)



with open("projects.html", "w+") as f:
    f.write(header)
    f.write("\n".join(strs))
    f.write(footer)