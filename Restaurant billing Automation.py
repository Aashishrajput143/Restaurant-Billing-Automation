#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter.ttk import Style,Treeview
import sqlite3
from datetime import datetime


# In[21]:


win=Tk()
win.state('zoomed')
win.title('Restaurant Bill Automation')
win.configure(bg='sky blue')
win.resizable(width=False,height=False)
title=Label(win,text='Restaurant Bill Automation',font=('Arial',40,'underline','bold'),bg='sky blue')
title.place(relx=.283,rely=.05)

img1=PhotoImage(file="logo.png")
img2=PhotoImage(file="logo2.png")

logo_lbl1=Label(win,image=img1)
logo_lbl1.place(x=0,y=0)

logo_lbl2=Label(win,image=img2)
logo_lbl2.place(relx=.85,y=0)

def home_screen():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(x=0,y=188,relwidth=1,relheight=.92)

    def reset():
        e_login.delete(0,"end")
        e_password.delete(0,"end")
        e_login.focus() 
        
    def auth():
        u=e_login.get()
        p=e_password.get()
        if(len(u)==0 or len(p)==0):
            messagebox.showwarning('Validation',"Username/Password cann't be empty")
        else:
            if(u=='admin' and p=='admin'):
                frm.destroy()
                login_screen()
            else:
                 messagebox.showerror('Validation',"Invalid Username/Password")
        
    lbl_login=Label(frm,text='Username :-',font=('Arial',20,'bold'),bg='green')
    lbl_login.place(relx=.3,rely=.2)
    
    e_login=Entry(frm,font=('Arial',20,'bold'),bd=4)
    e_login.place(relx=.48,rely=.2)
    e_login.focus()
    
    lbl_password=Label(frm,text='Password :-',font=('Arial',20,'bold'),bg='green')
    lbl_password.place(relx=.3,rely=.35)
    
    e_password=Entry(frm,font=('Arial',20,'bold'),bd=5,show='*')
    e_password.place(relx=.48,rely=.35) 
    
    btn_login=Button(frm,text='login',font=('Arial',18,'bold'),bd=4,command=auth)
    btn_login.place(relx=.52,rely=.5)
    
    btn_reset=Button(frm,text='reset',font=('Arial',18,'bold'),bd=4,command=reset)
    btn_reset.place(relx=.6,rely=.5)
    
def login_screen():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(x=0,y=188,relwidth=1,relheight=.92)
    
    def logout():
        option=messagebox.askyesno('confirmation','Do you want to logout?')
        if(option==True):
            frm.destroy()
            home_screen()
            
    def billing():
        ifrm=Frame(frm)
        ifrm.configure(bg="#2B547E")
        ifrm.place(relx=.17,y=25,relwidth=.812,relheight=.78)
        
        con=sqlite3.connect(database='restaurant.sqlite')
        cur=con.cursor()
        cur.execute("select item_name,item_price_unit from items")
        rows=cur.fetchall()
        items=[]
        for row in rows:
            items.append(row[0])
        con.close()
        
        billed_items={}
        def add_item_to_details():
            item=item_entry.get()
            qty=qty_entry.get()
            con=sqlite3.connect(database='restaurant.sqlite')
            cur=con.cursor()
            cur.execute("select item_price_unit from items where item_name=?",(item,))
            row=cur.fetchone()
            price=row[0]
            con.close()
            billed_items[item]=[qty,price,int(qty)*price]
            show_billed_items()

        def delete_item_to_details():
            item=item_entry.get()
            try:
                billed_items.pop(item)
                show_billed_items()
            except:
                messagebox.showwarning("Fail","Item not found")

        def show_billed_items():
            y=0
            for item in billed_items:
                Label(items_frm,text=item,bg='white',fg='blue',font=('',11)).place(relx=.05,rely=.13+y)
                qty_price_amt=billed_items.get(item)
                x=0
                for val in qty_price_amt:
                    Label(items_frm,text=str(val),bg='white',fg='blue',font=('',11)).place(relx=.35+x,rely=.13+y)
                    x=x+.28
                y=y+.07
        
        def final_bill():
            amt=0
            for item in billed_items:
                amt=amt+billed_items.get(item)[-1]
            final_amt=amt+(5*amt)/100
            messagebox.showinfo("Your Bill:",f"Total Bill :- {amt}")
        
        item_label=Label(ifrm,text="Select Item:-",font=('Arial',17,'bold'),bg='#2B547E')
        item_label.place(relx=.03,rely=.2)
        
        item_entry=Combobox(ifrm,font=('Arial',15,'bold'),values=items)
        item_entry.current(0)
        item_entry.place(relx=.155,rely=.2)
        
        qty_label=Label(ifrm,text="Select Qty:-",font=('Arial',17,'bold'),bg='#2B547E')
        qty_label.place(relx=.03,rely=.38)
        
        qty_entry=Combobox(ifrm,font=('Arial',15,'bold'),values=[i for i in range(1,101)])
        qty_entry.current(0)
        qty_entry.place(relx=.155,rely=.38)
        
        add_btn=Button(ifrm,width=8,text="Add",font=('Arial',15,'bold'),bd=5,command=add_item_to_details)
        add_btn.place(relx=.08,rely=.55)
        
        delete_btn=Button(ifrm,width=8,text="Delete",font=('Arial',15,'bold'),bd=5,command=delete_item_to_details)
        delete_btn.place(relx=.22,rely=.55)
        
        items_frm=Frame(ifrm,bg='white')
        items_frm.place(relx=.42,rely=.045,width=700,height=500)
        
        date=str(datetime.now())
        Label(items_frm,text=f"{date}",font=('',13,'bold'),bg='white',fg='blue').place(relx=.01,rely=0)
        
        item_details=Label(items_frm,text="Billing Items",font=('',13,'bold'),bg='white',fg='brown')
        item_details.pack()
        
        Label(items_frm,text="Item",font=('',11,'bold'),bg='white',fg='black').place(relx=.05,y=28)
        Label(items_frm,text="Qty",font=('',11,'bold'),bg='white',fg='black').place(relx=.35,y=28)
        Label(items_frm,text="Price/Unit",font=('',11,'bold'),bg='white',fg='black').place(relx=.63,y=28)
        Label(items_frm,text="Amount",font=('',11,'bold'),bg='white',fg='black').place(relx=.88,y=28)
        
        bill_btn=Button(ifrm,width=7,text="Bill",font=('',15,'bold'),bd=5,command=final_bill)
        bill_btn.place(relx=.903,rely=.895)
        
        
    def items():
        ifrm=Frame(frm)
        ifrm.configure(bg="grey")
        ifrm.place(relx=.17,y=25,relwidth=.812,relheight=.78)
        
        def add():
            ie=item_entry.get().upper()
            pe=price_entry.get()
            
            if(len(ie)==0 or len(pe)==0):
                messagebox.showwarning('Validation','Plz fill both field')
                return
            elif(not pe.isdigit() and pe.isdigit()):
                messagebox.showwarning("Validation","Price must be in digit")
                return
            else: 
                con=sqlite3.connect(database='restaurant.sqlite')
                cur=con.cursor()
                try:
                    cur.execute("insert into items values(?,?)",(ie,pe))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Item Added..")
                except:
                    messagebox.showwarning("Fail","Try with different Item..")
                
                item_entry.delete(0,END)
                price_entry.delete(0,END)
                item_entry.focus()
                
        def reset():
            item_entry.delete(0,END)
            price_entry.delete(0,END)
            item_entry.focus()
        
        item_label=Label(ifrm,text="Item Name:-",font=('Arial',20,'bold'),bg='grey')
        item_label.place(relx=.275,rely=.2)
        
        item_entry=Entry(ifrm,font=('Arial',20,'bold'))
        item_entry.place(relx=.45,rely=.2)
        item_entry.focus()
        
        price_label=Label(ifrm,text="Price/Unit:-",font=('Arial',20,'bold'),bg='grey')
        price_label.place(relx=.275,rely=.38)
        
        price_entry=Entry(ifrm,font=('Arial',20,'bold'))
        price_entry.place(relx=.45,rely=.38)
        
        add_btn=Button(ifrm,width=10,text="Add",font=('Arial',17,'bold'),bd=5,command=add)
        add_btn.place(relx=.335,rely=.55)
        
        reset_btn=Button(ifrm,width=10,text="Reset",font=('Arial',17,'bold'),bd=5,command=reset)
        reset_btn.place(relx=.52,rely=.55)
        
        
    def price():
        ifrm=Frame(frm)
        ifrm.configure(bg="purple")
        ifrm.place(relx=.17,y=25,relwidth=.812,relheight=.78)
        
        con=sqlite3.connect(database='restaurant.sqlite')
        cur=con.cursor()
        cur.execute("select item_name,item_price_unit from items")
        rows=cur.fetchall()
        items=[]
        for row in rows:
            items.append(row[0])
        con.close()
        
        def update():
            item=item_entry.get()
            price=set_entry.get()
            con=sqlite3.connect(database='restaurant.sqlite')
            cur=con.cursor()
            cur.execute("update items set item_price_unit=? where item_name=?",(price,item))
            con.commit()
            con.close()
            messagebox.showinfo("Success","Price updated")
            item_entry.delete(0,END)
            set_entry.delete(0,END)
            item_entry.focus()
    
        def reset():
            item_entry.delete(0,END)
            set_entry.delete(0,END)
            item_entry.focus()
        
        def select_item(event):
            item=item_entry.get()
            con=sqlite3.connect(database='restaurant.sqlite')
            cur=con.cursor()
            cur.execute("select item_price_unit from items where item_name=?",(item,))
            row=cur.fetchone()
            iprice=row[0]
            set_entry.delete(0,END)
            set_entry.insert(0,str(iprice))
            con.close()
    
        item_label=Label(ifrm,text="Select Item:-",font=('Arial',20,'bold'),bg='purple')
        item_label.place(relx=.275,rely=.2)
        
        item_entry=Combobox(ifrm,font=('Arial',15,'bold'),values=items)
        item_entry.current(0)
        item_entry.place(relx=.45,rely=.2)
        
        item_entry.bind('<<ComboboxSelected>>',select_item)
        
        set_label=Label(ifrm,text=" Set Price:-",font=('Arial',20,'bold'),bg='purple')
        set_label.place(relx=.275,rely=.38)
        
        set_entry=Entry(ifrm,font=('Arial',17,'bold'),bd=5)
        set_entry.place(relx=.45,rely=.38)
        
        update_btn=Button(ifrm,width=10,text="Update",font=('Arial',17,'bold'),bd=5,command=update)
        update_btn.place(relx=.335,rely=.55)
        
        reset_btn=Button(ifrm,width=10,text="Reset",font=('Arial',17,'bold'),bd=5,command=reset)
        reset_btn.place(relx=.52,rely=.55)
    
    welcome_lbl=Label(frm,text="Welcome,Admin.....",font=('',20),bg='green')
    welcome_lbl.place(x=1,y=14)

    billing_btn=Button(frm,width=12,text="Billing",font=('',17,'bold'),bd=5,command=billing)
    billing_btn.place(relx=.028,rely=.15)

    addItem_btn=Button(frm,width=12,text="Add Item",font=('',17,'bold'),bd=5,command=items)
    addItem_btn.place(relx=.028,rely=.30)

    editPrice_btn=Button(frm,width=12,text="Edit Price",font=('',17,'bold'),bd=5,command=price)
    editPrice_btn.place(relx=.028,rely=.45)
    
    logout_btn_2=Button(frm,text="logout",width=12,font=('',17,'bold'),bd=5,command=logout)
    logout_btn_2.place(relx=.028,rely=.6)
    
home_screen()
win.mainloop()


# In[3]:


#con=sqlite3.connect(database="restaurant.sqlite")
#cur=con.cursor()
#cur.execute("create table items(item_name text primary key,item_price_unit integer)")
#con.commit()
#con.close()


# In[ ]:




