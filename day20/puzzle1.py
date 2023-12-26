# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from collections import defaultdict
from functools import reduce

FLIP_FLOP = 0
CONJUNCTION = 1
BROADCASTER = 2

LOW = 0
HIGH = 1

nodes = defaultdict(lambda : [0, [], []])

def state_to_int(state: dict):
    return int(reduce(lambda rep, val: (rep + str(val) if (type(val) != dict) else \
                    rep + reduce(lambda rep, val: rep + str(val), val.values(), ""))
                  , state.values(), ""), base=2)

for line in input:
    if line[0] == "%" or line[0] == "&":
        sl = line.split(" ")
        name = sl[0][1:]
        nodes[name][0] = CONJUNCTION if line[0] == "&" else FLIP_FLOP
        for next in sl[2:]:
            if next[-1] == ",":
                next = next[:-1]
            nodes[name][1].append(next)
            nodes[next][2].append(name)
    else:
        sl = line.split(" ")
        name = sl[0]
        nodes[name][0] = BROADCASTER
        for next in sl[2:]:
            if next[-1] == ",":
                next = next[:-1]
            nodes[name][1].append(next)
            nodes[next][2].append(name)

signals = []
state = {key: ( LOW if (item[0] == FLIP_FLOP or item[0] == BROADCASTER) \
                    else {key: LOW for key in item[2]} )
            for key, item in nodes.items()}
ss = []
f = False

lsans = []
hsans = []
for iter in range(1000):

    # simulate one press while counting the signals
    hs = 0
    ls = 0

    # signals repr
    # (pulse type [LOW/HIGH], receiver, sender)

    # button push
    signals.append((LOW, 'broadcaster', 'button'))
    
    # simulate
    while signals:

        signal = signals.pop(0)

        # update counters
        if signal[0] == LOW:
            ls += 1
        else:
            hs += 1

        # simulate
        module_type = nodes[signal[1]][0]
        if module_type == FLIP_FLOP:

            # flip flops skip high signals
            if signal[0] == HIGH:
                continue

            ff_state = state[signal[1]]
            new_state = LOW if ff_state == HIGH else HIGH
            state[signal[1]] = new_state
            for next_module in nodes[signal[1]][1]:
                signals.append((new_state, next_module, signal[1]))

        elif module_type == CONJUNCTION:

            # update state first
            state[signal[1]][signal[2]] = signal[0]

            new_sig = LOW if all(state[signal[1]].values()) else HIGH
            for next_module in nodes[signal[1]][1]:
                signals.append((new_sig, next_module, signal[1]))

        else:   # module_type == BROADCASTER
            
            # resend for all
            for next_module in nodes[signal[1]][1]:
                signals.append((signal[0], next_module, signal[1]))

    state_int = state_to_int(state)

    # check for brake condition
    if state_int in ss and iter < 500:
        ss.append(state_int)
        lsans.append(ls)
        hsans.append(hs)
        f = True
        break

    # update states set and ans arrays
    ss.append(state_int)
    lsans.append(ls)
    hsans.append(hs)

if f:
    li = ss.index(ss[-1])   # loop start index

    print(ss, li)

    preh = hsans[:li]       # high pulse counters prefix
    prel = lsans[:li]       # low pulse counters prefix

    lhs = hsans[li:-1]      # high pulse loop counters
    lls = lsans[li:-1]      # low pulse loop counters

    for i in range(1000 - len(preh)):
        preh.append(lhs[i % len(lhs)])
        prel.append(lls[i % len(lls)])

    print(sum(preh) * sum(prel))
else:
    print(sum(lsans) * sum(hsans))