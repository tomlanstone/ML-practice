import nltk 
from nltk.book import *
import matplotlib.pyplot as plt

# 4

def q_4():
    a = len((text2))
    b = len(set((text2)))
    print(f"Number of words = {a}")
    print(f"Number of unique words = {b}")

## 6

def q_6():
    plt.style.use('default')
    text2.dispersion_plot(["Elinor","Marianne","Edward","Willoughby"])
    plt.show()

## 7 

def q_7():
    a = text5.collocations ()
    print(a)

## 9 

class q_9():
    def __init__(self):
        self.my_string = "This is a fun demonstration of what a string looks like"
    def a(self):
        print(self.my_string * 4)
    def b(self):
        print(self.my_string + self.my_string)
    def c(self):       
        print((self.my_string + "\n") * 3)

## 10

class q_10():
    def __init__(self):
        self.my_sent = ["This", "is", "a", "fun", "demonstration", "of", "what", "a", "list", "looks", "like"]

    def a(self):
        self.my_sent = " ".join(self.my_sent)
        print(self.my_sent)
    def b(self):
        self.my_sent = self.my_sent.split()
        print(self.my_sent)

## 11

class q_11():
    def __init__(self):
        self.phrase1 = ["I","am","list","a","hello"]
        self.phrase2 = ["Greetings", "this", "is", "the", "second", "list"]
    def a(self):
        a = len(self.phrase1)
        b = len(self.phrase2)
        print(a+b)
    def b(self):
        a = (self.phrase1)
        b = (self.phrase2)        
        print(len(a+b))

## 13

def q_13():
    ans = q_11()
    print(ans.phrase1[4][0])

## 14

def all_index(sent,word):
    print([i for i, x in enumerate(sent) if x.lower() == word])

## 15

def q_15():
    a = [i for i in text5 if i.lower().startswith("b")]
    print(sorted(set(a)))

## 17 
# finds all occurences of the word in the given text, searches for the start and end of the sentence for each one, returns them as a list of lists. Should be very easy to add an extra for loop to handle something such as a corpus of product reviews

class contextualiser():
    def __init__(self,text,word):
        self.word = word
        self.text = text
        self.indexes = [i for i, x in enumerate(text) if x.lower() == self.word]
    
    def get_context(self):
        sentences = [self.make_sentence(i) for i in self.indexes]
        return sentences
            
    def make_sentence(self, i):
        start = self._sentence_start(i)
        end = self._sentence_end(i)
        sentence = [w for w in self.text[start:end]]
        return sentence
    
    def _sentence_start(self, i):
        punctuation = [".","!","?"]
        count = i
        token = self.text[count]
        while token not in punctuation:
            token = self.text[count]
            count -=1
        if token in punctuation:
            start = count + 2
        return start
    
    def _sentence_end(self, i):
        punctuation = [".","!","?"]
        count = i
        token = self.text[count]
        while token not in punctuation:
            token = self.text[count]
            count +=1
        if token in punctuation:
            end = count 
        return end

## 18

def q_18():
    ans = sent1 + sent2 + sent3 + sent4 + sent5 + sent6 + sent7 + sent8
    a = len(ans)
    ans_b = sorted(set(ans))
    b = len(ans_b)
    print(b/a)

## 21

def q_21():
    a = text2[-2:]
    print(a)
q_21()

