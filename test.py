import jwt

with open(".keys/bot-label.pem", 'r') as rsa_priv_file:
    priv_rsakey = rsa_priv_file.read()
