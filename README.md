# Personal-Passvault
 A flask application (Python) which can be used to store you creds and use without unwanted eavesdropping .
 This Application is an offline passvault using standard python cryto libraries . Hence comes with some manual maintenance for portability.
 The crux of the storage and security revolves around the file "secret_file.json" , Make sure the file is only accesible by you. 
 
 Install Dependencies --  *pip install -r requirements.txt*
 To Run type *Python app.py* and the app will be up at *localhost:5000*
 ## Target Audience:
 
        * For people who wish to use credentials and in public places or within crowds
        * The application lets you copy creds without disclosing the value hence cannot be shouldersurfed
        * Simple operations to add/remove and view the credentials
        * Highly portable , copy the file "secret_file.json" any where u want and pull code from github and u have your app ready.
        * Minimal configuration and maintenance needed 
        * Extremely usefull if you want keep your creds offline and to know how and where they are stored.
        * Easy to modify and use your own crypto library

## Cons:
Making it minimalist have its own limitations

        - The file "secret_file.json" is encrpted but not using the hardest crypto available hence any weaknes in standard python crypto do apply.
        - App is offline hence u cannot retrieve creds from another device
        - You need to carry the "secret_file.json" /code project wherever u need your creds
        - There is no master password recovery , update creds and many functionality available (at the moment)


## Quick guide:

        - First time you run the app provide a password (master password) , which is used to encrypt you creds and is tied to you secret_file.json
        - You cannot update the master password hence if you need to change remove the secret file (that involves permanent loss of creds stored within)
        - Once you enter the correct password on successive logins , you can add passwords and has a provision to search creds using the domain name ("gmail")
        - Closing a card (password tiles) would remove the cred .
        - you cannot update a password tile - create a new one ! 


* Note - Functionalities would keep updated but the core idea of minimalist and simplicity would remain . 

