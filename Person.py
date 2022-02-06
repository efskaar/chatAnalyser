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

  def timeSendMessageDict(self):
    timeDict = {key:0 for key in range(24)}
    msgs = self.messages
    for msg in msgs:
      timeDict[int(msg['time'].split(':')[0])] +=1
    return timeDict
  
  def dayOfWeekSendMessageDict(self):
    mToInt = {'jan':1,'feb':2,'mar':3,
              'apr':4,'mai':5,'jun':6,
              'jul':7,'aug':8,'sep':9,
              'okt':10,'nov':11,'des':12}
    data = {'Sun':0,'Mon':0,
            'Tue':0,'Wed':0,
            'Thu':0,'Fri':0,
            'Sat':0}
    
    msgs = self.messages
    for msg in msgs:
      d,m,y = msg['date'].split('.')
      d,m,y = int(d),mToInt[m.strip()],int(y)
      data[self.dayOfWeek(d,m,y)] += 1
    return data
    
  def dayOfWeek(self,d,m,y):
    days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    anchorDate = [None,-4,0,0,-3,-5,-1,-3,-6,-2,-4,0,-2]
    leapYearMonth = 1 if y%4==0 and y%100==0 and y%400==0 and m<3 else 0
    diffAnchorDay = (d-anchorDate[m])-leapYearMonth
    dayOfWeek = int((diffAnchorDay+self.basisDayThatYear(y))%7)
    return days[dayOfWeek]

  def basisDayThatYear(self,setYear):
      nrLeapYear = ((setYear-setYear%4)/4)-((setYear-setYear%100)/100)+((setYear-setYear%400)/400)
      dayThatYear = setYear + nrLeapYear + 2
      return dayThatYear%7