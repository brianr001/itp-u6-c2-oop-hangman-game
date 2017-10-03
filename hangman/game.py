from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guessed_letter, hit=None, miss=None):
        self.guessed_letter = guessed_letter
        self.hit = hit
        self.miss = miss
        
        if hit == True and miss == True:
            raise InvalidGuessAttempt
    
    def is_hit(self):
        if self.hit == True:
            return True
        elif self.hit == None:
            return False
    
    def is_miss(self):
        if self.miss == True:
            return True
        elif self.miss == None:
            return False


class GuessWord(object):
    
    def __init__(self, answer):
        self.answer = answer.lower()
        self.masked = len(answer) * '*'
        if answer == "":
            raise InvalidWordException
        
    def perform_attempt(self, guessed_letter):
        
        list_masked_word = list(self.masked)
        
        if len(guessed_letter) > 1:
            raise InvalidGuessedLetterException
        if guessed_letter.lower() not in self.answer.lower():
            return GuessAttempt(guessed_letter, miss=True)
        if guessed_letter.lower() in self.answer.lower():
            for idx, letter in enumerate(self.answer):
                if letter.lower() == guessed_letter.lower():
                    list_masked_word[idx] = guessed_letter.lower()
            self.masked = "".join(list_masked_word)
            return GuessAttempt(guessed_letter, hit=True)

class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=None, number_of_guesses=5):
        if list_of_words == None:
            list_of_words = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(list_of_words))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else:
            return False

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()
        
    def guess(self, guessed_letter):
        guessed_letter = guessed_letter.lower()
        
        if guessed_letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
            
        if self.is_finished():
            raise GameFinishedException
            
        self.previous_guesses.append(guessed_letter)    
        attempt = self.word.perform_attempt(guessed_letter)
            
        if attempt.is_miss() == True:
            self.remaining_misses -= 1
            
        if self.is_won():
            raise GameWonException()
            
        if self.is_lost():
            raise GameLostException()
            
        return attempt
        
    @classmethod
    def select_random_word(self, list_of_words):
        if list_of_words == []:
            raise InvalidListOfWordsException()
        choice_word = random.choice(list_of_words)
        return choice_word
    
    