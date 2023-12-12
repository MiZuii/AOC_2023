# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #
from functools import cmp_to_key

card_to_int = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def get_hand_pos(hand):
    # 1 - all 5, 2 - all 4, 3 - full, 4 - three, 5 - two pairs, 6 - one pair, 7 high
    hset = set(hand)
    set_q = len(hset)
    if set_q == 1:
        return 1
    elif set_q == 2:
        el_q = hand.count(hset.pop())
        if el_q == 1 or el_q == 4:
            return 2
        else:
            return 3
    elif set_q == 3:
        el_1 = hand.count(hset.pop())
        el_2 = hand.count(hset.pop())
        if el_1 == 2 or el_2 == 2:
            return 5
        else:
            return 4
    elif set_q == 4:
        return 6
    elif set_q == 5:
        return 7
    

def gte(hand1, hand2):
    # returns True if hand1 >= hand2
    # else returns False
    hand1_pos = get_hand_pos(hand1)
    hand2_pos = get_hand_pos(hand2)

    if hand1_pos < hand2_pos:
        return 1
    elif hand1_pos == hand2_pos:
        # calc for equal positions
        for h1c, h2c in zip(hand1, hand2):
            if card_to_int[h1c] > card_to_int[h2c]:
                return 1
            elif card_to_int[h1c] < card_to_int[h2c]:
                return -1
        return 0
    return -1

input = inputf.read().split("\n")
input.sort(key=cmp_to_key(lambda x, y: gte(x[:5], y[:5])))

print(sum([(mul + 1)*int(line[6:]) for mul, line in enumerate(input)]))

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()