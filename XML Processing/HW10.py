#Ziyu Zhang (Tino)
#Section A1
#ziyuzhang13@gatech.edu
#I worked on the homework assignment alone, using only this semester's course materials.

from tkinter import*
import xml.etree.ElementTree as etree

class hw10:

    def __init__(self,win):
        self.win=win
        B=Button(self.win,text='Choose File',command=self.clicked)
        B.pack()
        

    def clicked(self):
        fileName=filedialog.askopenfilename()
        try:
            self.tree=etree.parse(fileName)
            self.parseGames()
        except:
            messagebox.showwarning('Oh no!',"The file cannot be parsed,please try again!")

    def parseGames(self):
        root=self.tree.getroot()
        dic={}
        for game in root:
            for inning in game:
                try:
                    atbats=inning.find('top').findall('atbat')
                    for atbat in atbats:
                        pitcherName=atbat.attrib['pitcher']
                        pitches=atbat.findall('pitch')
                        
                        newdic={}
                        for pitch in pitches:
                            pitch_type=pitch.attrib['pitch_type']
                            Type=pitch.attrib['type']
                            speed=pitch.attrib['start_speed']

                            if len(speed)==0:
                                continue
                            else:
                                
                                if pitch_type not in newdic:
                                    newdic[pitch_type]=[(speed,Type)]
                                else:
                                    newdic[pitch_type].append((speed,Type))
                        if pitcherName not in dic:
                            dic[pitcherName]=newdic
                        else:
                            for key in newdic:
                                if key in dic[pitcherName]:
                                    dic[pitcherName][key].extend(newdic[key])
                                else:
                                    dic[pitcherName][key]=newdic[key]
                    #bottom
                    atbats=inning.find("bottom").findall('atbat')
                    for atbat in atbats:
                        pitcherName=atbat.attrib['pitcher']
                        pitches=atbat.findall('pitch')
                        newdic={}
                        for pitch in pitches:
                            pitch_type=pitch.attrib['pitch_type']
                            Type=pitch.attrib['type']
                            speed=pitch.attrib['start_speed']
                            if len(speed)==0:
                                continue
                            else:
                                
                                if pitch_type not in newdic:
                                    newdic[pitch_type]=[(speed,Type)]
                                else:
                                    newdic[pitch_type].append((speed,Type))
                        if pitcherName not in dic:
                            dic[pitcherName]=newdic
                        else:
                            for key in newdic:
                                if key in dic[pitcherName]:
                                    dic[pitcherName][key].extend(newdic[key])
                                else:
                                    dic[pitcherName][key]=newdic[key]
                except:
                    break
                    
            


        self.dic=dic
        self.processPitches()


    def writePitchers(self):
        root=etree.Element('Pitchers')
        n=list(self.newdic.keys())
        n.sort()   
        for pitcher in n:
            li=etree.SubElement(root,'Pitcher',name=pitcher)
            for data in self.newdic[pitcher]:
                pi=etree.SubElement(li,'PitchData',pitchType=data)
                num=self.newdic[pitcher][data][0]
                speed=self.newdic[pitcher][data][1]
                ratio=self.newdic[pitcher][data][2]
                subnum=etree.SubElement(pi,'NumPitched')
                subnum.text=str(num)
                subspeed=etree.SubElement(pi,'AvgSpeed')
                subspeed.text=str(speed)
                subratio=etree.SubElement(pi,'StrikeToBallRatio')
                subratio.text=str(ratio)
        tree=etree.ElementTree(root)
        messagebox.showinfo('Parse Successful!','Press OK to save your output file')
        result = messagebox.askyesno("Save File", "Do you want to save as XML?")
        if result==True:
            loc=filedialog.asksaveasfilename()
            tree.write(loc,'UTF-8')
            label=Label(self.win,text='File successfully saved!')
            label.pack()
            
        else:
            return

    def processPitches(self):
        #dic format {name:{KC:(numPitched,avgspeed,ratio),FF:(etc..)
        newdic={}
        for pitcherName in self.dic:
            dic={}
            for pitch_type in self.dic[pitcherName]:
                sumSpeed=0
                br=[]
                for data in self.dic[pitcherName][pitch_type]:
                    try:
                        speed=float(data[0])
                        sumSpeed=sumSpeed+speed
                        br.append(data[1])
                    except:
                        continue
                NumPitched=len(self.dic[pitcherName][pitch_type])
                strikes=br.count('S')+br.count('X')
                balls=br.count('B')
                try:
                    ratio=strikes/balls
                except:
                    ratio=strikes/1
                avgSpeed=sumSpeed/NumPitched
                dic[pitch_type]=(NumPitched,avgSpeed,ratio)
            newdic[pitcherName]=dic
        self.newdic=newdic
        self.writePitchers()
            
            


win=Tk()
app=hw10(win)
win.mainloop()

