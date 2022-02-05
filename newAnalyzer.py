from newReadFile import Chat
from newGrapher import Grapher
import os

class Analyser():
  def __init__(self,file):
    self.rcf = Chat()
    self.rcf.readFile(file)
    self.grapher = Grapher()

  def totalReactionsInChat(self):
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
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      filename = f'{chatName}/{p}/given-emojis'
      self.grapher.makePlot(self.sortDict(p.totalGivenReactions),filename)

  def plotEmojisReceivedPerPerson(self):
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      filename = f'{chatName}/{p}/gotten-emojis'
      self.grapher.makePlot(self.sortDict(p.totalReactions),filename)
  
  def plotSendTimePerPerson(self):
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      data = p.timeSendMessageDict()
      data = self.sortDict(data,False)
      filename = f'{chatName}/{p}/sent-time'
      self.grapher.makePlot(data,filename)

  def plotSendDayOfWeekPerPerson(self):
    people = self.rcf.people
    chatName = self.rcf.chatName
    for key in people.keys():
      p = people[key]
      data = p.dayOfWeekSendMessageDict()
      filename = f'{chatName}/{p}/sent-dayWeek'
      self.grapher.makePlot(data,filename)

  def printBasicInfo(self):
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
    '''
    self.makeNecessaryDirs()
    self.plotDictData(self.totalReactionsInChat,"emojis")
    self.plotEmojisGivenPerPerson()
    self.plotEmojisReceivedPerPerson()
    # self.printBasicInfo()

  def sortDict(self,data,isValue=True):
    return {k: v for k, v in sorted(data.items(), key=lambda item: item[isValue])}

  def makeDir(self,path):
    '''
    For making a directory
    '''
    if not os.path.exists(path):
      os.mkdir(path)
      print("Directory " , path ,  " Created ")
    # else:    
    #   print("Directory " , path ,  " already exists")
  
  def makeNecessaryDirs(self):
    '''
    Makes all necessary directories for the results files
    '''
    people = self.rcf.people
    chatName = self.rcf.chatName
    self.makeDir(chatName)
    for p in people:
      self.makeDir(chatName+'/'+str(p))

if '__main__' == __name__:
  analyzer = Analyser('tfn.html')
  # analyzer.makeNecessaryDirs()
  analyzer.plotSendDayOfWeekPerPerson()
  # analyzer.fullAnalysisAndDataCreation()