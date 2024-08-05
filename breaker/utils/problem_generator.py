from ..crackers.caesar_cipher import c_cipher
from string import ascii_lowercase as letters
from random import randint
from .utils import create_hash


def caesar() -> tuple[str]:
    n = randint(100, 1000)
    # creating the problem string as an list, will convert it to string before shiping it off
    problem_str = list()
    
    for _ in range(n):
        problem_str += letters[randint(0, 25)]

    # hash the ans and write the hint
    problem_str = ''.join(problem_str)
    print('pure ans:', problem_str[:15])
    hashed_ans = create_hash(problem_str)
    hint = f'Caesar: first correct letter is {problem_str[0]}'
    
    problem = c_cipher(problem_str, randint(0, 25))
    
    
    return hint, problem, hashed_ans

def gen_problem(gate: int) -> tuple[str]:
    # this will call another func to gen that func's problem
    # each func will return a hint, the problem string and a hashed version of their answer
    # returned as a tuple
    problem =  {
        1: caesar
    }.get(gate, None)
    
    if not problem:
        return 'eh just return 1', '1'
    
    return problem()