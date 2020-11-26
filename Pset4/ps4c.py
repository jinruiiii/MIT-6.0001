# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy = self.valid_words
        return copy
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # Create a variables to store the length of vowels and consonants
        CONSONANTS_length = len(CONSONANTS_LOWER)
        VOWEL_length = len(VOWELS_LOWER)
        # Initialize a transpose dict
        map_dict = {}
        # Map each lowercase and uppercase vowel to their respective shuffled vowel based on the cipher
        for i in range(VOWEL_length):
            map_dict[VOWELS_LOWER[i]] = vowels_permutation[i]
            map_dict[VOWELS_UPPER[i]] = vowels_permutation[i].upper()
        # Append Cononants into the transpose dict, ensuring that key == vlaue    
        for j in range(CONSONANTS_length):
            map_dict[CONSONANTS_LOWER[j]] = CONSONANTS_LOWER[j]
            map_dict[CONSONANTS_UPPER[j]] = CONSONANTS_UPPER[j]
        return map_dict 

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        # Initialize encrypted_text
        encrypted_text = ""
        # Loop through every char in the plaintext
        for char in self.get_message_text():
            # if char is an alphabet, apply the cipher
            if char in transpose_dict:
                encrypted_text += transpose_dict[char]
            # if not, just append the char into the encrypted_text    
            else:
                encrypted_text += char
        return encrypted_text


        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # Get list of all the different permutations for the vowels
        permutations_list = get_permutations(VOWELS_LOWER)
        # Inititalizing a list that will have elements of the transpose dictionary
        transpose_list = []
        # Initialize a dict with key = 'decrypted' text and value = number of valid words
        decrypt_perms_dict = {}
        # Initialize a dict with key = 'decrypted' text and value = words in the 'decrypted text'
        words_dict = {}
        # Get all the permutations of the vowels and append them into tranpose_list
        for element in permutations_list:
            transpose_list.append(self.build_transpose_dict(element))
        # Initialize number of valid words (value) as 0 with key being the 'decrypted' text   
        for element in transpose_list:
            decrypt_perms_dict[self.apply_transpose(element)] = 0
        # Alogorithm used to append testing_text_list with words as elements    
        for key in decrypt_perms_dict:
            length = len(key)
            counter = 0
            words_dict[key] = []
            for i in range(length):
                if key[i].isalpha() == False:
                    if counter > 0:
                        words_dict[key].append(key[i - counter: i])
                    counter = 0
                elif key[i].isalpha() == True:
                    if i == length - 1:
                       words_dict[key].append(key[i - counter: i + 1])  
                    counter = counter + 1
        # For each valid word in words_dict[key], increment counter
        # Set the final counter value as the value of decrypt_perms_dict            
        for key in words_dict:
            counter1 = 0
            for element in words_dict[key]:
                for word in self.get_valid_words():
                    if element == word:
                        counter1 = counter1 + 1
                        break
            decrypt_perms_dict[key] = counter1
        # Search alogorithm to find the key in decrypt_perms_dict that has the highest value(valid words)    
        for key in decrypt_perms_dict:
            if decrypt_perms_dict[key] == max(decrypt_perms_dict.values()):
                return key            





        
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Today is a good day for badminton!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Tudey is e guud dey fur bedmintun!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
