from utils.dbconfig import dbconfig
from getpass import getpass
import hashlib
import string
import random

def generatedeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))

def config():
    #Create a Database
    db=dbconfig()
    cursor = db.cursor()
    print("---Creating a Database---")
    try:
        cursor.execute("Create Database pm")
    except Exception as e:
        print("!!Error Occured!!")
        sys.exit(0)
    print("-$-Database Created-$-")

    #create tables
    query="create table pm.secrets (masterkey_hash TEXT NOT NULL,device_secret TEXT NOT NULL)"
    res=cursor.execute(query)
    print("Table 'Secrets' Successfully")

    query="create table pm.entries (sitename TEXT NOT NULL,siteURL TEXT NOT NULL,email TEXT,username TEXT,password TEXT NOT NULL)"
    res=cursor.execute(query)
    print("Table 'Entries' Created")


    while 1:
        mp=getpass(' Chooose a Master Passsword: ')
        if mp==getpass("Re-type: ") and mp!="":
            break
        print("!!Please Try Again!!")

    #Hash the MASTER PWD

    hashed_mp=hashlib.sha256(mp.encode()).hexdigest()
    print("-$-Generated a Master Password-$-")

    #Generate Device Secret
    ds=generatedeviceSecret()
    print("-$-Device Sceret Generated-$-")

    #Adding Master Password to Database
    query="insert into pm.secrets(masterkey_hash,device_secret) values (%s,%s)"
    val=(hashed_mp,ds)
    cursor.execute(query,val)
    db.commit()

    print("---Added to Database----")
    print("---Configuration Done---")

    db.close()



config()
