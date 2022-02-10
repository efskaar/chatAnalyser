import emoji


class Person():
  def __init__(self,name):
    self.name = name
    self.words = {}
    self.messages = []
    self.monthDict = {}
    self.timeDict = {}
    self.totalEmojis = {}
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
    '''
    adds a message to the class and properly counts its properties
    
    Args:
      dict message  : dict containing all the data for the message
    
    Returns:
      None
    '''
    self.messages.append(message)
    self.analyseMessage(message)

  def analyseMessage(self,msg):
    '''
    counts the different properties of a msg and adds it to the person
    The reactions to the msg is sent of to the person that has given to reaction

    Args:
      dict msg  : containing all the properties for the msg
    
    Returns:
      None
    '''
    self.wordCounter(msg['text'])
    self.countLinks += len(msg['links'])
    self.countImgs += len(msg['images'])
    self.countFiles += len(msg['files'])
    self.emojisCounter(msg['emojis'])
    self.reactionCounter(msg['reactions'],msg['chatObj'])

  def emojisCounter(self,emojis):
    '''
    counts emojis in a list of emojis
    creates a new key in totalEmojis if necessary

    Args:
      list emojis   : a list of the emojis in the msg

    Returns: 
      None
    '''
    for emoji in emojis:
      if emoji in self.totalEmojis.keys():
        self.totalEmojis[emoji] += 1
      else:
        self.totalEmojis[emoji] = 1


  def wordCounter(self,text):
    '''
    counts words in a string and adds them to the words dict
    removes any signs that are not letters, numbers or space

    Args:
      string emojis   : a list of the emojis in the msg

    Returns: 
      None
    '''
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
    '''
    adds the reations to a dictionary of participants and emojis
    sends the given reaction of to the sender of that reaction
    adds the reactions to the total reactions

    Args: 
      list reactions  : list containing reactions from the JSON file
      string chat     : the name of the chat
    
    Returns: 
      None
    '''
    if len(reactions) > 0:
      for reaction in reactions:
        name = reaction['actor']
        emoji = reaction['reaction']
        chat.participants[name].addGivenReaction(self.name,emoji)
        self.addReactionToName(name,emoji)
        self.addTotalReaction(emoji)

  def addReactionToName(self,name,r):
    '''
    Inserts the reaction into the reactions dictionary for each participants

    Args:
      string name   : name of the participant
      string r      : the emoji for the reaction
    
    Returns:
      None
    '''
    if name in self.reactions.keys():
      if r in self.reactions[name].keys():
        self.reactions[name][r] += 1
      else:
        self.reactions[name][r] = 1
    else:
      self.reactions[name] = {}
      self.reactions[name][r] = 1
  
  def addTotalReaction(self,r):
    '''
    Inserts the reaction into the reactions dictionary in total

    Args:
      string r      : the emoji for the reaction
    
    Returns:
      None
    '''
    if r in self.totalReactions.keys():
      self.totalReactions[r] += 1
    else:
      self.totalReactions[r] = 1
  
  def addGivenReaction(self,name,r):
    self.addGivenReactionToName(name,r)
    self.addTotalGivenReaction(r)

  def addGivenReactionToName(self,name,r):
    '''
    Inserts the reaction into the reactions given dictionary to each participants

    Args:
      string name   : name of the participant
      string r      : the emoji for the reaction
    
    Returns:
      None
    '''
    if name in self.givenReactions.keys():
      if r in self.givenReactions[name].keys():
        self.givenReactions[name][r] += 1
      else:
        self.givenReactions[name][r] = 1
    else:
      self.givenReactions[name] = {}
      self.givenReactions[name][r] = 1
  
  def addTotalGivenReaction(self,r):
    '''
    Inserts the reaction into the reactions given dictionary in total

    Args:
      string r      : the emoji for the reaction
    
    Returns:
      None
    '''
    if r in self.totalGivenReactions.keys():
      self.totalGivenReactions[r] += 1
    else:
      self.totalGivenReactions[r] = 1

  def timeSendMessageDict(self):
    '''
    For all messages:
      extract time
      extract hour part for that time
    
    Args: 
      None

    Return:
      dict
        int key     : hour - 0 ... 23
        int value   : number of times a msg was sent at that hour of the day
    '''
    timeDict = {key:0 for key in range(24)}
    msgs = self.messages
    for msg in msgs:
      time = msg['time']
      h = time.hour
      timeDict[h] +=1
    return timeDict
  
  def monthSendMessageDict(self):
    '''
    For all messages:
      extract time
      extract hour part for that time
    
    Args: 
      None

    Return:
      dict
        int key     : hour - 0 ... 23
        int value   : number of times a msg was sent at that hour of the day
    '''
    monthDict = {key:0 for key in range(1,13)}
    msgs = self.messages
    for msg in msgs:
      date = msg['date']
      m = date.month
      monthDict[m] +=1
    return monthDict

  def dayOfWeekSendMessageDict(self):
    '''
    For all messages:
      extract date
      find the day of the week for that date
    
    Args: 
      None

    Return:
      dict
        string key  : first three letter of a day
        int value   : number of times a msg was sent on that day
    '''
    data = {'Mon':0,
            'Tue':0,'Wed':0,
            'Thu':0,'Fri':0,
            'Sat':0,'Sun':0,}
    
    msgs = self.messages
    for msg in msgs:
      date = msg['date']
      d,m,y = date.day,date.month,date.year
      data[self.dayOfWeek(d,m,y)] += 1
    return data
    
  def dayOfWeek(self,d,m,y):
    '''
    Calculates the day of the week a given date is

    Args:
      int d - day   1-31
      int m - month 1-12
      int y - year  1-xxxx
    
    return: 
      string : three first letters for the day
    '''
    days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    anchorDate = [None,-4,0,0,-3,-5,-1,-3,-6,-2,-4,0,-2]
    leapYearMonth = 1 if y%4==0 and y%100==0 and y%400==0 and m<3 else 0
    diffAnchorDay = (d-anchorDate[m])-leapYearMonth
    dayOfWeek = int((diffAnchorDay+self.basisDayThatYear(y))%7)
    return days[dayOfWeek]

  def basisDayThatYear(self,setYear):
      '''
      Finds the anchor day of the week for that given year
      
      Args:
        int setYear: year from a date

      return:
        int : 0 for sun ... 6 for sat
      '''
      nrLeapYear = ((setYear-setYear%4)/4)-((setYear-setYear%100)/100)+((setYear-setYear%400)/400)
      dayThatYear = setYear + nrLeapYear + 2
      return dayThatYear%7
