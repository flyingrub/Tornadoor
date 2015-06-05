# SSWOD
Secure System Which Opens a Door

## What is this ?
This project aims to create a server and a relation between a phone and a Raspberry Pi to open a door from the web, securely.
It runs [Tornado](http://www.tornadoweb.org/en/stable/) with tls.

## How does it works ?
* Client 
 * hello
* Server : 
 * alea `myaleastring`
* Client 
 * `mypin` pin `myaleastring`
* Server 
 * Opens the door if mypin is equal to is own secret pin and myaleastring is equal to the one he sent.


## Generate Keys :

Server Key :
```
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt
openssl x509 -in server.crt -out server.pem
```

keystore, for android client :
```
 keytool -import -alias stan -file server.crt -keystore certstore
```

## Android Client : 
https://github.com/flyingrub/SecureKey
