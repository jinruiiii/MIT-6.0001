# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words("words.txt")

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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # Initializing a dictionary
        shift_dict = {}
        total_letters = 26
        ASCII_A = 65
        ASCII_a = 97
        # Looping over each uppercase letter
        for i in range(total_letters):
            # Looping shift + 1 times
            for j in range(shift + 1):
                # If letter not in dict, add the letter to the dict and give it a value of the letter
                if chr(ASCII_A + i) not in shift_dict:
                    shift_dict[chr(ASCII_A + i)] = chr(ASCII_A + i)
                # If value of key is "Z", change it to "A" to prevent the value from going beyond the ASCII numbers for uppercase letters    
                elif shift_dict[chr(ASCII_A + i)] == 'Z':
                    shift_dict[chr(ASCII_A + i)] = "A"
                # Increment the ASCII number by 1 for each iteration    
                else:
                    shift_dict[chr(ASCII_A + i)] = chr(ord(shift_dict[chr(ASCII_A + i)]) + 1)
        for i in range(total_letters):   
            # Looping shift + 1 times         
            for j in range(shift + 1):
                # If letter not in dict, add the letter to the dict and give it a value of the letter
                if chr(ASCII_a + i) not in shift_dict:
                    shift_dict[chr(ASCII_a + i)] = chr(ASCII_a + i)
                # If value of key is "z", change it to "a" to prevent the value from going beyond the ASCII numbers for lowercase letters    
                elif shift_dict[chr(ASCII_a + i)] == 'z':
                    shift_dict[chr(ASCII_a + i)] = "a"
                # Increment the ASCII number by 1 for each iteration       
                else:
                    shift_dict[chr(ASCII_a + i)] = chr(ord(shift_dict[chr(ASCII_a + i)]) + 1)        
        return shift_dict            
        

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        message = self.get_message_text()
        # Initializing a new variable that will contain the encrypted text
        new_message = ""
        # Making sure that every alphabets are encrypted
        for char in message:
            # Ensure that only the alphabets are encrypted
            if char in shift_dict:
                new_message += shift_dict[char]
            else:
                new_message += char 
        return new_message           


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # Call the Message constructor that was already created
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        copy = self.encryption_dict
        return copy
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        self.shift = shift

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text
 
        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # Initializing a dict that will contain keys = the shift value and 
        # values = the number of real words when the encrypted text is shifted by that value
        real_words_dict = {}
        # Assigning 27 to the total number of shifts, excluding 27 itself
        total_shifts = 27
        # Get the length of the encrypted text
        length = len(self.get_message_text())
        # Loop through all the different shifts values to see which shift value will yield the most number of real words
        for shift in range(total_shifts):
            # Assigning the "decrypted" string to testing_text
            testing_text = self.apply_shift(26 - shift)
            counter0 = 0
            counter1 = 0
            # Initializing a list that will contain all the words in the 'decrypted' text (testing_text) for each shift value 
            testing_text_list = []
            # Alogorithm used to append testing_text_list with words as elements
            for i in range(length):
                if testing_text[i].isalpha() == False:
                    if counter0 > 0:
                        testing_text_list.append(testing_text[i - counter0: i]) 
                    counter0 = 0        
                elif testing_text[i].isalpha() == True:
                    if i == length - 1:
                       testing_text_list.append(testing_text[i - counter0: i + 1])  
                    counter0 = counter0 + 1    
            # Using counter, count the number of real words in the testing_text_list for each shift value                           
            for word in testing_text_list:
                for element in self.get_valid_words():
                    if word == element:
                        counter1 = counter1 + 1
                        break
            # Adding the result into real_words_dict where key = shift value and value = total real words        
            real_words_dict[26 - shift] = counter1 
            # Get the key witht the greatest value and append it into a new tuple called best_shift_tuple
            for key in real_words_dict:
                if real_words_dict[key] == max(real_words_dict.values()):
                    best_shift_tuple = (key, self.apply_shift(key))
        return best_shift_tuple            


if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext1 = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext1.get_message_text_encrypted())
    print("")
    plaintext2 = PlaintextMessage('I love playing badminton, basketball and frisbee!', 2)
    print('Expected Output: K nqxg rncakpi dcfokpvqp, dcumgvdcnn cpf htkudgg!')
    print('Actual Output:', plaintext2.get_message_text_encrypted())
    print("")



    #Example test case (CiphertextMessage)
    ciphertext1 = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext1.decrypt_message())
    print("")
    ciphertext2 = CiphertextMessage('K nqxg rncakpi dcfokpvqp, dcumgvdcnn cpf htkudgg!')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext2.decrypt_message())

    ciphertext3 = CiphertextMessage('Xoqy Tzcfsm wg o amhvwqoz qvofoqhsf qfsohsr cb hvs gdif ct o acasbh hc vszd qcjsf ob wbgittwqwsbhzm dzobbsr voqy. Vs vog pssb fsuwghsfsr tcf qzoggsg oh AWH hkwqs pstcfs, pih vog fsdcfhsrzm bsjsf doggsr oqzogg. Wh vog pssb hvs hforwhwcb ct hvs fsgwrsbhg ct Sogh Qoadig hc psqcas Xoqy Tzcfsm tcf o tsk bwuvhg soqv msof hc sriqohs wbqcawbu ghirsbhg wb hvs komg, asobg, obr shvwqg ct voqywbu.')
    print(ciphertext3.decrypt_message())

    