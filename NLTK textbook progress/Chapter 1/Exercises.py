import nltk 
#from nltk.book import *
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

