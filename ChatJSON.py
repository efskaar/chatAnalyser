import datetime,emoji,json
from PersonJSON import Person

class Chat():
  def __init__(self):
      self.participants = {}
      self.chatName = ''
      self.messages = []
      self.reactionCount = -1

  def getPeopleInChat(self):
    '''
    Makes a list of the names of the participants in the Chat
    '''
    return list(self.participants.keys())

  def fetchPeopleInChat(self,participants):
    for p in participants:
      name = self.formatString(p['name'])
      self.participants[name] = Person(name)

  def fetchContentInMessage(self,msg):
    tag = 'content'
    if tag in msg.keys():
      content = self.formatString(msg[tag])
      contentEmojis = self.extract_emojis(content)
    else:
      content = ''
      contentEmojis = ''
    return content,contentEmojis

  def fetchReactionsInMessage(self,msg):
    tag = 'reactions'
    if tag in msg.keys():
      for r in msg[tag]:
        for key in r.keys():
          r[key] = self.formatString(r[key])
      return msg[tag]
    else:
      return []
    
  def fetchMediaInMessage(self,msg,tag):
    return msg[tag] if tag in msg.keys() else []

  def fetchTimeAndDateInMessage(self,msg):
    ms = msg['timestamp_ms']
    dt = datetime.datetime.fromtimestamp(ms/1000.0)
    return dt.date(),dt.time()

  def fetchAllMessages(self,msgs):
    #creating data structure for each messages
    i = 0
    for msg in msgs:
      if not msg['is_unsent']:
        i += 1
        date,time = self.fetchTimeAndDateInMessage(msg)
        sender = self.formatString(msg['sender_name'])
        photos = self.fetchMediaInMessage(msg,'photos')
        gifs = self.fetchMediaInMessage(msg,'gifs')
        sticker = self.fetchMediaInMessage(msg,'sticker')
        videos = self.fetchMediaInMessage(msg,'videos')
        files = self.fetchMediaInMessage(msg,'files')
        reactions = self.fetchReactionsInMessage(msg)
        content,contentEmojis = self.fetchContentInMessage(msg)  
        links = []
        message = {
          'index':i,
          'chatObj': self,
          'chat':self.chatName,
          'sender':sender,
          'date':date,
          'time':time,
          'text':content,
          'emojis':contentEmojis,
          'reactions':reactions,
          'images':photos,
          'videos':videos,
          'gifs':gifs,
          'sticker':sticker,
          'files':files, #came in the future :)
          'links':links, #coming in the future
        }
        #chat's message list
        self.messages.append(message)
        #persons own message list
        self.participants[sender].addMessage(message)

  def formatString(self,text):
    return text.encode("latin_1").decode("utf_8")

  def extract_emojis(self,string):
    return ''.join(c for c in string if c in emoji.UNICODE_EMOJI['en'])

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
    return f'{self.chatName} consists of:\n{len(self.messages)} messages\n{self.countReactions()} reactions\n{len(self.participants)} people'

if '__main__' == __name__:
  rcf = Chat()
  rcf.readFile('tbs.json')
    
