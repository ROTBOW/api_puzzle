'''
    Implimention of Affine cipher,
    how should I hint this one?
    
    Author: ROTBOW
    Date: August 13th, 2024
'''
from string import ascii_lowercase


def affine_encode(imp_text: str, a: int, b: int) -> str:
    # (ax + b) modM
    text: list[str] = list(imp_text.lower())
    formula = lambda x: (a * x) + b
    
    for idx in range(len(text)):
        # use index on our letters to get the idx of the cur letter
        # then we mod it by 26 (total amount of our letters)
        new_idx = formula(ascii_lowercase.index(text[idx])) % 26
        
        # after we use the new idx to reassign the encoded letter
        text[idx] = ascii_lowercase[new_idx]
        
    return ''.join(text)