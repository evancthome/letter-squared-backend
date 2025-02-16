#MIT License

#Copyright (c) 2022 Lucas Lingle

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


from typing import List, Dict, Tuple, Optional
import copy
import random
import numpy as np
import argparse

count = 0


def has_contiguous_repeat(w: str):
    for i in range(0, len(w) - 1):
        if w[i] == w[i + 1]:
            return True
    return False


def read_words(wordlist_fp: str) -> List[str]:
    list_ = []
    with open(wordlist_fp, "r") as f:
        for line in f.readlines():
            list_.append(line.strip())
    set_ = {w.upper() for w in list_ if len(w) >= 3 and not has_contiguous_repeat(w)}
    return list(set_)


def search(
    s: str,
    state: Dict[str, int],
    last_side_id: int,
) -> Optional[Dict[str, int]]:
    """
    Performs search, assigning the letters of s to possible positions.
    If a successful layout for the entire string is found, it will be returned.

    :param s: String suffix yet to be assigned to sides.
    :param state: Dictionary mapping from characters to positions 0, ..., 11.
    :param last_side_id: Side ID assigned to previous character.
    :return: Final layout state or None.
    """
    global count
    count += 1

    # no letters left means it works.
    if len(s) == 0:
        return state

    # check if s[0] was seen earlier and thus already assigned somewhere.
    if s[0] in state:
        pos_id = state[s[0]]
        side_id = pos_id // 3
        # if this forced assignment causes the new letter to fall on the same side
        # as the previous letter, we have a problem.
        if side_id == last_side_id:
            return None
        return search(
            s=s[1:],
            state=copy.deepcopy(state),
            last_side_id=side_id,
        )

    # s[0] is a new character, so we assign it uniformly at random to any
    # open position that works, if there are any.
    blanks = set(range(12)) - (set(state.values()))
    blanks = list(blanks)
    random.shuffle(blanks)
    for pos_id in blanks:
        side_id = pos_id // 3
        # consecutive letters cannot be assigned to the same side.
        if side_id == last_side_id:
            continue
        # only three letters can only be assigned to a side.
        if len([k for k, v in state.items() if v // 3 == side_id]) == 3:
            continue

        # since there's nothing immediately preventing s[0] from being
        # assigned this position id, we continue our depth-first search.
        state_new = copy.deepcopy(state)
        state_new[s[0]] = pos_id
        final_state = search(
            s=s[1:],
            state=state_new,
            last_side_id=side_id,
        )
        if final_state is not None:
            return final_state

    # if none of the assignment suffixes for the given assignment prefix passed in work,
    # the prefix doesn't work.
    return None


def sample(wordlist_fp: str, verbose: bool) -> Tuple[str, str, Dict[str, int]]:
    w1list = read_words(wordlist_fp)
    w2list = copy.deepcopy(w1list)

    random.shuffle(w1list)
    random.shuffle(w2list)
    for w1 in w1list:
        for w2 in w2list:
            if w1[-1] != w2[0]:
                continue
            if len(set(w1 + w2)) != 12:
                continue
            if verbose:
                print(w1, w2)
            # we assign the first letter uniformly at random to any position.
            pos_id = np.random.randint(0, 12)
            side_id = pos_id // 3
            final_state = search(
                s=w1[1:] + w2[1:], state={w1[0]: pos_id}, last_side_id=side_id
            )
            if final_state is not None:
                return w1, w2, final_state
    raise ValueError("Couldn't find any combo with the given wordlist.")


def render(final_state: Dict[str, int]) -> Dict[str, List[str]]:
    """
    Returns a dictionary containing the letters organized by side.
    
    Returns:
        Dict with keys 'north', 'east', 'south', 'west' containing lists of letters
        for each side in position order.
    """
    north = [k for k, v in final_state.items() if v // 3 == 0]
    east = [k for k, v in final_state.items() if v // 3 == 1]
    south = [k for k, v in final_state.items() if v // 3 == 2]
    west = [k for k, v in final_state.items() if v // 3 == 3]
    
    # Sort letters by position within each side
    north.sort(key=lambda x: final_state[x] % 3)
    east.sort(key=lambda x: final_state[x] % 3)
    south.sort(key=lambda x: final_state[x] % 3)
    west.sort(key=lambda x: final_state[x] % 3)
    
    return {
        'north': north,
        'east': east,
        'south': south,
        'west': west
    }


if __name__ == "__main__":
    # Comment out or remove the command line interface code
    pass

    

