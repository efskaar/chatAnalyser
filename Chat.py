from bs4 import BeautifulSoup
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

  def fetchChatName(self,text):
    chatName = self.soup.find_all("div", {"class": self.chatNameC})
    self.chatName = chatName[0].contents[0]

  def fetchPeopleInChat(self,text):
    people = self.soup.find_all("div", {"class": self.peopleC})
    people = people[0].contents[0]
    #strip on ':', everything after is names
    #strip on ',', every name is seperated with , 
    people = people.split(':')[1].split(',')
    #temp solution --> og is norwegian, need a fix for later version
    #depends on your settings, language updated to english, thus and
    people[-1],pNew = people[-1].split(' and '); people.append(pNew)
    people = [p.strip() for p in people]
    #Fix this so we go through the people list and see if its new people
    for p in people:
      self.people[p] = Person(p)

  def removeFromString(self,text,listsOfEle):
    for ele in listsOfEle:
        text = text.replace(str(ele),'')
    return text

  def fetchAllMessages(self,):
    #creating list of messages
    msgs = self.soup.find_all("div", {"class": self.msgContainer})[1::]
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

  def readFile(self,file):
    with open(file,'r',encoding='utf8') as infile:
      text = infile.read()
      self.soup = BeautifulSoup(text, 'html.parser')
      #fetch chat name
      self.fetchChatName(text)
      #fetch people in chat
      self.fetchPeopleInChat(text)
      #fetch all messages
      self.fetchAllMessages()
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
    
