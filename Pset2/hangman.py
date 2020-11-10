# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
        if char not in letters_guessed:
            return False
    return True        





def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    string_all_letters = "abcdefghijklmnopqrstuvwxyz"
    list_available_letters = []    
    for element in string_all_letters:
        if element not in letters_guessed:
            list_available_letters.append(element)
    string_available_letters = ""        
    for element in list_available_letters:
        string_available_letters += element
    return string_available_letters    
              
def unique_chars(secret_word):
    unique = []
    for char in secret_word:
        if char not in unique:
            unique.append(char)
    return len(unique)            
    
    
def no_more_guesses(guesses):
    if guesses == 0:
          print(f"Sorry, you ran out of guesses. The word was {secret_word}")
          return True    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    length_of_secret = len(secret_word)
    unique_letters = unique_chars(secret_word)         
    guessing = []
    for i in range(length_of_secret * 2):
        if i % 2 == 0:
            guessing.append("_")
        else:
            guessing.append(" ")    
    guesses = 6
    warnings = 3
    print("Welcome to hangman!")
    print(f'I am thinking of a word that is {length_of_secret} letters long.')
    letters_guessed = []
    while is_word_guessed(secret_word, letters_guessed) == False:
        print(f"You have {guesses} guesses left.")
        available_letters = get_available_letters(letters_guessed)
        print(f"Available letters: {available_letters}")
        letter = "!"
        correct_guess = False
        alph_input = True
        while letter.isalpha() == False:
            letter = input("Please guess a letter:  ")
            if letter.isalpha() == False:
                alph_input = False
                warnings = warnings - 1
                print(f"{letter} is not a valid letter. You have {warnings} warnings left!")
            elif letter in letters_guessed:
                alph_input = False
                warnings = warnings - 1
                print(f"You have already guessed this letter! You have {warnings} warnings left!") 
            if warnings == 0:
                alph_input = False
                guesses = guesses - 1
                if no_more_guesses(guesses) == True:
                    return 0
                print(f"You will be penalized for giving non-alphabetical inputs 3 times! You now have {guesses} guesses left. ")  
                warnings = 3   
        if alph_input == False:
            continue           
        letter = letter.lower()
        letters_guessed.append(letter)
        if letter in secret_word:
            for i in range(length_of_secret):
                if letter == secret_word[i]:
                    guessing[i * 2] = letter
                    correct_guess = True
        guessing_string = ""
        for i in guessing:
            guessing_string += i
        if correct_guess == True:  
            print(f"Good guess: {guessing_string}")    
        else:
            guesses = guesses - 1  
            print(f"Oops, {letter} is not in the word: {guessing_string}")  
            if no_more_guesses(guesses) == True:
                return 0
        if is_word_guessed(secret_word, letters_guessed) == True:            
            score = guesses * unique_letters
            print(f"Congratulations! You have guessed the word {secret_word} correctly!")   
            print(f"Your score is {score}")     
        print("---------------------------------------")      


                                                     
      

if __name__ == "__main__":
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

