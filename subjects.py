import sys
import imaplib
import getpass
import email
import email.header
import datetime
import sqlite3
import mp_cat #Import Categorization Program


# After successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "Inbox"


def process_mailbox(M, user_email,conn):
    c = conn.cursor()
    #c.execute("DROP TABLE IF EXISTS test1;") 
    c.execute("CREATE TABLE IF NOT EXISTS test1(From_email varchar(40), To_email varchar(40), Dates varchar(20), Subject varchar(50), Category varchar(20), PRIMARY KEY(From_email,To_email, Dates, Subject, Category));")
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in reversed(data[0].split()):
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        sender = msg['From']
        print('Subject: %s\n' % (subject))
        body = str(msg.get_payload(0))
        i1 = body.find('\n')
        body = body[i1+2:]
        #print('Body: %s\n' % (body))
        category = mp_cat.cat(body)
        print('Category: %s\n' % (category))
        #iprint(all_words)
        
        #print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            date = str(local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            print("\n\n")

        c.execute("INSERT or REPLACE INTO test1 VALUES('"+sender+"','"+user_email+"','"+date+"','"+subject+"','"+category+"');")
        conn.commit()
    conn.close()


def read_emails():
    conn = sqlite3.connect('Database1.db')
    EMAIL_ACCOUNT = input("Enter your email: ")
    M = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)

    print(rv, data)

    rv, mailboxes = M.list()
    '''
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)'''

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M, EMAIL_ACCOUNT, conn)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)

    M.logout()
def disp_emails():
	print("Select a category...\n\ta. Business\n\tb. Document editing or checking\n\tc. Employment arrangements\n\td. Logistic Arrangements\n\te. Personal but in professional context\n\tf. Purely Personal")
	selection = input("\tEnter selection: ")
	print("\n")
	conn = sqlite3.connect('Database1.db')
	c = conn.cursor()
	if selection == 'a':
		c.execute("SELECT * from test1 where Category='business';")
	elif selection == 'b':
		c.execute("SELECT * from test1 where Category='document_edit';")
	elif selection == 'c':
		c.execute("SELECT * from test1 where Category='employment_arrangements';")
	elif selection == 'd':
		c.execute("SELECT * from test1 where Category='logistic_arrangements';")
	elif selection == 'e':
		c.execute("SELECT * from test1 where Category='personal_prof';")
	elif selection == 'f':
		c.execute("SELECT * from test1 where Category='purely_personal';")
	data = c.fetchall()
	print('\n'.join(str(e) for e in data))
	print("\n")
	conn.commit()
	conn.close()
#read_emails()
