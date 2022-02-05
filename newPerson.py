class Person():
  def __init__(self,name):
    self.name = name
    self.words = {}
    self.messages = []
    self.monthDict = {}
    self.timeDict = {}
    self.reactions = {}
    self.totalReactions = {}
    self.givenReactions = {}
    self.totalGivenReactions = {}
    self.countLinks = 0
    self.countImgs = 0
    self.countFiles = 0
    self.allowedSigns = 'qwertyuiopåasdfghjkløæzxcvbnmmQWERTYUIOPÅASDFGHJKLØÆZXCVBNM1234567890 '
  
  def __str__(self):
    return self.name
  
  def addMessage(self,message):
    self.messages.append(message)
    self.analyseMessage(message)

  def analyseMessage(self,msg):
    self.wordCounter(msg['text'])
    self.countLinks += len(msg['links'])
    self.countImgs += len(msg['images'])
    self.countFiles += len(msg['files'])
    self.reactionCounter(msg['reactions'],msg['chatObj'])

  '''
  ***************************************
  Counter functions for words and reactions
  ***************************************
  '''
  def wordCounter(self,text):
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

  def reactionCounter(self,reactions,chat):
    names = chat.getPeopleInChat()
    if len(reactions) > 0:
      for r in reactions:
        for name in names:
          if name in r:
            r = r.replace(name,'').strip()
            chat.people[name].addGivenReaction(self.name,r)
            self.addReactionToName(name,r)
        self.addTotalReaction(r)


  '''
  ***************************************
  helper functions for reactions counting
  ***************************************
  '''
  def addReactionToName(self,name,r):
    if name in self.reactions.keys():
      if r in self.reactions[name].keys():
        self.reactions[name][r] += 1
      else:
        self.reactions[name][r] = 1
    else:
      self.reactions[name] = {}
      self.reactions[name][r] = 1
  
  def addTotalReaction(self,r):
    if r in self.totalReactions.keys():
      self.totalReactions[r] += 1
    else:
      self.totalReactions[r] = 1


  



  
  def addGivenReaction(self,name,r):
    self.addGivenReactionToName(name,r)
    self.addTotalGivenReaction(r)
  
  '''
  ***************************************
  helper functions for reactions given counting
  ***************************************
  '''

  def addGivenReactionToName(self,name,r):
    if name in self.givenReactions.keys():
      if r in self.givenReactions[name].keys():
        self.givenReactions[name][r] += 1
      else:
        self.givenReactions[name][r] = 1
    else:
      self.givenReactions[name] = {}
      self.givenReactions[name][r] = 1
  
  def addTotalGivenReaction(self,r):
    if r in self.totalGivenReactions.keys():
      self.totalGivenReactions[r] += 1
    else:
      self.totalGivenReactions[r] = 1
    
