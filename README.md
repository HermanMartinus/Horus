# Horus
## The keeper of the keys

Horus is a simple, terminal-based password manager and 2FA generator.
Instead of saving passwords, Horus generates passwords using MD5 hashing of the account name and secret seed phrase and copies it directly to the clipboard.

## Installation
Clone repo/download raw
Change permissions on `setup.sh` file (if necessary)
```
$ chmod +x setup.sh
```
Run the `setup.sh` file
```
$ ./setup.sh
```
Add the this line to `.profile` or `.bash_profile` in your home directory:
```
export PATH=$PATH":$HOME/pwd"
```
Check that it's installed
```
$ horus
```

## Password manager
Set your seed phrase and remember it forever, it will act as your master password.
```
$ horus --seed "Super secret seed phrase"
```
Generate/get password for service
```
$ horus --pwd <service-name>
```
Should copy something like `&B572AD8ef1f939%` to the clipboard.

## 2FA generator
Add 2fa service
```
$ horus --atfa <service-name>
$ Paste the 2fa secret: <2fa-secret-key>
```
Get 2fa key
```
$ horus --tfa <service-name>
```
