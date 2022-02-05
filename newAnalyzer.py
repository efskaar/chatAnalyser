from newReadFile import Chat
from newGrapher import Grapher

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
    self.grapher.makePlot(func(),name)

  def plotEmojisGivenPerPerson(self):
    people = self.rcf.people
    for key in people.keys():
      p = people[key]
      filename = f'{p}-given-'
      self.grapher.makePlot(p.totalGivenReactions,filename,path='reactions\\')

  def plotEmojisReceivedPerPerson(self):
    people = self.rcf.people
    for key in people.keys():
      p = people[key]
      filename = f'{p}-gotten-'
      self.grapher.makePlot(p.totalReactions,filename,path='reactions\\')

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

if '__main__' == __name__:
  analyzer = Analyser('tfn.html')
  analyzer.plotDictData(analyzer.totalReactionsInChat,"emojis")
  analyzer.plotEmojisGivenPerPerson()
  analyzer.plotEmojisReceivedPerPerson()
  analyzer.printBasicInfo()