#Ziyu Zhang (Tino)
#Section A1
#ziyuzhang13@gatech.edu
#I worked on the homework assignment alone, using only this semester's course materials.
import string

class hw6():

    def __init__(self,win):
        f1=Frame(win)
        f1.grid(column=0,row=0)
        l1=Label(f1,text='Word Search File:')
        l1.pack()
        l2=Label(f1,text='Word Bank File:')
        l2.pack()
        f2=Frame(win)
        f2.grid(column=1,row=0)
        self.seS=StringVar()
        self.seS.set(':D')
        e1=Entry(f2,textvariable=self.seS, width=100)
        e1.pack()
        e1.config(state='readonly')
        self.seB=StringVar()
        self.seB.set(':D')
        e2=Entry(f2,textvariable=self.seB,width=100)
        e2.pack()
        e2.config(state='readonly')
        f3=Frame(win)
        f3.grid(column=0,row=1)
        b1=Button(f3,text='Generate Word Search', command=self.readFiles)
        b1.pack()
        f4=Frame(win)
        f4.grid(column=2,row=0)
        b2=Button(f4,text='Select File',command=self.openWSClicked)
        b2.pack()
        b3=Button(f4,text='Select File',command=self.openWBClicked)
        b3.pack()

        self.Win=win

    def openWSClicked(self):
        self.fileName=filedialog.askopenfilename()
        self.seS.set(self.fileName)
        
    def openWBClicked(self):
        self.fileName1=filedialog.askopenfilename()
        self.seB.set(self.fileName1)

    def readFiles(self):
        import csv
        f1=open(self.fileName,'r')
        f2=open(self.fileName1,'r')
        self.searchlist=[]
        self.banklist=[]
        self.testsearch=[]
        testbank=[]
        F1=csv.reader(f1,delimiter=',')
        F2=csv.reader(f2,delimiter=',')
        errorcount=0
        for i in F1:
            if len(i)>0:
                self.searchlist.append(i)
                self.testsearch.extend(i)
            for y in i:
                if y not in string.ascii_letters:
                    errorcount+=1
        
                      
        for j in F2:
            if len(j)>0:
                self.banklist.append(j)
                testbank.extend(j)
       
        count=0
        for k in self.banklist:
            self.banklist[count][0]=k[0].upper()
            self.banklist[count][0]=self.banklist[count][0].strip()
            count=count+1

        if errorcount>0:
            messagebox.showwarning(title='Excuse me!',message='Invalid File! >:(')
            
        else:
            self.generate()
        
    def generate(self):
        f4=Frame(self.Win)
        f4.grid(column=1,row=2)
        l3=Label(f4,text='Find the CS Vocab!')
        l3.pack()
        f5=Frame(self.Win)
        f5.grid(column=1,row=3)
        f6=Frame(self.Win)
        f6.grid(column=2,row=3)             
        rownumber=len(self.searchlist)
        self.columnnumber=len(self.searchlist[0])
        self.letters=[]
        l4=Label(f6,text='Word Bank')
        l4.pack(side=TOP)
        for i in range(0,rownumber):
            temp =[]
            for j in range(0,self.columnnumber):
                a=Label(f5,text=self.searchlist[i][j],width=4)
                a.grid(row=i,column=j)
                temp.append(a)
            self.letters.append(temp)
        
        self.words=[]
        for i in self.banklist:
            temp=[]
            a=Label(f6,text=i[0])
            a.pack(side=TOP)
            self.words.append(a)
        
        f7=Frame(self.Win)
        f7.grid(row=4,column=1)
        self.e3=Entry(f7,width=40)
        self.e3.pack(side=LEFT)
        b4=Button(f7,text='Find',width=10,command=self.findStartingCoords)
        b4.pack(side=LEFT)
        
    def findStartingCoords(self):
        self.OMG=[]
        self.wordfind=self.e3.get()
        self.FL=self.wordfind.upper()
        FL1=self.FL[0]
        for k in enumerate(self.testsearch):
            if FL1==k[1]:
                row=k[0]//self.columnnumber
                column=k[0]%self.columnnumber
                temp=(row,column)
                self.OMG.append(temp)
        
        self.find()
                        

    def find(self):
        self.coordList=[]
        lenlimit=len(self.wordfind.strip())
        wo=self.wordfind.strip()
        self.wo=wo.upper()
        M=list(self.wo)
        rownumber=len(self.searchlist)
        
        im=len(M)

        a=[]
        for i in self.banklist:
            a.extend(i)
        if self.wo not in a:
            messagebox.showwarning(title='Uh oh!',message="Uh oh.. There are no matches for that word. Please input a new word.")
        else:
            for i in self.OMG:
                lrcomplist=[] #left to right
                lrcomplistcord=[]
                for j in range(i[1],self.columnnumber):
                    lrcomplist.append(self.searchlist[i[0]][j])
                    temp=(i[0],j)
                    lrcomplistcord.append(temp)
                if M==lrcomplist[0:im]:
                    self.coordList.extend(lrcomplistcord[0:im])
                    
                rl=[]#right to left
                rlcord=[]
                for j in range(0,i[1]+1)[::-1]:
                    rl.append(self.searchlist[i[0]][j])
                    temp=(i[0],j)
                    rlcord.append(temp)
                if M==rl[0:im]:
                    self.coordList.extend(rlcord[0:im])

                down=[] #down
                downcord=[]
                for j in range(i[0],rownumber):
                    down.append(self.searchlist[j][i[1]])
                    temp=(j,i[1])
                    downcord.append(temp)
                if M==down[0:im]:
                    self.coordList.extend(downcord[0:im])

                up=[]#up (-row, column=)
                upcord=[]
                for j in range(0,i[0]+1)[::-1]:
                    up.append(self.searchlist[j][i[1]])
                    temp=(j,i[1])
                    upcord.append(temp)
                if M==up[0:im]:
                    self.coordList.extend(upcord[0:im])

                downR=[]#down right (+row,+column)
                downRcord=[]
                count=0
                if i[1]>=i[0]: #you iterate column, count rows
                    for j in range (i[1],self.columnnumber):
                        downR.append(self.searchlist[i[0]+count][j])
                        temp=(i[0]+count,j)
                        downRcord.append(temp)
                        count=count+1
                    if M==downR[0:im]:
                        self.coordList.extend(downRcord[0:im])
                elif i[1]<=i[0]: #you iterate rows, count columns
                    for j in range (i[0],self.columnnumber):
                        downR.append(self.searchlist[j][i[1]+count])
                        temp=(j,i[1]+count)
                        downRcord.append(temp)
                        count=count+1
                    if M==downR[0:im]:
                        self.coordList.extend(downRcord[0:im])
                
                downL=[] #down left (+row,-column)
                downLcord=[]
                count=0
                if self.columnnumber-1-i[1]>=i[0]: #you interate column,count rows    
                    for j in range(0,i[1]+1)[::-1]:
                        downL.append(self.searchlist[i[0]+count][j])
                        temp=(i[0]+count,j)
                        downLcord.append(temp)
                        count=count+1
                    if M==downL[0:im]:
                        self.coordList.extend(downLcord[0:im])
                elif self.columnnumber-1-i[1]<=i[0]: #interate row,count columns
                    for j in range(i[0],self.columnnumber):
                        downL.append(self.searchlist[j][i[1]-count])
                        temp=(j,i[1]-count)
                        downLcord.append(temp)
                        count=count+1
                    if M==downL[0:im]:
                        self.coordList.extend(downLcord[0:im])
                        
                    
                        

                upR=[]
                upRcord=[]
                count=0 #up right (-row,+column)
                if self.columnnumber-1-i[1]<=i[0]: #you interate column,count rows
                    for j in range(i[1],self.columnnumber):
                        upR.append(self.searchlist[i[0]-count][j])
                        temp=(i[0]-count,j)
                        upRcord.append(temp)
                        count=count+1
                    if M==upR[0:im]:
                        self.coordList.extend(upRcord[0:im])

                elif self.columnnumber-1-i[1]>=i[0]: #you interate row,count column
                    for j in range(0,i[0]+1)[::-1]:
                        upR.append(self.searchlist[j][i[1]+count])
                        temp=(j,i[1]+count)
                        upRcord.append(temp)
                        count=count+1
                    if M==upR[0:im]:
                        self.coordList.extend(upRcord[0:im])
                    
                    

                upL=[] #up left (-row,-column)
                upLcord=[]
                count=0
                if i[1]<=i[0]: #you interate column,count rows
                    for j in range(0,i[1]+1)[::-1]:
                        upL.append(self.searchlist[i[0]-count][j])
                        temp=(i[0]-count,j)
                        upLcord.append(temp)
                        count=count+1
                    if M==upL[0:im]:
                        self.coordList.extend(upLcord[0:im])

                elif i[1]>=i[0]: #you interate row,count column
                    for j in range(0,i[0]+1)[::-1]:
                        upL.append(self.searchlist[j][i[1]-count]) 
                        temp=(j,i[1]-count)
                        upLcord.append(temp)
                        count=count+1
                    if M==upL[0:im]:
                        self.coordList.extend(upLcord[0:im])

                ll=1
                

            self.new=[]
            for i in self.coordList:
                if i not in self.new:
                    self.new.append(i)
           

            
                
            self.updateGUI()
    def updateGUI(self):
        a=[]
        for i in self.banklist:
            a.extend(i)
        if len(self.new)!=0:
            if self.wo in a:
                index=a.index(self.wo)
                
            self.words[index].config(fg='grey')

        for j in self.new:
            self.letters[j[0]][j[1]].config(bg='yellow')

from tkinter import *

win=Tk()
win.title('Word Search Generator!')
app=hw6(win)
win.mainloop()
