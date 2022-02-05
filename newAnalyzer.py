from newReadFile import Chat

class Analyser():
  def __init__(self,file):
      self.rcf = Chat()
      self.rcf.readFile(file)

  def printBasicInfo(self):
    people = self.rcf.people
    summen = 0
    for name in people.keys():
      # print('\n\n',name)
      p = people[name]
      words = p.words
      # words = {k: v for k, v in sorted(p.words.items(), key=lambda item: item[1])}
      # for word in words:
      #   print(word,words[word])
      print('\n',name)
      print(f'{len(p.messages)} messages with {sum(words.values())} words')
      print(f'On average {sum(words.values())/len(p.messages):.0f} words per message')
      print('Received',sum(p.totalReactions.values()),p.totalReactions)
      print('Given',sum(p.totalGivenReactions.values()),p.totalGivenReactions)
      summen += sum(p.totalReactions.values())

if '__main__' == __name__:
  analyser = Analyser('tfn.html')
  analyser.printBasicInfo()