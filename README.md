# AutomatedBot
  This bot uses a self-created machine learning algorithm to decide what response to use. It comes with pre-installed commands such as help, /add, and end. Also has some other functionalities such as tracking time and keeping a log of all conversations. Documentation can be found here: https://gowustl-my.sharepoint.com/:w:/g/personal/a_z_lu_wustl_edu/EXQ9RXJIL9NEnatHRIXD9dIBEFrb561LN3p7C41fbQrnbQ?e=eWXmf7. Or can be done typing in "documentation" in the bot.
  
Auto Responding Bot Documentation 

Albert Lu 

 

Purpose of this Bot: This bot is created to automate a response to a human input. It comes with a few commands, but otherwise the bot can be taught how to respond using a feedback algorithm. 

 

Imported Libraries: 

import threading 
import time 
import heapq 

Classes: 

class ReplyBot(object): 

This is the only class used in this project. It is the bot that talks to the human and has all the methods that ensure the proper usage.  

Methods: 

def __init__(self) 

The constructor of this class. This method has some general variables such as self.on that is the conditional for the while loop explained further below. There is also the timer variables as well as a few dictionaries such as self.convodict, self.learned, self.learnmap that hold the pre-installed response and are used for learning new commands. Self.listcommands and self.nodelete are list formats of pre-installed commands where self.nodelete is the list of commands that cannot be deleted. 

 

def startconvo(self, timers): 

This method would send a response if the human has not interacted with the bot after a certain amount of time (the variable timers). This is activated by the boolean self.noresponse in the constructor. 

 

def reply(self): 

The method the human uses to talk to the bot using input(). Also sets the noresponse variable to false, so that the time is reset between text. 

def timer(self): 

Keeps track of the time the human has not responded in a separate thread running. If the human replies, the time for the thread is set to 0, so a new countdown will happen. 

 

def activate(self): 

Starts the thread for the actual conversation. It loops between the human typing and the bot responding with self.reply() and self.answer() 

 

def answer(self): 

How the bot responds is handled within this method. There is a dictionary with strings that already have a response. If the input from the human contains the word from the dictionary, the bot will automatically respond with the string. If it is a special case such as help, end, /add, /remove, or /log, the helper functions will run for those commands. Otherwise if there is no response to the bot, the bot will ask for a suggestion. This is covered in learn(). 

 

def addNewCommand(self): 

The bot asks for a new input in a specific format. The special format requires the usage a of a period to separate the command and the response. So for this bot, the bot searches for the period and takes everything before the period to be the command and takes everything after to be the response. It is then added to dictionary. If there is an issue with the command, the bot will return an error statement to the user. 

 

def deleteCommand(self): 

This method deletes unwanted commands. However, because some commands are deemed essential (stored in the nodelete list), only some commands can be deleted. This bot checks if the word is a command and is not in the nodelete list before removing it. It then updates the commands list. If there is an issue with the command, the bot will return an error statement to the user. 

 

def testUndo(self, oldcommand, oldresponse): 

This method is offered in case the delete method is used in an unintended way. It simply undoes the delete before by readding it to the dictionary and the commands list. 

 

def endConvo(self): 

Turns off the bot's responses. 

 

def learn(self, prompt): 

When prompted with an unknown input, learn() will be called so that the bot can learn what to respond. Currently, it breaks the input into separate words and asks the user to assign a reply they believe is appropriate for the their command. This response is added to the self.learned dictionary where it is stored in a string:list[string] format. The item for self.learned is then linked to another dictionary, self.learnmap where it is stored in a string:integer format. Self.learnmap is used to assign a rating score for the new response. As the response is saved in a list, the intention for the method is for a command to receive multiple suggestions what the response should be and decides what the best response should be. After running this function, self.aggregate() is called onto this the new/newly updated response list. 

 

def aggregate(self, learncommand): 

(WIP). This method should search through the response list and for commonly shared words, it should dictate if it should be suggested or not. It should also look at similar responses and eliminate one. 

 

def checkLearned(self, prompt): 

After being taught a response, when the command is ushered once again, this command is run. This runs on a reverse priority queue using heapq, and inserts all the response into this priority queue. It responds by popping off the most highly rated response and asks the user if this is the intended result. This then triggers the helper function judgeResponse() with a "yes" or "no" input. If the answer is yes, it updates the rating by plussing 1 and ends the loop and returning True. If the answer is no, judgeResponse() is called in and another answer from the priority queue is called, triggering the same response. 

 

def judgeResponse(self, strkey, response, prompt): 

If the response is no, this method would prompt the user if they would like to add another suggestion. If the suggestion is already in the learned responses, it would update the rating with another increment. Otherwise, it will add the response to the already existing responses and in turn add it to the priority queue for the next time the command is called. 
