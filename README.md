# Messenger **Chat Analyser**
 A chat analyzer for messenger chats. 
 
# How to use this project:
 In order to use this project you have to download your messenger chats from facebook

#### Copy the project and open a chat-file with the Analyzer class
  * **Analyzer** will send the file to **Chat**
  * **Chat** will read the JSON data, systemize the data and send the data to the **Person** class
  * **Person** will systematicly count the parsed data from **Chat**
  * **Analyzer** can fetch data from **Person** and send it systematically to **Grapher**
  * **Grapher** can make bar plots of dict data
    * **Grapher** will be updated with further functionality in the future 

# Dependencies:
  * **json**
  * **emoji**
  * **datetime**
  * **matplotlib**
