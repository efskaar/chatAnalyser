from Chat import Chat
from Grapher import Grapher
import os

class Analyser():
  def __init__(self,file):
    self.rcf = Chat()
    self.rcf.readFile(file)
    self.grapher = Grapher()

  def totalReactionsInChat(self):
    '''
    Creates a bar plot:
      X-axis: Emojis
      Y-axis: Frequency 
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    reactionsDict = {}
    for name in people.keys():
      p = people[name]
      for key in p.totalReactions.keys():
        if key in reactionsDict:
          reactionsDict[key] += p.totalReactions[key]
        else:
          reactionsDict[key] = p.totalReactions[key]
    reactionsDict = {k: v for k, v in sorted(reactionsDict.items(), key=lambda item: item[1])}
    return reactionsDict

  def plotDictData(self,func,name):
    self.grapher.makePlot(func(),name,path=self.rcf.chatName+'/')

  def plotEmojisGivenPerPerson(self):
    '''
    Creates a bar plot per person for emojis given:
      X-axis: Emojis
      Y-axis: Frequency 
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      filename = f'{chatName}/{p}/given-emojis'
      self.grapher.makePlot(self.sortDict(p.totalGivenReactions),filename)

  def plotEmojisReceivedPerPerson(self):
    '''
    Creates a bar plot per person for emojis received:
      X-axis: Emojis
      Y-axis: Frequency 
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      filename = f'{chatName}/{p}/gotten-emojis'
      self.grapher.makePlot(self.sortDict(p.totalReactions),filename)
  
  def plotSendTimePerPerson(self):
    '''
    Creates a bar plot per person:
      X-axis: Hour of the day
      Y-axis: Frequency 
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      data = p.timeSendMessageDict()
      data = self.sortDict(data,False)
      filename = f'{chatName}/{p}/sent-time'
      self.grapher.makePlot(data,filename)

  def plotSendDayOfWeekPerPerson(self):
    '''
    Creates a bar plot per person:
      X-axis: Day of week
      Y-axis: Frequency 
    One plot per person
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      data = p.dayOfWeekSendMessageDict()
      filename = f'{chatName}/{p}/sent-dayWeek'
      self.grapher.makePlot(data,filename)

  def plotSendTime(self):
    '''
    Creates a bar for the whole chat:
      X-axis: Hour of the day
      Y-axis: Frequency 
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    data = {key:0 for key in range(24)}
    for key in people.keys():
      p = people[key]
      newData = p.timeSendMessageDict()
      for key in data.keys():
        data[key] += newData[key]
    filename = f'{chatName}/sent-time'
    self.grapher.makePlot(data,filename)

  def plotSendDayOfWeek(self):
    '''
    Creates a bar for the whole chat:
      X-axis: Day of week
      Y-axis: Frequency 
    One plot per person
    
    Args:
      None
    
    Returns: 
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    data = {'Mon':0,
            'Tue':0,'Wed':0,
            'Thu':0,'Fri':0,
            'Sat':0,'Sun':0,}
    for key in people.keys():
      p = people[key]
      newData = p.dayOfWeekSendMessageDict()
      for key in data.keys():
        data[key] += newData[key]
    filename = f'{chatName}/sent-dayWeek'
    self.grapher.makePlot(data,filename)


  def printBasicInfo(self):
    '''
    Prints basic info to the terminal
    Words per message
    Messages - Words 
    And the reaction dictionaries are printed
    
    Args:
      None

    Returns:
      None
    '''
    people = self.rcf.people
    summen = 0
    for name in people.keys():
      p = people[name]
      words = p.words
      print('\n',name)
      print(f'{len(p.messages)} messages with {sum(words.values())} words')
      print(f'On average {sum(words.values())/len(p.messages):.0f} words per message')
      print('Received',sum(p.totalReactions.values()),p.totalReactions)
      print('Given',sum(p.totalGivenReactions.values()),p.totalGivenReactions)
      summen += sum(p.totalReactions.values())
    print('\n\n\n')
    print(self.totalReactionsInChat())
  
  def fullAnalysisAndDataCreation(self):
    '''
    In case you want a full analysis of the chat

    Args: 
      None

    Returns:
      None
    '''
    self.makeNecessaryDirs()
    # self.plotDictData(self.totalReactionsInChat,"emojis")
    # self.plotSendDayOfWeek()
    # self.plotSendTime()
    # self.plotEmojisGivenPerPerson()
    # self.plotEmojisReceivedPerPerson()
    # self.plotSendDayOfWeekPerPerson()
    self.plotSendTimePerPerson()
    # self.printBasicInfo()





  def sortDict(self,data,isValue=True):
    '''
    Sorts a dictionary by value or key
    Sort by value by default 

    Args:
      dict data       : dictionary that will be sorted
      boolean isValue : default:True 
          True  --> sort by value
          False --> sort by key 
    
    returns:
      dict            : sorted dictionary
    '''
    return {k: v for k, v in sorted(data.items(), key=lambda item: item[isValue])}





  def makeDir(self,path):
    '''
    For making a directory
    
    Args: 
      str path  : the path including the new dir
    
    Returns:
      None 
    '''
    if not os.path.exists(path):
      os.mkdir(path)
      print("Directory " , path ,  " Created ")
    # else:    
    #   print("Directory " , path ,  " already exists")
  
  def makeNecessaryDirs(self):
    '''
    Makes all necessary directories for the results files
    
    Args:
      None
    Return:
      None
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    self.makeDir(chatName)
    for p in people:
      self.makeDir(chatName+'/'+str(p))

if '__main__' == __name__:
  analyzer = Analyser('tbs.html')
  analyzer.fullAnalysisAndDataCreation()
