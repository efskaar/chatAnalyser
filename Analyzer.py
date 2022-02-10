from Person import Person
from Chat import Chat
from Grapher import Grapher
import os

class Analyser():
  def __init__(self,file):
    self.rcf = Chat()
    self.rcf.readFile(file)
    self.grapher = Grapher()

  def plotDataInChat(self,func,fname,toSort=False,byValue=True):
    '''
    Creates a bar plot:
      X-axis: Data from func
      Y-axis: Frequency 
    
    Args:
      function func   : the function needs to return dict data
      string fname    : the filename with path for the output plot
      boolean tosort  : if the data needs to be sorted
      boolean byValue : true if sorting should be by value, false if by key
    
    Returns: 
      dict data       : collected data from all the participants via the func function

    Output: 
      image in the chat directory
    '''
    chatName = self.rcf.chatName
    filename = f'{chatName}/{fname}'
    people = self.rcf.participants
    data = {}
    for name in people.keys():
      p = people[name]
      newData = func(p)
      for key in newData.keys():
        if key in data:
          data[key] += newData[key]
        else:
          data[key] = newData[key]
    if toSort:
      data = self.sortDict(data,byValue)
    self.grapher.makePlot(data,filename)
    return data

  def plotDataPerPerson(self,func,fname):
    '''
    Creates a bar plot:
      X-axis: Data from func
      Y-axis: Frequency 
    
    Args:
      function func   : the function needs to return dict data
      string fname    : the filename with path for the output plot
    
    Returns: 
      None

    Output: 
      a image in each of the participant specific chat directory
    '''
    people = self.rcf.participants
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      filename = f'{chatName}/{p}/{fname}'
      self.grapher.makePlot(func(p),filename)

  def emojisGiven(self,p):
    return self.sortDict(p.totalGivenReactions)

  def emojis(self,p):
    return self.sortDict(p.totalEmojis)

  def emojisReceived(self,p):
    return self.sortDict(p.totalReactions)

  def sendTime(self,p):
    return self.sortDict(p.timeSendMessageDict(),False)

  def monthTime(self,p):
    return self.sortDict(p.monthSendMessageDict(),False)

  def dayOfWeek(self,p):
    return p.dayOfWeekSendMessageDict()

  def sortDict(self,data,byValue=True):
    '''
    Sorts a dictionary by value or key
    Sort by value by default 

    Args:
      dict data       : dictionary that will be sorted
      boolean byValue : default:True 
          True  --> sort by value
          False --> sort by key 
    
    returns:
      dict            : sorted dictionary
    '''
    return {k: v for k, v in sorted(data.items(), key=lambda item: item[byValue])}

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
    people = self.rcf.participants
    chatName = self.rcf.chatName
    self.makeDir(chatName)
    for p in people:
      self.makeDir(chatName+'/'+str(p))

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
    people = self.rcf.participants
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
    print(self.plotDataInChat(self.emojisGiven,'reactions-given',True))

  def fullAnalysisAndDataCreation(self):
    '''
    In case you want a full analysis of the chat

    Args: 
      None

    Returns:
      None
    '''
    self.makeNecessaryDirs()
    self.printBasicInfo()
    #chat specific
    self.plotDataInChat(self.emojis,'emojis-used',True)
    self.plotDataInChat(self.emojisGiven,'reactions-given',True)
    self.plotDataInChat(self.emojisReceived,'reactions-recieved',True)
    self.plotDataInChat(self.dayOfWeek,'msg-per-day-of-the-week')
    self.plotDataInChat(self.sendTime,'msg-send-time')
    self.plotDataInChat(self.monthTime,'msg-per-month')
    
    #person specific
    self.plotDataPerPerson(self.emojis,'emojis-used')
    self.plotDataPerPerson(self.emojisGiven,'reactions-given')
    self.plotDataPerPerson(self.emojisReceived,'reactions-recieved')
    self.plotDataPerPerson(self.dayOfWeek,'msg-per-day-of-the-week')
    self.plotDataPerPerson(self.sendTime,'msg-send-time')
    self.plotDataPerPerson(self.monthTime,'msg-per-month')

if '__main__' == __name__:
  analyzer = Analyser('tfn.json')
  analyzer.fullAnalysisAndDataCreation()
