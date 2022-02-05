from pyexpat.errors import messages
from bs4 import BeautifulSoup

class Person():
  def __init__(self,name):
    self.name = name
    self.words = {}
    self.messages = []
    self.allowedSigns = 'qwertyuiopåasdfghjkløæzxcvbnmmQWERTYUIOPÅASDFGHJKLØÆZXCVBNM1234567890 '
  
  def __str__(self):
    return self.name
  
  def addMessage(self,message):
    self.messages.append(message)
    self.analyseMessage(message)

  def analyseMessage(self,msg):
    text = msg['text']
    for letter in text:
      if letter not in self.allowedSigns:
        text = text.replace(letter,' ')
    words = list(filter(('').__ne__, text.split(' ')))
    for word in words:
      word = word.lower()
      if word not in self.words.keys():
        self.words[word] = 1
      else:
        self.words[word] += 1

