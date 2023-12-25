# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

#typing for visibility
x: int
m: int
a: int
s: int

SUI = input.index('')
workflows_in = input[:SUI]
parts_in = input[SUI+1:]
workflows = {}

def create_exp(content):

    # if no condition just return new workflow/R/A
    if content.count(":") == 0:
        return compile(f"\"{content}\"", '<string>', 'eval')

    cs = content.split(":")
    condition = cs[0]
    end_state = cs[1]
    return compile(f"\"{end_state}\" if {condition} else None", '<string>', 'eval')

# init
for wf in workflows_in:
    wfs = wf.split("{")
    name = wfs[0]
    contents = wfs[1][:-1].split(",")

    # each workflow contains list of compiled expressions which after evaluation
    # return new workflow, Accept state, Reject state or None (which
    # means that next compiled expression should be run)
    workflows[name] = [create_exp(content) for content in contents]

# evaluation
ans = 0
for part in parts_in:
    part = part[1:-1]
    part = part.split(",")
    for var in part:
        exec(var)
    
    wf_name = "in"
    # go through workflows
    while wf_name != 'A' and wf_name != 'R':
        wfc = workflows[wf_name]
        for wf in wfc:
            wf_name = eval(wf)
            if wf_name != None:
                break
    
    if wf_name == "A":
        ans += x + m + a + s

print(ans)
