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
        self.stat=Toplevel()
        self.stat.title('Statistics')
        self.LoginPage()
        self.Register()
        self.reg.withdraw()
        self.stat.withdraw()


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
            self.username=self.S1.get()
            self.password=self.S2.get()
            sql="SELECT * FROM ReservationUser WHERE Username='%s' AND Password='%s'" % (self.username,self.password)
            c=db.cursor()
            num=c.execute(sql)
            if num!=1:
                messagebox.showwarning('Opps!','You have entered an unrecognizable username/password combination!')
            else:
                messagebox.showinfo('Congratulations!',"You have successfully logged in!")
                self.log.withdraw()
                self.Homepage()
                self.home.deiconify()
        
                
    def Homepage(self):
        self.home=Toplevel()
        self.home.title('Room Reservation Homepage')
        self.SS=StringVar()
        self.SSS=StringVar()
        l1=Label(self.home,text='Welcome to GT Room Reservation System!',relief='raised')
        l1.grid(row=0,column=1,columnspan=3)
        ll=Label(self.home,text=' ')
        ll.grid(row=1,column=0)
        l2=Label(self.home,text='Current Reservations')
        l2.grid(row=2,column=0,sticky=E)
        e1=Entry(self.home,width=55,textvariable=self.SS)
        e1.grid(row=2,column=1,columnspan=6)
        e1.config(state='readonly')
        lll=Label(self.home,text=' ')
        lll.grid(row=4,column=0)
        l3=Label(self.home,text='Make new Reservations')
        l3.grid(row=5,column=0)
        f1=Frame(self.home,borderwidth=1,relief=SUNKEN)
        f1.grid(row=6,column=0)
        f1L=Label(f1,text='Day Choices')
        f1L.grid(row=0,column=0,sticky=N+S+E+W)
        f1list=['Monday','Tuesday','Wednesday','Thursday','Friday']
        self.f1v=StringVar()
        rowcount=1
        for i in f1list:      
            f1r=Radiobutton(f1,text=i,variable=self.f1v,value=i)
            f1r.grid(row=rowcount,column=0,sticky=W)          
            rowcount=rowcount+1
        self.f1v.set('empty')
        b1=Button(self.home,text='Cancel All Reservations',command=self.cancelReservation)
        b1.grid(row=8,column=0,sticky=N+S+E+W)
        llll=Label(self.home,text=' ')
        llll.grid(row=7,column=0)
        f2=Frame(self.home,borderwidth=1,relief=SUNKEN)
        f2.grid(row=6,column=1)
        f2L=Label(f2,text='Time Choices')
        f2L.grid(row=0,column=0,sticky=N+S+W+E)
        rowcount=1
        self.f2v=StringVar()
        f2list=['Morning','Afternoon','Evening','Night']
        for i in f2list:
            f2r=Radiobutton(f2,text=i,variable=self.f2v,value=i)
            f2r.grid(row=rowcount,column=0,sticky=W)
            rowcount=rowcount+1
        self.f2v.set('empty')
        f3=Frame(self.home,borderwidth=1,relief=SUNKEN)
        f3.grid(row=6,column=2)
        f4=Frame(self.home,borderwidth=1,relief=SUNKEN)
        f4.grid(row=6,column=3)
        f5=Frame(self.home,borderwidth=1,relief=SUNKEN)
        f5.grid(row=6,column=4)
        f3L=Label(f3,text='Building Choices')
        f3L.grid(row=0,column=0,sticky=N+S+W+E)
        f3list=['CULC','Klaus']
        self.f3v=StringVar()
        rowcount=1
        for i in f3list:
            f3r=Radiobutton(f3,text=i,variable=self.f3v,value=i)
            f3r.grid(row=rowcount,column=0,sticky=W)
            rowcount=rowcount+1
        self.f3v.set('empty')
        f4L=Label(f4,text='Floor Choices')
        f4L.grid(row=0,column=0)
        f4list=[1,2,3,4]
        self.f4v=StringVar()
        rowcount=1
        for i in f4list:
            f4r=Radiobutton(f4,text=i,variable=self.f4v,value=i)
            f4r.grid(row=rowcount,column=0,sticky=W)
            rowcount=rowcount+1
        self.f4v.set('empty')
        f5L=Label(f5,text='Room Choices')
        f5L.grid(row=0,column=0,columnspan=2,sticky=E+S+W+N)
        f5list1=list(range(1,6))
        f5list2=list(range(6,11))
        self.f5v=StringVar()
        rowcount=1
        for i in f5list1:
            f5r=Radiobutton(f5,text=i,variable=self.f5v,value=i)
            f5r.grid(row=rowcount,column=0,sticky=W)
            rowcount=rowcount+1
        rowcount=1
        for i in f5list2:
            f5r=Radiobutton(f5,text=i,variable=self.f5v,value=i)
            f5r.grid(row=rowcount,column=1,sticky=W)
            rowcount=rowcount+1
        self.f5v.set('empty')
        b2=Button(self.home,text='Check Availabe Options',command=self.availableReservations)
        b2.grid(row=8,column=1,columnspan=2,sticky=N+S+W+E)
        b3=Button(self.home,text='Stats',command=self.stats)
        b3.grid(row=8,column=3,sticky=N+S+E+W)
        b4=Button(self.home,text='Logout',command=self.hometologin)
        b4.grid(row=8,column=4,sticky=N+W+E+S)
        db=self.Connect()                 
        if db==None:
            lol=0
        else:
            c=db.cursor()
            sql1="SELECT RoomNo,Building,Floor,Day,Time FROM RoomReservations WHERE ReservedBy='%s'" %(self.username)
            self.numm=c.execute(sql1)
            data=c.fetchall()
            if self.numm==0:
                self.SS.set('No Reservations')
            elif self.numm==1:
                self.SS.set('Room %d on %s floor %d is reserved for %s at %s hours.'%(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4]))
            elif self.numm>1:
                self.SS.set('Room %d on %s floor %d is reserved for %s at %s hours.'%(data[1][0],data[1][1],data[1][2],data[1][3],data[1][4]))
                self.SSS.set('Room %d on %s floor %d is reserved for %s at %s hours.'%(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4]))
                self.e22=Entry(self.home,width=55,textvariable=self.SSS)
                self.e22.config(state='readonly')
                self.e22.grid(row=3,column=1,columnspan=6)
            


                     
        
        
        
    def hometologin(self):
        self.home.withdraw()
        self.home.destroy()
        self.log.deiconify()
    
    def availableReservations(self):
        if self.f1v.get()!='empty' and self.f2v.get()!='empty' and self.f3v.get()!='empty' and self.f4v.get()!='empty' and self.f5v.get()!='empty':
            
            db=self.Connect()
            day=self.f1v.get()
            building=self.f3v.get()
            floo=self.f4v.get()
            floor=int(floo)
            roo=self.f5v.get()
            room=int(roo)
            time=self.f2v.get()      
                 
            if db==None:
                lol=0
            else:
                c=db.cursor()
                sql="SELECT Time FROM RoomReservations WHERE Building='%s' AND Floor=%d AND RoomNo=%d AND Day='%s'"%(building,floor,room,day)
                num=c.execute(sql)
                data=c.fetchall()
                
                Morning=[8,9,10,11]
                Afternoon=[12,13,14,15]
                Evening=[16,17,18,19]
                Night=[20,21,22,23]
                unavail=[]
                for i in data:
                    index=i[0].find(':')
                    hour=int(i[0][0:index])
                    unavail.append(hour)
                if time=='Morning':
                    for i in unavail:
                        if i in Morning:
                            del Morning[Morning.index(i)]
                    
                    avail=Morning[:]
                elif time=='Afternoon':
                    for i in unavail:
                        if i in Afternoon:
                            del Afternoon[Afternoon.index(i)]
                    
                    avail=Afternoon[:]
                elif time=='Evening':
                    for i in unavail:
                        if i in Evening:
                            del Evening[Evening.index(i)]
                    
                    avail=Evening[:]
                elif time=='Night':
                    for i in unavail:
                        if i in Night:
                            del Night[Night.index(i)]
                    
                    avail=Night[:]
                if len(avail)==0:
                    messagebox.showwarning('Search Failure','Sorry! But this room is unavailable for the selected day and time')
                
                elif self.numm>1:
                    messagebox.showwarning('Error','You can only make 2 reservations per week. Try again next week.')
                else:
                    self.home.withdraw()
                    self.avail=Toplevel()
                    self.avail.title('Available Rooms')
                    l1=Label(self.avail,text=' ')
                    l1.grid(row=0,column=0)
                    labels=['Building','Floor','Room','Day','Time','Select']
                    availstring=[]
                    for i in avail:
                        if i/10<1:
                            strr='0'+str(i)+':00'
                            availstring.append(strr)
                        else:
                            strr=str(i)+':00'
                            availstring.append(strr)                        
                    select=[building,floor,room,day]
                    columncount=0
                    for i in labels:
                        yo=Label(self.avail,text=i,relief='raised')
                        yo.grid(row=1,column=columncount,sticky=N+S+E+W)
                        columncount=columncount+1
                    rowcount=2
                    columncount=0
                    self.ASV=StringVar()
                    for i in availstring:
                        for j in select:
                            lo=Label(self.avail,text=j)
                            lo.grid(row=rowcount,column=columncount,sticky=N+S+E+W)
                            columncount=columncount+1
                        lo=Label(self.avail,text=i)
                        lo.grid(row=rowcount,column=4,sticky=N+S+W+E)
                        rbb=Radiobutton(self.avail,variable=self.ASV,value=i)
                        rbb.grid(row=rowcount,column=5,sticky=N+S+E+W)
                        rowcount=rowcount+1
                        columncount=0
                    self.ASV.set('Empty')
                    SB=Button(self.avail,text='Submit Reservation',command=self.makeReservation)
                    SB.grid(row=rowcount,column=3,columnspan=2,sticky=N+S+W+E)
                    CB=Button(self.avail,text='Cancel',command=self.availtohome)
                    CB.grid(row=rowcount,column=5,sticky=N+S+W+E)
                    self.avail.deiconify()
        else:
            messagebox.showwarning('Search Failure','Please choose a valid option from each category!')
                    
                                   
    def availtohome(self):
        self.avail.destroy()
        self.availableReservations()
        self.avail.withdraw()
        self.home.destroy()
        self.Homepage()
        self.home.deiconify()

    def makeReservation(self):
        if self.ASV.get()=='Empty':
            messagebox.showwarning('Error!','Please select a time!')
        else:
            day=self.f1v.get()
            building=self.f3v.get()
            floo=self.f4v.get()
            floor=int(floo)
            roo=self.f5v.get()
            room=int(roo)
            time=self.f2v.get()
            db=self.Connect()
            exacttime=self.ASV.get()
            if db==None:
                lol=0
            else:
                sql='''INSERT INTO RoomReservations VALUES ("%s",%d,%d,"%s","%s","%s")'''%(building,floor,room,day,exacttime,self.username)
                c=db.cursor()
                c.execute(sql)
                db.commit()
                c.close()
                Sql='UPDATE ReservationUser SET NumberOfReservations=%d WHERE Username="%s"'%(self.numm+1,self.username)
                E=db.cursor()
                E.execute(Sql)
                db.commit()
                messagebox.showinfo('Reservation Completion!','Congratulations! Your room has been reserved!')
                self.avail.withdraw()
                self.Homepage()
                self.home.deiconify()

    def cancelReservation(self):
        if self.numm==0:
            messagebox.showwarning('Error!','You currently have no reservation to delete!')
        else:               
            db=self.Connect()
            if db==None:
                lol=0
            else:
                sql='DELETE FROM RoomReservations WHERE ReservedBy="%s"'%(self.username)
                sql2='UPDATE ReservationUser SET NumberOfReservations=%d WHERE Username="%s"'%(0,self.username)
                e=db.cursor()
                e2=db.cursor()
                e.execute(sql)
                e2.execute(sql2)
                e.close()
                e2.close()
                db.commit()
                messagebox.showinfo('Cancellation Completion','Congratulations! Your previous Reservations have been cancelled!')
                self.home.destroy()
                self.Homepage()
                

    def stats(self):       
        db=self.Connect()
        if db==None:
            lol=0
        else:
            c=db.cursor()
            sql='SELECT AVG(NumberOfReservations) FROM ReservationUser'
            c.execute(sql)
            avgR=c.fetchall()
            avg=float(avgR[0][0])
            c.close()
            sql2='SELECT COUNT(*) FROM RoomReservations WHERE Building="CULC"'
            sql3='SELECT COUNT(*) FROM RoomReservations WHERE Building="Klaus"'
            e=db.cursor()
            e.execute(sql2)
            f=db.cursor()
            f.execute(sql3)
            culc=int(e.fetchall()[0][0])
            klaus=int(f.fetchall()[0][0])
            if culc>klaus:
                message='CULC is more busy with %d reservations so far.'%(culc)
            elif culc<klaus:
                message='Klaus is more busy with %d reservations so far.'%(klaus)
            elif culc==klaus:
                message='Both are busy with %d reservations so far.'%(klaus)
            self.avg=StringVar()
            self.bui=StringVar()
            self.avg.set(avg)
            self.bui.set(message)
            ll=Label(self.stat,text=' ')
            ll.grid(row=0,column=0)
            l1=Label(self.stat,text='The average number of reservations per person is: ')
            l1.grid(row=1,column=0,sticky=E)
            l2=Label(self.stat,text='The busiest building: ')
            l2.grid(row=2,column=0,sticky=E)
            e1=Entry(self.stat,width=50,textvariable=self.avg)
            e1.config(state='readonly')
            e1.grid(row=1,column=1,columnspan=2)
            e2=Entry(self.stat,width=50,textvariable=self.bui)
            e2.config(state='readonly')
            e2.grid(row=2,column=1,columnspan=2)
            b=Button(self.stat,text='back',command=self.stattohome)
            b.grid(row=3,column=2,sticky=N+S+W+E)
            self.stat.deiconify()
            self.home.withdraw()

    def stattohome(self):
        self.stat.withdraw()
        self.home.deiconify()
            
            

win=Tk()
app=hw9(win)
win.mainloop()
