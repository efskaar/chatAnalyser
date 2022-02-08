# chatAnalyser
 A chat analyzer for messenger chats. 
 
# How to use this project:
 In order to use this project you have to download your messenger chats from facebook

#### Copy the project and open a chat-file with the Analyzer class
  * **Analyzer** will send the file to **Chat**
  * **Chat** will parse the HTML data and send the parsed data to the person class
  * **Person** will systematicly count the parsed data from **Chat**
  * **Analyzer** can fetch data from **Person** and send it systematically to **Grapher**
  * **Grapher** can make bar plots of dict data
    * **Grapher** will be updated with further functionality in the future 

# Dependencies:
  **beautifulSoup** only for the HTML parser version
  json
  emoji
  datetime
  matplotlib
