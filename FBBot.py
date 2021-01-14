import threading
import time
import heapq


class ReplyBot(object):
    def __init__(self):
        self.on = True
        self.responsetime = 0
        self.timea = time.time()
        self.convodict = {
            "help": "Thanks for asking for help. Here are a list of commands:",
            "operator": "You are now in line for an operator",
            "documentation": "Documentation of this program is located here: https://gowustl-my.sharepoint.com/:w:/g/personal/a_z_lu_wustl_edu/EXQ9RXJIL9NEnatHRIXD9dIBEFrb561LN3p7C41fbQrnbQ?e=eWXmf7",
            "/add": "Please input your new response in this manner: [command.response]",
            "/delete": "Please choose which command to delete out of the following:",
            "end": "Goodbye.",
            "log" : "Here are your logs:"

        }
        self.learnmap = {

        }
        self.learned = {

        }
        self.listcommands = ["help", "operator", "documentation", "/add", "/delete", "log"]
        self.replytext = ""
        self.nodelete = ["help", "/add", "/delete"]
        self.log = []


    def startconvo(self, checktime, time):
        if checktime == time:
            print("Send a response if the time has elapsed")

    def reply(self):

        self.replytext = input()
        self.log.append(self.replytext)
        self.responsetime = 0

    def checkElapsedtime(self):
        return time.time() - self.timea
    def timer(self):
        self.responsetime = 0

        while 1:
            self.responsetime += 1
            self.startconvo(60, self.responsetime)
            time.sleep(1)



    def activate(self):
        while self.on is True:
            self.reply()
            self.answer()


    def answer(self):


        ans = ""
        prompt = ""

        for x in self.replytext.split():
            if x in self.convodict:
                if ans != "":
                    print("You have more than one command!")
                    return None
                else:
                    prompt = x
                    ans = self.convodict[x]
        print(ans)
        self.log.append(ans)
        if prompt == "/add":
            self.addNewCommand()
        if prompt == "help":
            print(self.listcommands)
        if prompt == "/delete":
            listdelete = [i for i in self.listcommands + self.nodelete if
                          i not in self.listcommands or i not in self.nodelete]
            print(listdelete)
            self.deleteCommand()
        if prompt == "end":
            self.endConvo()
        if prompt == "log":
            print(self.log)
        if prompt == "" and ans == "":
            if self.checkLearned(self.replytext):
                pass
            else:
                print("I am unsure how to respond")
                self.log.append("I am unsure how to respond")
                self.learn(self.replytext)

    def checkLearned(self, prompt):
        checklist = []
        for x in prompt.split():
            if x in self.learned:
                for y in self.learned[x]:
                    heapq.heappush(checklist, (-1*self.learnmap[y], y))
        if not checklist:
            return False
        else:
            while checklist:
                cur = heapq.heappop(checklist)[1]
                print(cur)
                self.log.append(cur)
                response = input("Is this an appropiate answer? Please answer yes or no.")
                self.judgeResponse(cur, response, prompt)
                if response == "yes":
                    break
        return True
    def judgeResponse(self, strkey, response, prompt):
        if response == "yes":
            self.learnmap[strkey] = self.learnmap[strkey] + 1
        if response == "no":
            self.learnmap[strkey] = self.learnmap[strkey] -1
            self.learn(prompt)
    def addNewCommand(self):
        i = 0
        flag = False
        self.reply()
        while i < len(self.replytext):
            if self.replytext[i] == '.':
                command = self.replytext[0:i]
                response = self.replytext[i + 1::]
                self.convodict[command] = response
                self.listcommands.append(command)
                flag = True
                print("Your command has been successfully added")
                self.log.append("Your command has been successfully added")
            i = i + 1
        if not flag:
            print("Your command has not been added please try /add again")
            self.log.append("Your command has not been added please try /add again")
    def deleteCommand(self):
        self.reply()
        for x in self.replytext.split():
            if x in self.convodict and x not in self.nodelete:
                holdcommand = x
                holdresponse = self.convodict[x]
                del self.convodict[x]
                self.listcommands.remove(x)
                print(
                    "The command: " + x + " has been successfully deleted. Please do /undo if this was not your intent")
                self.log.append("The command: " + x + " has been successfully deleted. Please do /undo if this was not your intent")
                self.testUndo(holdcommand, holdresponse)
            else:
                print(
                    "Sorry, you have either chosen a command that cannot be deleted or have inputted a command that does not exist")
                self.log.append("Sorry, you have either chosen a command that cannot be deleted or have inputted a command that does not exist")

    def testUndo(self, oldcommand, oldresponse):
        self.reply()
        if self.replytext == "/undo":
            self.convodict[oldcommand] = oldresponse
            self.listcommands.append(oldcommand)
            print("Your command has been successfully re-added")
            self.log.append("Your command has been successfully re-added")
        else:
            self.answer()

    def endConvo(self):
        self.on = False

    def learn(self, prompt):
        proposed = input("What should I reply with?")
        self.log.append(proposed)
        for x in prompt.split():

            if x not in self.learned:
                self.learned[x] = [proposed]

                self.learnmap[proposed] = 1
            else:
                if isinstance(self.learned[x], list):
                    if proposed not in self.learned[x]:
                        self.learned[x].append(proposed)
                        self.learnmap[proposed] = 1
                    else:
                        self.learnmap[proposed] = self.learnmap[proposed] + 1
                self.aggregate(self.learned[x])
        print("Your suggestion has been noted")
        self.log.append("Your suggestion has been noted")



    def aggregate(self, learncommand):
        learncommand.sort()


t = ReplyBot()
test1 = threading.Thread(target=t.timer).start()
test2 = threading.Thread(target=t.activate).start()
