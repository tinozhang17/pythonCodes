#Ziyu Zhang (Tino)
#Section A1
#ziyuzhang13@gatech.edu
#I worked on the homework assignment alone, using only this semester's course materials.

class hw8:

    def __init__(self,win):
        self.S1=StringVar()
        self.S2=StringVar()
        self.S3=StringVar()
        f1=Frame(win)
        f1.pack(side=LEFT)
        f2=Frame(win)
        f2.pack(side=LEFT)
        f12=Frame(f1)
        f12.pack()
        b1=Button(f12,text='Load Input CSV File',command=self.loadCSVclicked)
        b1.grid(row=0,column=0,columnspan=2,sticky=N+S+E+W)
        l1=Label(f12,text='File Path')
        l1.grid(row=1,column=0,columnspan=2,sticky=N+S+E+W)
        l2=Label(f12,text='Input CSV File')
        l2.grid(row=2,column=0)
        e1=Entry(f12,width=60,textvariable=self.S1)
        e1.grid(row=2,column=1)
        e1.config(state='readonly')
        l3=Label(f12,text='Website URL')
        l3.grid(row=3,column=0)
        e2=Entry(f12,width=60,textvariable=self.S2)
        e2.grid(row=3,column=1)
        l4=Label(f12,text='Output CSV File')
        l4.grid(row=4,column=0)
        e3=Entry(f12,width=60,textvariable=self.S3)
        e3.grid(row=4,column=1)
        e3.config(state='readonly')
        self.b2=Button(f12,text='Process Data',command=self.PDclicked)
        self.b2.grid(row=5,column=0,columnspan=2,sticky=N+W+S+E)
        self.b2.config(state=DISABLED)

        Dep=['Employees Per Department','Environment','Education','Human Resources',
             'Public Works','Transportation','Total']
        Labellist=[]
        count=0
        for i in Dep:
            a=Label(f2,text=i)
            a.grid(row=count,column=0)
            count=count+1
            Labellist.append(a)

        Labellist[0].grid(columnspan=2)
        
        self.StrVarlist=[]
        count=1
        for i in range(0,6):
            self.a=StringVar()
            self.a.set('-')
            l=Label(f2,textvariable=self.a)
            l.grid(row=count,column=1)
            count=count+1
            self.StrVarlist.append(self.a)
            
        
        
    def loadCSVclicked(self):
        self.filename = filedialog.askopenfilename()
        self.a=self.loadCSVfile(self.filename)
        if self.a==None:
            messagebox.showwarning("Invalid Move", "Please select a CSV file!")
        else:
            self.S1.set(self.filename)
            self.b2.config(state='normal')

            
            
            
        

    def loadCSVfile(self,filename):
        import csv
        self.csvlist=[]
        fh=open(filename)
        read=csv.reader(fh,delimiter=',')
        try:
            for i in read:
                if i[2]=='Parks and Recreation':
                    i[2]='Environment'
                self.csvlist.append(i)
            del self.csvlist[0]
            return self.csvlist
        except:
            return None
        
       
      
    def PDclicked(self):
        url=self.S2.get()
        tabledata=self.downloadSalaryData(url)
        if tabledata==None:
            messagebox.showwarning("Invalid Move", "URL or data invalid!")
            return None
        converted=self.convertHTMLtoCSVFormat(tabledata)
        merge=self.mergeData(self.a,converted)
        self.calculate(merge)
        self.saveData(merge)
        
        


    def downloadSalaryData(self,url):
        from urllib import request
        try:
            response=request.urlopen(url)
        except:
            return None
        html=response.read()
        data=html.decode()
        from re import findall
        reg=findall('<tr><td>([a-zA-Z]+\s[a-zA-Z]+)</td><td>(-|\d+)</td><td>([a-zA-Z]+\s?[a-zA-Z]+\s?[a-zA-Z]+?)</td></tr>',data) #regex
        b=list(map(list,reg))  #convert list of tuples to list of lists
        return b


    def convertHTMLtoCSVFormat(self,data):
        for i in data:
            name=i[0].split(' ')
            lastname=name[1]
            firstname=name[0]
            dep=i[2]
            if dep=='Parks and Recreation':
                dep='Environment'
            del i[0]
            i.insert(0,firstname)
            i.insert(0,lastname)
            del i[3]
            i.insert(2,dep)
        return data

    def mergeData(self,csvdata,tabledata):
        self.dic={}
        for i in tabledata:
            self.dic[i[0]+', '+i[1]]=[str(i[3]),i[2]]
        for j in csvdata:
            try:
                b=self.dic[j[0]+', '+j[1]]
                if b[0]=='-':
                    self.dic[j[0]+', '+j[1]]=[str(j[3]),j[2]]
            except:
                self.dic[j[0]+', '+j[1]]=[str(j[3]),j[2]]
        return self.dic
        
    def saveData(self,dic):
        grandlist=[]
        value=list(dic.values())
        keys=list(dic.keys())
        for i in range(0,self.total):
            b=[]
            b.append(keys[i])
            b.extend(value[i])
            grandlist.append(b)
        grandlist.sort(key=lambda x:(x[2],x[0]))
        grandlist.insert(0,['Name','Salary','Department'])
        location=filedialog.asksaveasfilename()
        self.S3.set(location)
        import csv
        fh=open(location,'w',newline="")
        csvWriter=csv.writer(fh)
        csvWriter.writerows(grandlist)
        fh.close()
        
        
                       

    def calculate(self,dic):
        value=list(dic.values())
        values=[]
        for i in value:
            values.append(i[1])
        environment=values.count('Environment')
        Ed=values.count('Education')
        HR=values.count('Human Resources')
        PW=values.count('Public Works')
        Tran=values.count('Transportation')
        self.total=len(values)
        lol=[environment,Ed,HR,PW,Tran,self.total]
        count=0
        for i in self.StrVarlist:
            i.set(lol[count])
            count=count+1
        


from tkinter import *
win=Tk()
win.title('City of Shamalamadingdong')
app=hw8(win)
win.mainloop()



















