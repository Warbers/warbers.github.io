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
        tokens.append({"t":"plain" ,"val":projs})
        projs = ""
    else:
        end = projs.find("%!")
        if end == -1:
            raise SyntaxError
        if idx != 0:
            tokens.append({"t":"plain" ,"val":projs[:idx]})
        tokens.append({"t":"template" ,"val":projs[idx+2:end].strip})
        projs = projs[end+2:]

print(tokens)

ast = {"root": []}

def parse_template_tok(t_val: str):
    elems = [proc.strip() for proc in t_val.split(" ")]
    if elems[0] == "for-each":
        tok_for = {"t":"for-each","iter_val": elems[1],"iter_arr": elems[3]}

def parse_root():
    while len(tokens) > 0:
        tok = tokens.pop(0)
        if tok["t"] == "plain":
            ast["root"].append(tok)
        elif tok["t"] == "template":
            ast["root"].append(parse_template_tok(tok["val"]))


parse_root()

print(projs)
with open("projects.html", "w+") as f:
    f.write(header)
    f.write(projs)
    f.write(footer)