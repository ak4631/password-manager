from utils.dbconfig import dbconfig
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from rich.table import Table
from rich.console import Console

import utils.aesutil as uaes

def computeMasterKey(mp,ds):
    password=mp.encode()
    salt=ds.encode()
    key=PBKDF2(password,salt,32,count=1000000,hmac_hash_module=SHA512)
    return key

def retriveEntries(mp,ds,search,decryptPwd=False):
    db=dbconfig()
    cursor=db.cursor()

    query=""
    if len(search)==0:
        query="select * from pm.entries"
    else:
        query="select * from pm.entries where "
        for i in search:
            query+=f"{i} = '{search[i]}' AND "
        query=query[:-5]

    cursor.execute(query)
    results=cursor.fetchall()

    if len(results)==0:
        print("No results for the search")
        return

    if (decryptPwd and len(results)>1) or (not decryptPwd):
        table=Table(title="Results")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")
        for i in results:
            table.add_row(i[0],i[1],i[2],i[3],"{hidden}")
        console=Console()
        console.print(table)
        return

    if len(results)==1 and decryptPwd:
        mk=computeMasterKey(mp,ds)
        decrypted=uaes.decrypt(key=mk,source=results[0][4],keyType="bytes")

        print("Your password is ",decrypted.decode())

    db.close()
        

    
        
