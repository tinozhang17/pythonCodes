#Ziyu Zhang (Tino)
#Section A1
#ziyuzhang13@gatech.edu
#I worked on the homework assignment alone, using only this semester's course materials.
from tkinter import *

class hw9:

    def __init__(self,win):
        self.log=win
        self.log.title('Login')
        self.reg=Toplevel()
        self.reg.title('Room Reservation New User Registration')
        self.LoginPage()
        self.Register()
        self.reg.withdraw()


    def LoginPage(self):
        self.S1=StringVar()
        self.S2=StringVar()
        try:
            from urllib import request 
            url = "http://www.licensing.gatech.edu/sites/licensing.gatech.edu/files/images/logoIWMYGT.gif"
            response = request.urlopen(url)
            myPicture = response.read()
            import base64
            b64_data = base64.encodebytes(myPicture)
            self.photo= PhotoImage(data=b64_data)
            l=Label(self.reg,image=self.photo)
            l.image=self.photo
            l.grid(row=0,column=0,columnspan=5,sticky=N+E+W+S)
        except:
            lol=0
        user=Label(self.log,text='Username')
        user.grid(row=1,column=0,sticky=E)
        passwd=Label(self.log,text='Password')
        passwd.grid(row=2,column=0,sticky=E)
        E1=Entry(self.log,width=30,textvariable=self.S1)
        E1.grid(row=1,column=1,columnspan=3)
        E2=Entry(self.log,width=30,textvariable=self.S2)
        E2.grid(row=2,column=1,columnspan=3)
        B1=Button(self.log,text='Register',command=self.toRegister)
        B1.grid(row=3,column=2,sticky=N+E+W+S)
        B2=Button(self.log,text='Login',command=self.LoginCheck)
        B2.grid(row=3,column=3,sticky=E+W+N+S)
        B3=Button(self.log,text='Exit',command=self.exitclick)
        B3.grid(row=3,column=4)
               
    def exitclick(self):
        self.log.withdraw()
        
    def toRegister(self):
        self.log.withdraw()
        self.reg.deiconify()
        
    def Register(self):
        self.S3=StringVar()
        self.S4=StringVar()
        self.S5=StringVar()
        self.S6=StringVar()
        self.reg.deiconify()
        try:
            from urllib import request 
            url = "http://www.licensing.gatech.edu/sites/licensing.gatech.edu/files/images/logoIWMYGT.gif"
            response = request.urlopen(url)
            myPicture = response.read()
            import base64
            b64_data = base64.encodebytes(myPicture)
            self.photo= PhotoImage(data=b64_data)
            l=Label(self.log,image=self.photo)
            l.image=self.photo
            l.grid(row=0,column=0,columnspan=5,sticky=N+E+W+S)
        except:
            lol=0
        a=['Last Name','Username','Password','Confirm Password']
        r=1
        for i in a:
            L=Label(self.reg,text=i)
            L.grid(row=r,column=0,sticky=W)
            r=r+1
        var=[self.S3,self.S4,self.S5,self.S6]
        r=1
        for i in var:
            En=Entry(self.reg,textvariable=i,width=30)
            En.grid(row=r,column=1,columnspan=2)
            r=r+1
        B4=Button(self.reg,text='Cancel',command=self.backtologin)
        B4.grid(row=5,column=2,sticky=N+S+W+E)
        B5=Button(self.reg,text='Register',command=self.RegisterNew)
        B5.grid(row=5,column=3,sticky=N+E+S+W)
        
    def backtologin(self):
        self.reg.withdraw()
        self.log.deiconify()
        
    def Connect(self):   
        try:            
            import pymysql
            a = pymysql.connect(host="academic-mysql.cc.gatech.edu", user='zzhang363',passwd="******",db='cs2316db')
            return a
        except:
            messagebox.showwarning('Oh no!','Check your internet connection!')
            return None
        
    def RegisterNew(self):
        db=self.Connect()
        if db==None:
            lol=0
        else:
            Username=self.S4.get()
            Password1=self.S5.get()
            Password2=self.S6.get()
            LName=self.S3.get()
            c=db.cursor()
            sql="SELECT * FROM ReservationUser WHERE Username='%s'" % (Username)
            num=c.execute(sql)
            from re import findall
            numcheck=findall('(\d)',Password1)
            capcheck=findall('([A-Z])',Password1)
            c.close()
            if len(Username)==0 or len(Password1)==0:
                messagebox.showwarning('Oh no!','Please enter a Username and Password!')
            elif Password1!=Password2:
                messagebox.showwarning('Oh no!',"Passwords don't match each other!")
            elif len(Username)>=15:
                messagebox.showwarning('Oh no!','Username must be 15 characters or less!')
            elif num!=0:
                messagebox.showwarning('Oh no!','The username already exists in the database!')
            elif len(numcheck)==0 or len(capcheck)==0:
                messagebox.showwarning('Oh no!',"Password must consists of at least one uppercase letter and one number")
            else:
                C=db.cursor()
                if len(LName)==0:                   
                    SQL='''INSERT INTO ReservationUser (Username,Password) VALUES (%s,%s)'''  
                    num1=C.execute(SQL,(Username,Password1))
                    C.close()
                    db.commit()
                    messagebox.showinfo('Congratulations!',"You are successfully registered")
                    self.backtologin()
                elif len(LName)!=0:
                    SQL='''INSERT INTO ReservationUser (Username,Password,LastName) VALUES (%s,%s,%s)'''  
                    num1=C.execute(SQL,(Username,Password1,LName))
                    C.close()
                    db.commit()
                    messagebox.showinfo('Congratulations!',"You are successfully registered")
                    self.backtologin()
                

         
    def LoginCheck(self):
        db=self.Connect()
        if db==None:
            lol=0
        else:
            username=self.S1.get()
            password=self.S2.get()
            sql="SELECT * FROM ReservationUser WHERE Username='%s' AND Password='%s'" % (username,password)
            c=db.cursor()
            num=c.execute(sql)
            if num!=1:
                messagebox.showwarning('Opps!','You have entered an unrecognizable username/password combination!')
            else:
                messagebox.showinfo('Congratulations!',"You have successfully logged in!")
                self.log.withdraw()
            



win=Tk()
app=hw9(win)
win.mainloop()
