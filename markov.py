"""Generate Markov text from text files."""

#from random import choice
import random
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    #opens file
    file = open(file_path)
    #reads entire file and sets to text_string
    text_string = file.read()
    file.close()

    #cleans the text string
    text_string = text_string.replace("\n", " ")
    text_string = text_string.replace("\t", " ")
    text_string = text_string.replace('  ', ' ')
    text_string = text_string.strip()


    return text_string


def make_chains(text_string, n_gram):
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
    
    #creates list of words from text string to iterate over
    text_list = text_string.split(" ")

    #iterates over the text_list, minus n_grams to prevent 
    #out of index error
    list_len = len(text_list)
    for i in range(list_len - n_gram):
        #creates a tuple with a length of n_gram
        key = [text_list[i + n ] for n in range(n_gram)]
        key = tuple(key)# = (text_list[i], text_list[i+1])
        #if the key does not yet exist in dict
        #initialize a list and add a ele from text_list
        #with an index of i + n_gram
        if chains.get(key, 0) == 0:
            chains[key] = [text_list[i + n_gram]] 
        #if it does exist just append the list with 
        #ele from the index i + n_gram
        else:    
            chains[key].append(text_list[i + n_gram])

   
    return chains


def make_text(chains):
    """Return text from chains."""
    words = []
    punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', ' ', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    #grab the starting tuple
    curr_key = random.choice(list(chains.keys())) # tuple

    #makes sure the starting key is capital and not punctuation
    while curr_key[0][0].islower() or curr_key[0][0] in punct: 
        curr_key = random.choice(list(chains.keys()))
    # print(type(curr_key))

    #get the length of the tuple
    n_gram = len(curr_key)

    #add the first key to the words list
    words.extend([curr_key[i] for i in range(n_gram)])

    #keeps looping while building words list
    while True:
        #grabs the next word value from chains dict
        to_append = random.choice(chains[curr_key]) # string
        #add the word to the words list
        words.append(to_append)
        #sets the next key using index 1 - n of tuple
        next_key = [curr_key[i] for i in range(1, n_gram)]
        #adds the next word value from chains dict to end of new key
        next_key.append(to_append)
        next_key = tuple(next_key)
        #if the next key exists, set the next key to the current key
        if next_key in chains:
            curr_key = next_key
        #otherwise we are done and can break out of the loop
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
    chains = make_chains(input_text, n_gram_size)

    # Produce random text
    random_text = make_text(chains)

    print(random_text)
