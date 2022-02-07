from calendar import formatstring
import datetime,emoji,json
from Person import Person

class Chat():
  def __init__(self):
      self.people = {}
      self.chatName = ''
      self.messages = []
      self.reactionCount = -1
      self.peopleC = '_2lek'
      self.chatNameC = '_3b0d'
      self.reactonUlTag = '_tqp'
      self.msgDivC = '_3-96 _2let'
      self.dateTimeC = '_3-94 _2lem'
      self.senderC = '_3-96 _2pio _2lek _2lel'
      self.msgContainer = 'pam _3-95 _2pi0 _2lej uiBoxWhite noborder'

  def getPeopleInChat(self):
    return list(self.people.keys())

  def fetchPeopleInChat(self,participants):
    for p in participants:
      name = formatstring(p['name'])
      self.people[name] = Person(name)

  def fetchAllMessages(self,msgs):
    #creating data structure for each messages
    for i in range(len(msgs)):
      m = msgs[i]
      dateStamp,timeStamp = m.find_all('div',{"class": self.dateTimeC})[0].contents[0].split(',')
      
      #quick fix for english version
      year,timeStamp = timeStamp.strip().split(' ')
      month,day = dateStamp.split(' ')
      dateStamp = f'{day}.{month.lower()}.{year}'

      #who sent and what did they send
      sender = m.find_all('div',{"class": self.senderC})[0].contents[0]
      messageText = m.find_all('div',{"class": self.msgDivC})[0].contents[0]
      stringifyMSG = str(messageText).replace('<div>','').replace('</div>','')
      
      imgs = m.find_all('img')
      reactions = m.find_all('li')
      aelements = m.find_all('a')
      reactionUl = m.find_all('ul',{"class":self.reactonUlTag})
      stringifyMSG = self.removeFromString(stringifyMSG,aelements)
      stringifyMSG = self.removeFromString(stringifyMSG,reactionUl)
      
      imgs = [str(img) for img in imgs]   
      reactions = [str(r.contents[0]) for r in reactions]     

      #it is possible for a link to have a empty innerHTML -.- 
      links = []
      for link in aelements:
        if len(link.contents)>0:
          links.append(str(link.contents[0]))

      message = {
        'index':i,
        'chatObj': self,
        'chat':self.chatName,
        'sender':sender,
        'date':dateStamp,
        'time':timeStamp,
        'text':stringifyMSG,
        'reactions':reactions,
        'links':links,
        'images':imgs,
        'files':[], #coming in the future
      }
      #chat's message list
      self.messages.append(message)
      #persons own message list
      self.people[sender].addMessage(message)

  def formatString(self,text):
    return text.encode("latin_1").decode("utf_8")

  def readFile(self,file):
    with open(file,'r', encoding='utf-8') as infile:
      #keys: participants, messages, title, is_still_participant, 
      #                   thread_type, thread_path, magic_words
      data = json.load(infile)
      self.chatName = self.formatString(data['title'])
      self.fetchPeopleInChat(data['participants'])
      self.fetchAllMessages(data['messages'])
    print(self)

  def countReactions(self):
    if self.reactionCount == -1:
      counter = 0
      for m in self.messages:
        counter += len(m['reactions'])
      self.reactionCount = counter
    return self.reactionCount

  def printMessages(self):
    for m in self.messages:
        print('\n\n')
        print(m['text'])

  def __str__(self):
    return f'{self.chatName} consists of:\n{len(self.messages)} messages\n{self.countReactions()} reactions\n{len(self.people)} people'

if '__main__' == __name__:
  rcf = Chat()
  rcf.readFile('tfn.html')
    
