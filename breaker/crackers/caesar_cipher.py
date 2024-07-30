'''
impletation of the caesar cipher
nothing fancy, an example input from the api would be:

'''
from string import ascii_lowercase

def c_cipher(text: str, rotations: int, direction: bool = True) -> str:
    # clean our input text and turn it into a list
    text = list(text.strip().lower())
    # neg our rotations if our direction isn't forwards(true)
    if not direction:
        rotations *= -1
    
    for idx in range(len(text)):
        # if our cur letter is not a letter, ignore it
        if text[idx] not in ascii_lowercase:
            continue
        
        # get the starting idx of the letter in the alpha
        start_point = ascii_lowercase.index(text[idx])
        
        # change our curr letter to the new one based off the start
        # we mod it to ensure that loops, well loop.
        text[idx] = ascii_lowercase[(start_point + rotations) % 26]

    # after the loop ends, return the list joined into a string
    return ''.join(text)
    
    
