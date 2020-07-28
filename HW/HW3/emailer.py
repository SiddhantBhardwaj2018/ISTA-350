import tkinter as tk
from tkinter import font
import smtplib, ssl, sys
import email.message, email.policy, email.utils
from hw3 import *

"""
To prepare to demo to the class, create the new classlist.csv and db per instructions at the
top of hw3.

If you're sending from gmail, go to https://www.google.com/settings/security/lesssecureapps
and turn it on.
"""

root = tk.Tk()
root.title("Emailer")

left_frame = tk.Frame(root, bd=5, relief="sunken", padx=8)
# the pack geometry manager is being at the level of the root frame
left_frame.pack(side='left') 

# create a dictionary to compactly pass some keyword arguments to some widget constructors
height = 1
pady = 10
my_font = font.Font(size=14)
kwargs = {'height': height, 'pady': pady, 'font': my_font}

# ************ left_frame: Email Login ************************

# The grid geometry manager is being used inside left_frame
tk.Label(left_frame, text='--- Email SMTP Server Login ---', **kwargs).grid(columnspan=4)

def set_fld(fld, text):
    fld.delete(0, 'end')
    fld.insert('end', text)
# Clear the field on left click:
domain = tk.Entry(left_frame, width=30, justify='left', font=my_font)
domain.grid(row=2, column=1, columnspan=3, sticky='w')
domain.bind('<Button-1>', lambda event: set_fld(domain, ''))

'''
Programming note: a callback must be specified as a reference to a function object
(no parentheses therefore), so when callbacks require arguments, lambdas are the best
option.  Google callback shim/curry a function for another option.  If parentheses
are given, the function will execute once on startup and then the callback will 
always return that initial call's return value.
'''
    
tk.Button(left_frame, text='UA', **kwargs, width=10,
    command=lambda: set_fld(domain, 'smtpgate.email.arizona.edu')).grid(row=1, sticky='w')
tk.Button(left_frame, text='Gmail', **kwargs, width=10,
    command=lambda: set_fld(domain, 'smtp.gmail.com')).grid(row=1, column=1, sticky='w')
tk.Button(left_frame, text='Hotmail', **kwargs, width=10,
    command=lambda: set_fld(domain, 'smtp.live.com')).grid(row=1, column=2, sticky='w')
tk.Button(left_frame, text='Yahoo', **kwargs, width=10,
    command=lambda: set_fld(domain, 'smtp.mail.yahoo.com')).grid(row=1, column=3, sticky='w')
    
tk.Label(left_frame, text='      Domain:', **kwargs).grid(row=2)

tk.Label(left_frame, text='    Username:', **kwargs).grid(row=3)
username = tk.Entry(left_frame, width=30, justify='left', font=my_font)
username.grid(row=3, column=1, columnspan=3, sticky='w')
username.bind('<Button-1>', lambda event: set_fld(username, ''))

tk.Label(left_frame, text='    Password:', **kwargs).grid(row=4)
password = tk.Entry(left_frame, width=30, justify='left', font=my_font, show='*')
password.grid(row=4, column=1, columnspan=3, sticky='w')
password.bind('<Button-1>', lambda event: set_fld(password, ''))

tk.Label(left_frame, text='      Status:', **kwargs).grid(row=5)
login_status = tk.Entry(left_frame, width=30, justify='left', font=my_font)
login_status.grid(row=5, column=1, columnspan=3, sticky='w')
login_status.bind('<Button-1>', lambda event: set_fld(login_status, ''))

logged_in = False
smtp_connection = None
def update_login_status(msg, err=False):
    login_status.delete(0, 'end')
    if not err: login_status.config(fg='#00CC33')
    else: login_status.config(fg='red')
    login_status.insert(0, msg)
def end_connection(msg, err=False):
    global smtp_connection
    try: smtp_connection.quit()
    except: pass
    update_login_status(msg, err)
def successful_login(msg):
    global logged_in
    update_login_status(msg)
    login_logout_button['text'] = 'Logout'
    logged_in = True
def login_logout():
    '''
    A relatively complicated version so that we can know if the connection is
    secure or not and catch failures.  Can be done in a few lines without the frills.
    '''
    global logged_in, smtp_connection
    if not logged_in:
        try:  
            smtp_connection = smtplib.SMTP(domain.get(), 587)
            smtp_connection.ehlo()
            smtp_connection.starttls()
            smtp_connection.login(username.get(), password.get())
            successful_login('Logged in and using TLS')
        except:
            try: smtp_connection.quit()
            except: pass
            print('TLS failed, trying SSL')
            smtp_connection = smtplib.SMTP_SSL(domain.get(), 465)
            smtp_connection.ehlo()
            smtp_connection.login(username.get(), password.get())
            successful_login('Logged in and using SSL')
        if not logged_in:
            end_connection('Login failed', True)
    else:
        end_connection('Logged out')
        logged_in = False
        login_logout_button['text'] = 'Login'
login_logout_button = tk.Button(left_frame, text='Login', **kwargs, width=10, command=login_logout)
login_logout_button.grid(row=6, column=1, sticky='w')
password.bind('<Return>', lambda event: login_logout())

# ************ left_frame: Manage People ************************

tk.Label(left_frame, text='', **kwargs).grid(row=7, columnspan=3) # blank line spacer
tk.Label(left_frame, text='--- Manage People ---', **kwargs).grid(row=8, columnspan=4)

tk.Label(left_frame, text='       Email:', **kwargs).grid(row=9)
email_fld = tk.Entry(left_frame, width=30, justify='left', font=my_font)
email_fld.grid(row=9, column=1, columnspan=3, sticky='w')
email_fld.bind('<Button-1>', lambda event: set_fld(email_fld, ''))

tk.Label(left_frame, text='       First:', **kwargs).grid(row=10)
first = tk.Entry(left_frame, width=30, justify='left', font=my_font)
first.grid(row=10, column=1, columnspan=3, sticky='w')
first.bind('<Button-1>', lambda event: set_fld(first, ''))

tk.Label(left_frame, text='        Last:', **kwargs).grid(row=11)
last = tk.Entry(left_frame, width=30, justify='left', font=my_font)
last.grid(row=11, column=1, columnspan=3, sticky='w')
last.bind('<Button-1>', lambda event: set_fld(last, ''))

tk.Label(left_frame, text='    Birthday:', **kwargs).grid(row=12)
bday = tk.Entry(left_frame, width=30, justify='left', font=my_font)
bday.grid(row=12, column=1, columnspan=3, sticky='w')
bday.bind('<Button-1>', lambda event: set_fld(bday, ''))

tk.Label(left_frame, text='  Status/Log:', **kwargs).grid(row=13)
people_status = tk.Entry(left_frame, width=30, justify='left', font=my_font)
people_status.grid(row=13, column=1, columnspan=3, sticky='w')

def update_people_status(msg, err=False):
    people_status.delete(0, 'end')
    if not err: people_status.config(fg='#00CC33')
    else: people_status.config(fg='red')
    people_status.insert(0, msg)

def friend():
    people_status.delete(0, 'end')
    try:
        add_person(db, Person(first.get(), last.get(), bday.get(), email_fld.get()))
        update_people_status(email_fld.get() + ' added to friends')
    except:
        update_people_status('duplicate key: failed to add ' + email_fld.get())
    
def colleague():
    people_status.delete(0, 'end')
    try:
        add_person(db, Person(first.get(), last.get(), bday.get(), email_fld.get()), friend=False, colleague=True)
        update_people_status(email_fld.get() + ' added to colleagues')
    except:
        update_people_status('duplicate key: failed to add ' + email_fld.get())
    
def delete():
    em = email_fld.get()
    # need filler for the other fields, email_fld is all that counts
    delete_person(db, Person('f', 'l', 'bd', email_fld.get()))
    people_status.config(fg='#00CC33')
    update_people_status(email_fld.get() + ' deleted')
    
    
tk.Button(left_frame, text='friend', **kwargs, width=10, command=friend).grid(row=14, sticky='w')
tk.Button(left_frame, text='colleague', **kwargs, width=10, command=colleague).grid(row=14, column=1, sticky='w')
tk.Button(left_frame, text='delete', **kwargs, width=10, command=delete).grid(row=14, column=2, sticky='w')
'''
Programming exercise: add an update button.  Would need to add a
get_person method to hw3.py (or in here).  update would put
that person's info into fields for editing/saving and delete the old entry.
'''
    
tk.Label(left_frame, text='Save/Delete', **kwargs).grid(row=15, columnspan=3 )

# ************ right_frame: Compose and Send ************************

right_frame = tk.Frame(root, bd=5, relief="sunken", width=48, padx=8)
# the pack geometry manager is being at the level of the root frame
right_frame.pack() 

# make rows 1-3 widgets before row 0 widgets because need listbox for row 0
tk.Label(right_frame, text='', **kwargs).grid(row=1, columnspan=4) # blank line spacer
tk.Label(right_frame, text=' Hit Enter to Transfer Selection to Recipients:', **kwargs).grid(row=2, columnspan=4, sticky='w')

scrollbar = tk.Scrollbar(right_frame, orient='vertical')
lb = tk.Listbox(right_frame, selectmode='extended', yscrollcommand=scrollbar.set, width=60)
scrollbar.config(command=lb.yview)
lb.grid(row=3, column=0, columnspan=3, sticky='w')
scrollbar.grid(row=3, column=3, sticky='nsw')
def transfer():
    indices = lb.curselection()
    items = [lb.get(index) for index in indices]
    recips.delete(0, 'end')
    recips.insert(0, ', '.join(items))  
lb.bind('<Return>', lambda event: transfer())
  
def friends():
    lb.delete(0, 'end')
    for email in [p.email for p in get_friends(db)]:
        lb.insert(tk.END, email)

def colleagues():
    lb.delete(0, 'end')
    for email in [p.email for p in get_colleagues(db)]:
        lb.insert(tk.END, email)

def union():
    lb.delete(0, 'end')
    for email in [p.email for p in get_all(db)]:
        lb.insert(tk.END, email)

def intersection():
    lb.delete(0, 'end')
    for email in [p.email for p in get_and(db)]:
        lb.insert(tk.END, email)
    
friends_button = tk.Button(right_frame, text='Friends', command=friends, **kwargs, width=10)
friends_button.grid(row=0, column=0, sticky='w')
colleagues_button = tk.Button(right_frame, text='Colleagues', command=colleagues, **kwargs, width=10)
colleagues_button.grid(row=0, column=1, sticky='w')
union_button = tk.Button(right_frame, text='All', command=union, **kwargs, width=10)
union_button.grid(row=0, column=2, sticky='w')
intersection_button = tk.Button(right_frame, text='And', command=intersection, **kwargs, width=10)
intersection_button.grid(row=0, column=3, sticky='w')   

tk.Label(right_frame, text='Recipients:', **kwargs).grid(row=5, column=0, sticky='w') 
recips = tk.Entry(right_frame, width=30, justify='left', font=my_font)
recips.grid(row=5, column=1, columnspan=3, sticky='w')

tk.Label(right_frame, text='Subject:   ', **kwargs).grid(row=6, column=0, sticky='w') 
subject = tk.Entry(right_frame, width=30, justify='left', font=my_font)
subject.grid(row=6, column=1, columnspan=3, sticky='w')

tk.Label(right_frame, text='Body:   ', **kwargs).grid(row=7, column=0, sticky='w') 
body=tk.Text(right_frame, height=16, width=44)
body.grid(row=8, column=0, columnspan=3)
sb = tk.Scrollbar(right_frame, orient='vertical', command=body.yview)
body.configure(yscrollcommand=sb.set)
sb.grid(row=8, column=3, sticky='nws')

def send():
    global smtp_connection
    from_addr = username.get() + '@' + '.'.join(domain.get().split('.')[1:])
    print('---', from_addr, '---')
    msg = email.message.EmailMessage(email.policy.SMTP)
    msg['To'] = recips.get()
    msg['From'] = from_addr
    msg['Subject'] = subject.get()
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()
    msg.set_content(body.get(1.0, 'end'))
    #msg = 'Subject: ' + subject.get() + '\n' + body.get(1.0, 'end')
    smtp_connection.send_message(msg)
    
def cancel():
    recips.delete(0, 'end')
    subject.delete(0, 'end')
    body.delete(1.0, 'end')
    
send_button = tk.Button(right_frame, command=send, text='Send', **kwargs, width=10)
send_button.grid(row=9, column=0)

cancel_button = tk.Button(right_frame, command=cancel, text='Cancel', **kwargs, width=10)
cancel_button.grid(row=9, column=1)

def _delete_window():
    global smtp_connection
    db.close()
    try:
        smtp_connection.quit()
    except Exception as e:
        print(e)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", _delete_window)

db = open_persons_db()
    
root.mainloop()
