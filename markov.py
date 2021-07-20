"""Generate Markov text from text files."""

#from random import choice
import random
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """


    file = open(file_path)
    text_string = file.read().replace("\n", " ").rstrip()
    file.close()

    return text_string


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    
    chains = {}
    text_list = text_string.split(" ")
    list_len = len(text_list)
    for i in range(list_len-2):
        key = (text_list[i], text_list[i+1])
        if chains.get(key, 0) == 0:
            chains[key] = [text_list[i+2]] 
        else:    
            chains[key].append(text_list[i+2])
   
    return chains



def make_text(chains):
    """Return text from chains."""
    words = []
    curr_key = random.choice(list(chains.keys()))
    words.extend([curr_key[0],curr_key[1]])
    while True:
        to_append = random.choice(chains[curr_key])
        words.append(to_append)
        next_key = (curr_key[1], to_append)
        if next_key in chains:
            curr_key = next_key
        else:
            break

    return ' '.join(words)


if __name__ == '__main__':
    
    argv = sys.argv[1]
    input_path = argv

    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)

    # Get a Markov chain
    n_gram_size = 2
    chains = make_chains(input_text)

    # Produce random text
    random_text = make_text(chains)

    print(random_text)
