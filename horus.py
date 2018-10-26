#!/usr/bin/env python
import argparse, os
import json
import hmac, base64, struct, hashlib, time
import hashlib

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'authenticator.json')
jsonFile = open(file_path, "r")
data = json.load(jsonFile)
jsonFile.close()

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

def get_otp(account):
    if account in data['accounts']:
        one_time_password = get_totp_token(data['accounts'][account]['secret'])
        return one_time_password
    else:
        return False

def add_otp(service, secret):
    data['accounts'][service] = {"secret": secret}
    jsonFile = open(file_path, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    print ('2fa account added')

def add_seed(seed):
    data['seed'] = seed
    jsonFile = open(file_path, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    print ('Seed added')

def create_password(service):
    special_characters = "!@#$%^&*()/"
    if data['seed'] and len(data['seed']) > 0:
        combo = service + data['seed']
        hash_object = hashlib.md5(combo.encode())
        password = hash_object.hexdigest()
        password = "{0}{1}{2}{3}".format(
            special_characters[len(service) % 10],
            password[0:7].upper(),
            password[8:15].lower(),
            special_characters[10-(len(service) % 10)],
            )
        return password
    else:
        print ("You first need to set your seed phrase. See the Horus docs for instructions")
        return False

def copy_to_clipboard(text):
    os.system("echo '%s' | pbcopy" % (text))
    print ('<copied to clipboard>')

parser = argparse.ArgumentParser()
parser.add_argument('--pwd', '-p', help='Get/generate password')
parser.add_argument('--seed', '-s', help='Set seed phrase')
parser.add_argument('--tfa', help='Get 2fa code')
parser.add_argument('--atfa', help='Add 2fa code')
if parser.parse_args().pwd:
    password = create_password(parser.parse_args().pwd.lower())
    if password:
        copy_to_clipboard(password)
elif parser.parse_args().seed:
    add_seed(parser.parse_args().seed.lower())
elif parser.parse_args().tfa:
    tfa = get_otp(parser.parse_args().tfa.lower())
    if tfa:
        copy_to_clipboard(tfa)
    else:
        print ("Account does not exist")
elif parser.parse_args().atfa:
    add_otp(parser.parse_args().atfa.lower(), raw_input("Paste the 2fa secret: "))
else:
    print ('Horus - Keeper of the keys')
