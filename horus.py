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
        return "Account does not exist"

def add_otp(service, secret):
    data['accounts'][service] = {"secret": secret}
    jsonFile = open(file_path, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def create_password(service):
    combo = service + data['seed']
    hash_object = hashlib.md5(combo.encode())
    password = hash_object.hexdigest()
    password = "@{0}{1}!".format(password[0:7].upper(), password[8:15].lower())
    return password

def set_seed(seed):
    data['seed'] = seed
    jsonFile = open(file_path, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

parser = argparse.ArgumentParser()
parser.add_argument('--pwd', help='Get/generate password')
parser.add_argument('--seed', help='Set password seed')
parser.add_argument('--tfa', help='Get 2fa code')
parser.add_argument('--atfa', help='Add 2fa code')
if parser.parse_args().pwd:
    os.system("echo '%s' | pbcopy" % (create_password(parser.parse_args().pwd.lower())))
    print ('<copied to clipboard>')
elif parser.parse_args().tfa:
    tfa = get_otp(parser.parse_args().tfa.lower())
    os.system("echo '%s' | pbcopy" % tfa)
    print tfa, '- <copied to clipboard>'
elif parser.parse_args().atfa:
    add_otp(parser.parse_args().atfa.lower(), raw_input("Paste the 2fa secret: "))
elif parser.parse_args().seed:
    set_seed(parser.parse_args().seed.lower())
