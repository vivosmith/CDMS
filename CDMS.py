import sqlite3
import random
from PIL import ImageTk
from random import randint
import PIL.Image
from tkinter import *
import tkinter
import io
import urllib.parse
import mechanicalsoup
from sys import platform
browser=mechanicalsoup.StatefulBrowser()
top=tkinter.Tk()
if platform=="win32":
   top.iconbitmap(default="icon.ico")
top.title("CDMS: Sports Card DB")
EnterFrame=Frame(top,bg="black")
EnterFrame.pack(expand=True, fill='both')
displayFrame=Frame(top,bg="black")
displayFrame.pack(expand=True, fill='both')
labelFrame=Frame(top,bg="silver")
Playername=Entry(EnterFrame,width=50)
Playername.insert(END,"player name or title")
Playername.pack()
mfg=Entry(EnterFrame,width=50)
mfg.insert(END,"manufacturer")
mfg.pack()
Year=Entry(EnterFrame,width=4)
Year.insert(END,"year")
Year.pack()
grade=Entry(EnterFrame,width=5)
grade.insert(END,"grade")
grade.pack()
sport=Entry(EnterFrame,width=5)
sport.insert(END,"sport")
sport.pack()
series=Entry(EnterFrame,width=5)
series.insert(END,"series")
series.pack()
labelFrame.pack(expand=True, fill='both')
by_id=Entry(EnterFrame,width=40)
by_id.insert(END,"by ID for Delete Button")
by_id.pack()
global pager
pager=0

def delete_card():
   if by_id.get()!="" or by_id.get()!=" ":
      Id_selected=str(by_id.get())
      conn=sqlite3.connect('card.db')
      player=str(Playername.get())
      mfg_=str(mfg.get())
      year_=str(Year.get())
      conn.execute("DELETE from COLLECTION WHERE ID=(?)", [Id_selected])
      conn.commit()
      conn.close()
delete_button=Button(EnterFrame,text="Delete Card",command=delete_card)
delete_button.pack()
def lab(result):
   for widget in displayFrame.winfo_children():
      widget.destroy()
   count=0
   results=[]
   term_=""
   grade_=""
   if results!="" or results!=" ":
      for res in result:
         results.insert(count,Label(labelFrame,text=" "))
         results[count].config(text = res, width = "75" , )
         results[count].pack()
         count=count+1
         term_=res[1]+" "+res[2]+" "+res[0]
         grade_number=grade.get()
   if grade.get()=="grade":
      grade_=""
   else:
      grade_="&Grade="+str(grade_number)
   if grade.get()!=" " and grade.get()!="" and grade.get()!="grade" and grade_!="":
      page='https://www.ebay.com/sch/Sports-Trading-Cards/212/i.html?_from=R40'+grade_+'&_nkw='+term_
   else:
      page='https://www.ebay.com/sch/Sports-Trading-Cards/212/i.html?_from=R40&Grade=Ungraded&_nkw='+term_
   print(page)
   URL=browser.get(page)
   finder=URL.soup.find_all('img')[2]['src']
   price=URL.soup.find_all(attrs={"class","lvprice prc"})[0]
   price_str=StringVar()
   raw_data = urllib.request.urlopen(str(finder)).read()
   im = PIL.Image.open(io.BytesIO(raw_data))
   image = ImageTk.PhotoImage(im)
   label1 = Label(displayFrame, image=image)
   label2=Label(displayFrame,textvariable=price_str,bg="grey")
   label1.pack_forget()
   label2.pack_forget()
   label1.image=image
   label1.pack()
   price_set=re.sub(r"(Trending at*$\*)"," ",str(price.text))
   price_s="".join(str(price_set).split())
   price_l=re.sub(r"(})","",str(price_s))
   price_r=re.sub(r"({)","",str(price_l))
   price_str.set(price_r)
   label2.pack()
def all_lab(result):
   for widget in labelFrame.winfo_children():
      widget.destroy()
   count=0
   results=[]
   for res in result:
      results.insert(count,Label(labelFrame,text=" "))
      reso=re.sub("({)","",str(res))
      reso2=re.sub("(})","",str(reso))
      results[count].config(text = reso2, width = "75" , )
      results[count].pack()
      count=count+1

def set():
   db(Year.get(),grade.get(),sport.get(),Playername.get(),mfg.get(),series.get())
def get():
   for widget in labelFrame.winfo_children():
      widget.destroy()
   get_db(Year.get(),grade.get(),sport.get(),Playername.get(),mfg.get(),series.get())  
add_card=Button(EnterFrame,text="Add a Card to the Database",command=set)
search_card=Button(EnterFrame,text="Search the Database",relief=SUNKEN,command=get)
add_card.pack()
search_card.pack()
def all_db():
   for widget in labelFrame.winfo_children():
      widget.destroy()
   conn = sqlite3.connect('card.db')
   def next_page():
     global pager
     if pager<d_size:
         pager=pager+10
         paged=str(pager)
         print(paged)
         cursor=conn.execute("SELECT * from COLLECTION LIMIT 10,(?)",[paged]) 
         all_lab(cursor)
         if pager>=d_size:
            next_button.pack_forget()
   results=conn.execute("SELECT * from COLLECTION ORDER BY YEAR")
   res=results.fetchall()
   d_size=len(res)
   print(d_size)
   if d_size<10:
      cursor=conn.execute("SELECT * from COLLECTION")
      all_lab(cursor)
   if d_size>10:
      paged=str(pager)
      next_button=Button(EnterFrame,text="Next page",command=next_page)
      next_button.pack()
      if pager==0:
         print(paged)
         cursor=conn.execute("SELECT * from COLLECTION LIMIT 10")
         all_lab(cursor)
   
      
def db(year,grade,sport,player_name,mfg,series_):
   Id=randint(1,2000000000)
   if year=='year' or year.isdigit==False:
      year=" "
   if sport=="sport":
      sport=" "
   if grade=="grade" or grade.isdigit==False:
      grade="0"
   if mfg=='mfg':
      mfg=" "
   if series_=='series':
      series_=" "
   grades=grade
   conn = sqlite3.connect('card.db')
   print ("Opened database successfully")
   conn.execute('INSERT INTO COLLECTION (ID,NAME,GRADE,YEAR,SPORT,MFG,SERIES) VALUES (?,?,?,?,?,?,?)', (Id,player_name,grades,year,sport,mfg,series_))
   conn.commit()
   conn.close()
search_card=Button(EnterFrame,text="Search for All Cards",command=all_db)
search_card.pack()
def get_db(year,grade,sport,player_name,mfg,series_):
   conn = sqlite3.connect('card.db')
   if year=='year' or year.isdigit==False:
      year=" "
   if sport=="sport":
      sport=" "
   if grade=="grade" or grade.get().isdigit==False:
      grade="0"
   if mfg=='mfg':
      mfg=" "
   if player_name=='play name or title':  
      player_name=" "
   if series_=='series':
      series_=" "
   grade_number=grade
   grade_="&Grade="+str(grade_number)
   grades=int(grade)
   cursor = conn.execute("SELECT NAME, YEAR, MFG from COLLECTION WHERE NAME==(?) AND YEAR==(?) AND MFG==(?)",(player_name,year,mfg))
   lab(cursor)
   counter=0
   conn.commit()
   conn.close()
top.mainloop()