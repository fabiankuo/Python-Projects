
# coding: utf-8

# In[ ]:


#This is a hangman Game
#a random word is read from the txt file: words.txt
#the user gets 6 tries to guess the word or loses


# In[ ]:


import random
import string


# In[ ]:


def GetSecretWord():
    '''
    opens a txt file with words, randomly chooses a word from the file
    returns a string
    '''
    wordFile = open('words.txt','r')
    line = wordFile.readline()
    wordlist = line.split()
    return random.choice(wordlist)


# In[ ]:


def WonGame(secretWord, guessedLetters):
    '''
    parameters: string secretWord, string guessedLetters
    checks if the secretWord was guessed
    if guessed then returns true
    else returns false
    '''
    for chars in secretWord:
        if chars not in guessedLetters:
            return False
    return True


# In[ ]:


def AvailableLetters(guessedLetters):
    '''
    parameters: list guessedLetters
    creates a new list with available letters
    returns a string of available letters
    '''
    completeAlphabet = string.ascii_lowercase
    availableLetters = []
    if len(guessedLetters) < 1:
        completeAlphabet
    for chars in completeAlphabet:
        if chars not in guessedLetters:
            availableLetters.append(chars)
    return ''.join(availableLetters)


# In[ ]:


def InSecretWord(userGuess, secretWord):
    '''
    parameters: string userGuess, input from user, string secretWord the secret word that needs to be guessed
    checks if the letter is in the secretWord
    returns bool
    '''
    if userGuess in secretWord:
        print('Good guess: ')
        return True
    else:
        return False


# In[ ]:


def GetUserInput(guessedLetters):
    '''
    parameters: list guessedLetters, list of letters that had been guessed
    asks for input from user
    input must be a lowercased alphabet
    input should not be already picked before
    returns the user's input
    '''
    userGuess = None
    while True:
        try:
            userGuess = str(raw_input('Please guess a letter: ')).lower()
            if len(userGuess)>1:
                print('Only one letter only.')
                raise Exception
            elif userGuess in guessedLetters:
                print('Letter alrady guessed.')
                raise Exception
            elif userGuess not in string.ascii_lowercase:
                raise Exception
            else:
                guessedLetters.append(userGuess)
                break
        except:
            print('Please enter a valid input')
    return userGuess


# In[ ]:


def ShowCurrentProgress(guessedLetters, secretWord):
    progress = ['_ '] * len(secretWord)
    for x in xrange(len(secretWord)):
        if secretWord[x] in guessedLetters:
            progress[x] = secretWord[x]
    print("Current Guess Progress: {}".format(''.join(progress)))


# In[ ]:


def Play():
    lettersGuessed = []
    secretWord = GetSecretWord()
    chances = 8
    availableLetters = AvailableLetters(lettersGuessed)
    userGuess = None
    won = False
    print("Welcome to the Hangman Game")
    print("The length of the word is {}".format(len(secretWord)))
    while chances > 0:
        print('Chances Left: {}'.format(chances))
        print('Available letters: {}'.format(AvailableLetters(lettersGuessed)))
        userGuess = GetUserInput(lettersGuessed)
        if InSecretWord(userGuess,secretWord):
            print("Good Guess!")
            ShowCurrentProgress(lettersGuessed, secretWord)
            if WonGame(secretWord, lettersGuessed):
                won = True
                break
        else:
            print("{} is not in the word".format(userGuess))
            chances -= 1
    if won:
        print("You Won! the word is: {}".format(secretWord))
    else:
        print("You Lost, the word is: {}".format(secretWord))


# In[ ]:


Play()

