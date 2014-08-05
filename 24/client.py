import praw 
import time
import winsound
import html.entities
import tkinter
import string
from tkinter import Tk, BOTH, Entry, PhotoImage
from tkinter.ttk import Frame, Button, Style, Label

class Program():
    def __init__(self, name, path):
        self.name = name
        self.path = path

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("")
        #self.style = Style()
        #self.style.theme_use("clam")
        #self.pack(fill=BOTH, expand = 1)

        self.labelU = Label(self, text="U:")
        self.labelP = Label(self, text="P:")

        self.mailrecipient = 'GoldenSights'
        
        self.entryUsername = Entry(self)
        self.entryUsername.focus_set()
        self.entryUsername.bind('<Return>', lambda event: self.entryPassword.focus_set())

        self.entryPassword = Entry(self)
        self.entryPassword.config(show='•')
        self.entryPassword.bind('<Return>', lambda event: self.login(self.entryUsername.get(), self.entryPassword.get()))

        self.newbutton = Button(self, text="Login", command= lambda: self.login(self.entryUsername.get(), self.entryPassword.get()))
        self.newbutton.bind('<Return>', lambda event: self.login(self.entryUsername.get(), self.entryPassword.get()))
        self.newbutton.config(width=6)
        self.quitbutton = Button(self, text="Quit", command= lambda: self.quit())
        self.quitbutton.config(width=6)
    
        self.labelU.grid(row=0, column=0,padx=0)
        self.entryUsername.grid(row=0, column=1)
        self.labelP.grid(row=1, column=0)
        self.entryPassword.grid(row=1, column=1, pady=4)
        self.newbutton.grid(row=2, column=1)
        self.quitbutton.grid(row=3, column=1, pady=4)

        self.labelErrorPointer = Label(self, text="◀")

        self.indicatorGreen = PhotoImage(file="indicatorGreen.gif")
        self.indicatorRed = PhotoImage(file="indicatorRed.gif")
        self.indicatorBlue = PhotoImage(file="indicatorBlue.gif")
        self.indicatorBlack = PhotoImage(file="indicatorBlack.gif")
        

        
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()


        w=400
        h=480
        x = (sw - w) / 2
        y = (sh - h) / 2

        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y-50))
        

    def login(self, username, password):
        print('U: ' + username)
        self.username = username
        if username == '' or not all(char in string.ascii_letters+string.digits+'_-' for char in username):
            print('Please enter a username')
            self.entryUsername.focus_set()
            self.labelErrorPointer.grid(row=0, column=2)
        elif password == '':
            print('Please enter a password')
            self.entryPassword.focus_set()
            self.labelErrorPointer.grid(row=1, column=2)
            
        else:
            self.labelErrorPointer.grid_forget()
            print('Attempting login for ' + username)
            try:
                self.USERAGENT = username + ' practices Tkinter+PRAW mixing with utility by /u/GoldenSights.'
                self.r = praw.Reddit(self.USERAGENT)
                #self.r.login(username, password)
                print('Success')
                self.labelU.grid_forget()
                self.labelP.grid_forget()
                self.entryUsername.grid_forget()
                self.entryPassword.grid_forget()
                self.newbutton.grid_forget()
                self.quitbutton.grid_forget()
                self.usernamelabel = Label(self, text=username + ', Sending to /u/' + self.mailrecipient)
                self.usernamelabel.grid(row=0, column=0, pady = 5, columnspan=2)
                self.quitbutton.grid(row=900, column=0)


                self.optionDiscuss = "Discussion Flair + Crosposting"
                self.prevmode = self.optionDiscuss
                self.curmode = self.optionDiscuss
                self.optionvar = tkinter.StringVar(self)
                self.optionvar.trace("w",self.permaloop)
                self.optionvar.set(self.optionDiscuss)
                self.option = tkinter.OptionMenu(self, self.optionvar, self.optionDiscuss, "two", "three", "four")
                self.newbutton.unbind("<Return>")
                self.entryUsername.unbind("<Return>")
                self.entryPassword.unbind("<Return>")
                self.option.grid(row=1,column=0,columnspan=2)
                self.updategui(True)
            except praw.errors.InvalidUserPass:
                pass
                print('Invalid username or password')
                self.entryPassword.delete(0,200)
                self.labelErrorPointer.grid(row=1, column=2)

    def permaloop(self, *args):
        self.curmode = self.optionvar.get()
        print('Was: ' + self.prevmode + ' | Now: ' + self.curmode)
        if self.curmode != self.prevmode:
            self.prevmode = self.curmode
            self.updategui(True)

    def updategui(self, *args):
        print('Updating GUI')
        if self.curmode == self.optionDiscuss and args[0] == True:
            self.labellist = []
            self.entrylist = []
            self.verifylist = []
            self.newrowindex = 4
            self.labelPermalink = Label(self, text="Thread Permalink:")
            self.entryPermalink = Entry(self)
            self.rowconfigure(2,weight=2)
            self.labelPermalink.grid(row=2,column=0)
            self.entryPermalink.grid(row=2,column=1)
            self.labelcrossposting = Label(self,text="Crosspost to:")
            self.labelcrossposting.grid(row=3,column=0,columnspan=2)
            for m in range(5):
                self.redditlabel = Label(self,text="/r/")
                self.redditlabel.grid(row=self.newrowindex,column=0)
                self.labellist.append(self.redditlabel)

                self.redditentry = Entry(self)
                self.redditentry.grid(row=self.newrowindex,column=1)
                self.entrylist.append(self.redditentry)

                self.newrowindex +=1

            self.morerowbutton = Button(self,text="+row",command=self.morerows)
            self.morerowbutton.grid(row=898,column=0,columnspan=2)

            self.verifybutton = Button(self,text="Verify",command= lambda: self.updategui(False))
            self.verifybutton.grid(row=899,column=0,columnspan=2)

            self.newrowindex += 2

        if self.curmode == self.optionDiscuss and args[0] == False:
            verifies = []

            i = self.entryPermalink.get()
            if len(i) == 6:
                pid = i
            else:
                if 'www.reddit.com/r/' in i and '/comments/' in i:
                    pid = i.split('/comments/')[1].split('/')[0]
                if 'http://redd.it/' in i:
                    pid = i.split('redd.it/')[1]

            for flag in self.verifylist:
                flag.grid_forget()
                self.verifylist.remove(flag)

            try:
                print('Fetching Submission ' + pid)
                self.r.get_info(thing_id="t3_" + pid).title + 'Check'
                self.redditlabel = Label(self, image=self.indicatorGreen)
                self.redditlabel.grid(row=2,column=2)
                self.verifylist.append(self.redditlabel)
                verifies.append(True)
                print('\tSuccess')
            except:
                print('Failed. Make sure to include the http://. Copy and paste straight from your browser for best result')
                self.redditlabel = Label(self, image=self.indicatorRed)
                self.redditlabel.grid(row=2,column=2)
                self.verifylist.append(self.redditlabel)
                verifies.append(False)

            for entry in self.entrylist:
                i = entry.get()
                if i != '':
                    print('Fetching /r/' + i)
                    if all(char in string.ascii_letters+string.digits+'_-' for char in i):
                        try:
                            sub = self.r.get_subreddit(i,fetch=True)
                            self.redditlabel = Label(self, image=self.indicatorGreen)
                            self.redditlabel.grid(row=entry.grid_info()['row'],column=2)
                            self.verifylist.append(self.redditlabel)
                            verifies.append(True)
                            print('\tSuccess')
                        except:
                            self.redditlabel = Label(self, image=self.indicatorRed)
                            self.redditlabel.grid(row=entry.grid_info()['row'],column=2)
                            self.verifylist.append(self.redditlabel)
                            verifies.append(False)
                            print('\tFailed')
                        time.sleep(2)
                    else:
                        self.redditlabel = Label(self, image=self.indicatorRed)
                        self.redditlabel.grid(row=entry.grid_info()['row'],column=2)
                        self.verifylist.append(self.redditlabel)
                        verifies.append(False)
                        print('\tFailed')

            print(verifies)

    def morerows(self, *args):
        self.redditlabel = Label(self,text="/r/")
        self.redditlabel.grid(row=self.newrowindex,column=0)
        self.labellist.append(self.redditlabel)

        self.redditentry = Entry(self)
        self.redditentry.grid(row=self.newrowindex,column=1)
        self.entrylist.append(self.redditentry)

        self.newrowindex += 1
        if self.newrowindex == 20:
            self.morerowbutton.grid_forget()





        

def main():
    root = Tk()
    f1 = tkinter.Frame(width=200, height=200)
    ex = Example(root)
    f1.pack(fill="both", expand=True, padx=20, pady=20)
    ex.place(in_=f1, anchor="c", relx=.5, rely=.5)
    root.mainloop()



if __name__ == '__main__':
    main()



