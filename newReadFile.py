from email import message


class ReadChatFile():
  def __init__(self):
      self.people = []
      self.chatName = ''
      self.messages = []

  def divWithClass(self,text,className):
    endDiv = '</div>'
    classTag = f'<div class={className}>'
    classContent = (text.split(classTag)[1].split(endDiv)[0])
    return classContent

  def fetchChatName(self,text):
    chatNameClass = '"_3b0d"'
    chatName = self.divWithClass(text,chatNameClass)
    self.chatName = chatName

  def fetchPeopleInChat(self,text):
    peopleClass = '"_2lek"'
    people = self.divWithClass(text,peopleClass)
    #strip on ':', everything after is names
    #strip on ',', every name is seperated with , 
    people = people.split(':')[1].split(',')
    #temp solution --> og is norwegian, need a fix for later version
    people[-1],pNew = people[-1].split('og'); people.append(pNew)
    people = [p.strip() for p in people]
    self.people = people

  def fetchReactions(self,text):
    reactionTag = '<ul class="_tqp">'
    reactions = text.split(reactionTag)
    if len(reactions)>1:
      return [r[4::] for r in reactions[1].split('</li>')[:-1:]]
    return []

  def fetchMessageText(self,text):
    # I HATE THESE LINES 
    # might be some uncatched bugs in here
    reactionTag = '<ul class="_tqp">'
    messageClass = '"_3-96 _2let"'
    dateAndTimeClass = '"_3-94 _2lem"'
    temp = text.split(messageClass)[1][22::]
    if len(temp.split(reactionTag)) > 1:
      temp = temp.split(reactionTag)[0]
    else:
      temp = temp.split(dateAndTimeClass)[0][:-51:]
    temp = temp.replace('<div>','')
    temp = temp.replace('</div>','')
    return temp

  def fetchAllMessages(self,text):
    #classNames for the html
    dateAndTimeClass = '"_3-94 _2lem"'
    senderClass = '"_3-96 _2pio _2lek _2lel"'

    #creating list of messages
    messagesContainer = '"pam _3-95 _2pi0 _2lej uiBoxWhite noborder"'
    classTag = f'<div class={messagesContainer}>'
    messagesInChat = text.split(classTag)[2::]
    
    #fetching sender,reactions,date,time,text
    for i in range(0,len(messagesInChat)):
      reactions = self.fetchReactions(messagesInChat[i])
      sender = self.divWithClass(messagesInChat[i],senderClass)
      dateStamp, timeStamp = self.divWithClass(messagesInChat[i],dateAndTimeClass).split(',')
      messageText = self.fetchMessageText(messagesInChat[i])
    
      #appending the new data structure for the message
      self.messages.append({
        'index':i,
        'sender':sender,
        'date':dateStamp,
        'time':timeStamp,
        'text':messageText,
        'reactions':reactions
      })

  def readFile(self,file):
    with open(file,'r',encoding='utf8') as infile:
      text = infile.read()
      #fetch chat name
      self.fetchChatName(text)
      #fetch people in chat
      self.fetchPeopleInChat(text)
      #fetch all messages
      self.fetchAllMessages(text)
    print(self)

  def printMessages(self):
    for m in self.messages:
        print('\n\n')
        print(m['text'])

  def __str__(self):
    return f'{self.chatName} consists of {len(self.messages)} messages between {len(self.people)} people'


if '__main__' == __name__:
  rcf = ReadChatFile()
  rcf.readFile('tfn.html')
  print(rcf)