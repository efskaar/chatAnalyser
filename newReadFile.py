
def divWithClass(text,className):
  endDiv = '</div>'
  classTag = f'<div class={className}>'
  classContent = (text.split(classTag)[1].split(endDiv)[0])
  return classContent





def fetchChatName(text):
  chatNameClass = '"_3b0d"'
  chatName = divWithClass(text,chatNameClass)
  return chatName





def fetchPeopleInChat(text):
  peopleClass = '"_2lek"'
  people = divWithClass(text,peopleClass)
  #strip on ':', everything after is names
  #strip on ',', every name is seperated with , 
  people = people.split(':')[1].split(',')
  #temp solution --> og is norwegian, need a fix for later version
  people[-1],pNew = people[-1].split('og'); people.append(pNew)
  people = [p.strip() for p in people]
  return people




def fetchReactions(text):
  reactionTag = '<ul class="_tqp">'
  reactions = text.split(reactionTag)
  if len(reactions)>1:
    return [r[4::] for r in reactions[1].split('</li>')[:-1:]]
  return []




def fetchMessageText(text):
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


def fetchAllMessages(text):
  #classNames for the html
  dateAndTimeClass = '"_3-94 _2lem"'
  senderClass = '"_3-96 _2pio _2lek _2lel"'

  #creating list of messages
  messagesContainer = '"pam _3-95 _2pi0 _2lej uiBoxWhite noborder"'
  classTag = f'<div class={messagesContainer}>'
  messages = text.split(classTag)[2::]
  
  #fetching sender,reactions,date,time,text
  listDictMessages = []
  for i in range(0,len(messages)):
    reactions = fetchReactions(messages[i])
    sender = divWithClass(messages[i],senderClass)
    dateStamp, timeStamp = divWithClass(messages[i],dateAndTimeClass).split(',')
    messageText = fetchMessageText(messages[i])
  
    #appending the new data structure for the message
    listDictMessages.append({
      'index':i,
      'sender':sender,
      'date':dateStamp,
      'time':timeStamp,
      'text':messageText,
      'reactions':reactions
    })
  return listDictMessages


def readFile(file):
  with open(file,'r',encoding='utf8') as infile:
    text = infile.read()
    
    #fetch chat name
    chatName = fetchChatName(text)
    # print(chatName)

    #fetch people in chat
    people = fetchPeopleInChat(text)
    # print(people)

    #fetch all messages
    messages = fetchAllMessages(text)
    for m in messages:
      print('\n\n')
      print(m['text'])


if '__main__' == __name__:
  readFile('tfn.html')