import argparse
from getpass import getpass
import hashlib

import utils.add
import utils.retrieve
import utils.generate
from utils.dbconfig import dbconfig



def inputAndValidateMasterPassword():
    mp = getpass("MASTER PASSWORD: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
            print("WRONG!")
            return None

    return [mp,result[1]]

def main():
    print("""What do you want to do?
    (1) Add a password
    (2) Extract password
    (3) Generate
    (q) Quit
    """)

    done=False

    while not done:
        print("--------------------------")
        choice = input("Enter your Choice: ")
        print("--------------------------")
        if choice == "1":
            print("---------Adding Credentials-----------------")
            name=input("Enter Site Name: ")
            url=input("Enter Site URL: ")
            login=input("Enter Username: ")
            email=input("Enter your email: ")
            if name==None or url==None or login==None:
                
                if name==None:
                    print("Site Name is Required")
                if url==None:
                    print("Site Url is Required")
                if login==None:
                    print("Site Username is Required")

                return
            
            if email==None:
                email=""

            res=inputAndValidateMasterPassword()
            
            if res is not None:
                utils.add.addEntry(res[0],res[1],name,url,email,login)
            
               
        elif choice=="2":
            print("--------Extracting Data-------")
            print("--------------------------")
            print("If Dont Know the Enter 'N'")
            print("--------------------------")
            name=input("Enter Site Name: ")
            url=input("Enter Site URL: ")
            login=input("Enter Username: ")
            email=input("Enter your email: ")
            res=inputAndValidateMasterPassword()
            search={}
            if name is not None and name!="N":
                search["sitename"]=name
            if url is not None and url!="N":
                search["siteurl"]=url
            if email is not None and email!="N":
                search["email"]=email
            if login is not None and login!="N":
                search["username"]=login

            if res is not None:
                utils.retrieve.retriveEntries(res[0],res[1],search,True)
                


        elif choice=="3":
            print("------------Random Pass--------------")
            length=int(input("Enter length: "))
            if length==None:
                print("Length is required")
                return
            password=utils.generate.generatePassword(length)
            print("Password is: ",password)

            
        elif choice == 'q':
            done=True
            print("Bye")

        else:
            print("Invalid Choice!")

    
    
    
main()

















    
