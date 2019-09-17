from flask import Flask
from flask import request
import requests
from io import BytesIO
import sys
from github import Github
import os
import json
import datetime
import time
import calendar
import jwt


trained_dir = ".trained-issues"
keys_dir = ".keys"

port = sys.argv[1]
app = Flask(__name__)


@app.route('/getvalues', methods=['GET'])
def getJsoHandler():
    return {"values": "1234"}


def changlabel(token, label, user, project, number):
    g = Github(token)
    repo = g.get_repo(user+"/"+project)
    # repo.get_issue(int(number)).edit(labels=label)
    repo.get_issue(int(number)).add_to_labels(label)


def get_key_0():
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend

    with open(f'{keys_dir}/wk-j-issue-bot.2019-09-17.private-key.pem', 'rb') as fh:
        # signing_key = jwk_from_pem(fh.read())
        signing_key = fh.read()

    cert_obj = load_pem_x509_certificate(signing_key, default_backend())
    public_key = cert_obj.public_key()


def register():
    # from Crypto.PublicKey import RSAAlgorithm
    from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
    jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


def get_key():
    # from Crypto.PublicKey import RSA

    register()

    with open(f'{keys_dir}/wk-j-issue-bot.2019-09-17.private-key.pem', 'rb') as fh:
        data = fh.read()
        # private_key = RSA.importKey(data)
    # return private_key
    return data


def genToken(appid):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    exp = calendar.timegm(exp.timetuple())
    message = {
        'iat': int(time.time()),
        'exp': exp,
        'iss': 40736,
    }
    signing_key = get_key()
    compact_jws = jwt.encode(message, signing_key, 'RS256')
    data = {'Authorization': f'Bearer {compact_jws}',
            'Accept': 'application/vnd.github.machine-man-preview+json'}
    r = requests.post(
        url=f"https://api.github.com/app/installations/{appid}/access_tokens", headers=data)
    data = r.json()
    token = data["token"]
    return token


def predic(text):
    import dill as pickle
    from pythainlp.tokenize import word_tokenize
    with open(f'{trained_dir}/vocabulary.data', 'rb') as file:
        vocabulary = pickle.load(file)
    with open(f'{trained_dir}/model.data', 'rb') as file:
        classifier = pickle.load(file)
    featurized_test_sentence = {
        i: (i in word_tokenize(text.lower())) for i in vocabulary}
    # ใช้โมเดลที่ train ประมวลผล
    label = classifier.classify(featurized_test_sentence)
    return label

# ลบ <>


def deltag(msg):
    item = msg.split("<")
    if len(item) > 1:
        msg = item[0]
        for i in item:
            dt = i.split(">")
            j = 1
            while j < len(dt):
                msg = msg+dt[j]
                j = j+1
    return msg

# ลบ รูป


def delimg(msg):
    item = msg.split("![")
    if len(item) > 1:
        msg = item[0]
        for i in item:
            dt = i.split(")")
            j = 1
            while j < len(dt):
                msg = msg+dt[j]
                j = j+1
    return msg


def clean_msg(msg):
    import re
    import string
    # ลบ image
    msg = delimg(msg)
    # ลบ <>
    msg = deltag(msg)
    # ลบ text ที่อยู่ในวงเล็บ <> ทั้งหมด
    msg = re.sub(r'<.*?>', '', msg)
    # ลบ hashtag
    msg = re.sub(r'#', '', msg)
    # ลบ เครื่องหมายคำพูด (punctuation)
    for c in string.punctuation:
        msg = re.sub(r'\{}'.format(c), '', msg)
    # ลบ separator เช่น \n \t
    # msg = ' '.join(msg.split())
    return msg


@app.route('/github', methods=['POST'])
def github():
    content = request.get_json()
    action = content["action"]
    if action == "opened":
        title = content["issue"]["title"]
        description = content["issue"]["body"]
        number = content["issue"]["number"]
        project = content["repository"]["name"]
        appid = content["installation"]["id"]
        userfull = content["repository"]["full_name"]
        tokenUser = userfull.split("/")
        user = tokenUser[0]
        pretitle = clean_msg(title)
        preDes = clean_msg(description)
        text = pretitle+preDes
        label = predic(text)
        token = genToken(appid)
        changlabel(token, label, user, project, number)
    return "Complete"


app.run(debug=True, host='0.0.0.0', port=port)
