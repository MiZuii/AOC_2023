# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
input = inputf.read().split("\n")
inputf.close()
# -------------------------------- PUZZLE CODE ------------------------------- #

from interval3 import Interval, IntervalSet
from collections import defaultdict
from functools import reduce

CTOI = {'x': 0, 'm': 1, 'a': 2, 's': 3}
SUI = input.index('')
workflows_in = input[:SUI]
workflows = defaultdict(lambda : [0, [], set(), []])

def calc_comb(subsets_arr):

    def subset_comb(ss):
        return reduce(lambda val, s: val *((s.upper_bound() if s.upper_closed() else s.upper_bound() - 1) \
                                           - (s.lower_bound() if s.lower_closed() else s.lower_bound() + 1) + 1), ss, 1)

    return sum([subset_comb(subset) for subset in subsets_arr])

def get_intervals_from_exp(exp):
    if exp[1] is None:
        return (None, None, None, None), (None, None, None, None)

    var = exp[1][0]
    to_next = [None, None, None, None]
    to_next[CTOI[var]] = IntervalSet([Interval.greater_than(int(exp[1][2:]))]) if exp[1][1] == '>' else IntervalSet([Interval.less_than(int(exp[1][2:]))])
    
    to_this = [None, None, None, None]
    to_this[CTOI[var]] = IntervalSet([Interval.greater_than_or_equal_to(int(exp[1][2:]))]) if exp[1][1] == '<' else IntervalSet([Interval.less_than_or_equal_to(int(exp[1][2:]))])

    return tuple(to_next), tuple(to_this)

def intervals_and(i1, i2):
    ni = lambda x: i1[x] & i2[x] if ((i1[x] is not None) and (i2[x] is not None)) else (i1[x] if (i2[x] is None) else (i2[x] if i1[x] is None else None))
    return ni(0), ni(1), ni(2), ni(3)

def intervals_or(i1, i2):
    ni = lambda x: i1[x] | i2[x] if ((i1[x] is not None) and (i2[x] is not None)) else (i1[x] if (i2[x] is None) else (i2[x] if i1[x] is None else None))
    return ni(0), ni(1), ni(2), ni(3)

# parse input
for wf in workflows_in:
    wfs = wf.split("{")
    name = wfs[0]
    contents = wfs[1][:-1]
    conts = contents.split(",")
    for content in conts:
        if content.count(":") == 0:
            workflows[name][2].add(content)
            workflows[name][3].append((content, None))
        else:
            cs = content.split(":")
            workflows[name][2].add(cs[1])
            workflows[name][3].append((cs[1], cs[0]))


# perform topologic sort
q = []
def visit(node):
    # uses global q and workflows
    global q
    global workflows
    workflows[node][0] = 1

    for child in workflows[node][2]:
        if workflows[child][0] == 0:
            visit(child)

    q.append(node)
visit("in")

# prep in workflow
workflows["in"][1].append((IntervalSet([Interval(1, 4000, closed=True)]),
                           IntervalSet([Interval(1, 4000, closed=True)]),
                           IntervalSet([Interval(1, 4000, closed=True)]),
                           IntervalSet([Interval(1, 4000, closed=True)])))

# calc intervals
q.reverse()
for wf in q:
    for exp in workflows[wf][3]:
        to_next_wf, to_update = get_intervals_from_exp(exp)
        update_arr = []

        for subset in workflows[wf][1]:
            ns = intervals_and(subset, to_next_wf)
            workflows[exp[0]][1].append(ns)

            update_arr.append(intervals_and(subset, to_update))

        workflows[wf][1] = update_arr

print(calc_comb(workflows['A'][1]))
