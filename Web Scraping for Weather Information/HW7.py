#Ziyu Zhang (Tino)
#Section A1
#ziyuzhang13@gatech.edu
#I worked on the homework assignment alone, using only this semester's course materials.

class WebScrap():

    def __init__(self,win):
        self.button=Button(win,text='Get Info',command=self.clicked)
        self.button.pack()
        self.now=StringVar()
        self.feel=StringVar()
        self.message=StringVar()
        label=Label(win,textvariable=self.now)
        label.pack()
        l2=Label(win,textvariable=self.feel)
        l2.pack()
        l3=Label(win,textvariable=self.message)
        l3.pack()
        
        
        
    def clicked(self):
        self.getInfo()

    def getInfo(self):
        from urllib import request
        response=request.urlopen('http://www.weather.com/weather/today/30334')
        html=response.read()
        strHtml=html.decode()
        C=0
        index=0
        length=len(strHtml)
        while C!=5:
            index=strHtml.find('&deg',index, length)
            index=index+4
            C=C+1   
        position=index-4
        e=position-33
        d=[]
        while True:
            try:
                a=int(strHtml[e])
                e=e-1
                d.append(str(a))
            except:
                break      
        deg1=''.join(d[::-1])
        newindex=strHtml.find('&deg',index,length)
        new=newindex-8
        o=[]
        while True:
            try:
                kk=int(strHtml[new])
                new=new-1
                o.append(str(kk))
            except:
                break
        
        deg2=''.join(o[::-1])
        word='The temperature right now is: '+deg1+'F.'
        word1='And it feels like: '+deg2+'F.'
        self.now.set(word)
        self.feel.set(word1)
        if deg1==deg2:
            self.message.set('What you see is what you feel!')
        else:
            self.message.set('What you see is different from what you feel!')
        rere=[int(deg1),int(deg2)]
        return rere
        

from tkinter import *

win=Tk()
task=WebScrap(win)
win.mainloop()



