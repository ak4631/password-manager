from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from utils.dbconfig import dbconfig

import utils.aesutil as uaes

def computeMasterKey(mp,ds):
    password=mp.encode()
    salt=ds.encode()
    key=PBKDF2(password,salt,32,count=1000000,hmac_hash_module=SHA512)
    return key


def addEntry(mp,ds,sitename,siteurl,email,username):
    #get the password
    password=getpass("Password: ")

    mk=computeMasterKey(mp,ds)

    encrypted=uaes.encrypt(key=mk,source=password,keyType="bytes")

    #Add Password to db
    db=dbconfig()
    cursor=db.cursor()
    query="insert into pm.entries(sitename,siteurl,email,username,password) values (%s,%s,%s,%s,%s)"
    val=(sitename,siteurl,email,username,encrypted)
    cursor.execute(query,val)
    db.commit()

    print("Entry Added")
