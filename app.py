from flask import Flask, render_template, url_for, request, make_response, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField, SubmitField
import json
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jkbdsabdn23ub32u@#$@#!@$!@#'
app.config['DEBUG'] = True
Bootstrap(app)

class encryptform(FlaskForm):
    plaintext = TextAreaField("Plaintext", validators=[DataRequired()])
    keyPadding = IntegerField("KeyPadding", validators=[DataRequired()])
    key2 = StringField("Key2", validators=[DataRequired()])
    # submit = SubmitField("encrypt")

class decryptform(FlaskForm):
    chipertext = TextAreaField("chipertext", validators=[DataRequired()])
    keyPadding = IntegerField("keyPadding", validators=[DataRequired()])
    key2 = StringField("key2", validators=[DataRequired()])
    # submit = SubmitField("decrypt")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/encrypt')
def enc():
    form = encryptform()
    return render_template("encrypt.html", form=form)

@app.route('/encrypt/proc', methods=['POST'])
def encrypt():
    form = encryptform()
    response = ""
    if request.method == "POST":
        plaintext = form.plaintext.data
        keyPadding = form.keyPadding.data
        key2 = form.key2.data
        mentah = proccess_caesar(plaintext, keyPadding)
        setengah = vigenere(mentah,key2)
        mateng = proccess_rail_fence(setengah,keyPadding)
        response = make_response(json.dumps(mateng))
        response.content_type = 'application/json'
    return response
    # else:
    #     return redirect('/encrypt')

def proccess_caesar(plaintext,padding):
    mentah = []
    for i in range(len(plaintext)):
        if i%2 == 0:
            if 33 <= ord(plaintext[i]) <= 47:
                mentah.append(chr((ord(plaintext[i]) + (padding+2)) %33 % 14 + 33))
            elif 48 <= ord(plaintext[i]) <= 57:
                mentah.append(chr((ord(plaintext[i])+ (padding+2)) % 48 % 10 + 48))
            elif 58 <= ord(plaintext[i]) <= 64:
                mentah.append(chr((ord(plaintext[i])+ (padding+2)) % 58 % 7 + 58))
            elif 65 <= ord(plaintext[i]) <= 90:
                mentah.append(chr((ord(plaintext[i]) + (padding+2)) % 65 % 26 + 65))
            elif 91 <= ord(plaintext[i]) <= 96:
                mentah.append(chr((ord(plaintext[i]) + (padding+2)) % 91 % 6 + 91))
            elif 97 <= ord(plaintext[i]) <= 122:
                mentah.append(chr((ord(plaintext[i])+ (padding+2)) % 97 % 26 + 97))
            elif 123 <= ord(plaintext[i]) <= 126:
                mentah.append(chr((ord(plaintext[i]) + (padding+2)) % 123 % 4 + 123))
            else:
                mentah.append(plaintext[i])
        else:
            if 33 <= ord(plaintext[i]) <= 47:
                mentah.append(chr((ord(plaintext[i]) + (padding+3)) %33 % 14 + 33))
            elif 48 <= ord(plaintext[i]) <= 57:
                mentah.append(chr((ord(plaintext[i])+ (padding+3)) % 48 % 10 + 48))
            elif 58 <= ord(plaintext[i]) <= 64:
                mentah.append(chr((ord(plaintext[i])+ (padding+3)) % 58 % 7 + 58))
            elif 65 <= ord(plaintext[i]) <= 90:
                mentah.append(chr((ord(plaintext[i]) + (padding+3)) % 65 % 26 + 65))
            elif 91 <= ord(plaintext[i]) <= 96:
                mentah.append(chr((ord(plaintext[i]) + (padding+3)) % 91 % 6 + 91))
            elif 97 <= ord(plaintext[i]) <= 122:
                mentah.append(chr((ord(plaintext[i])+ (padding+3)) % 97 % 26 + 97))
            elif 123 <= ord(plaintext[i]) <= 126:
                mentah.append(chr((ord(plaintext[i]) + (padding+3)) % 123 % 4 + 123))
            else:
                mentah.append(plaintext[i])

    return ''.join(mentah)

def vigenere(mentah,key2):
    universe = [c for c in (chr(i) for i in range(32,127))]
    uni_len = len(universe)
    k_len = len(key2)
    ret_plain= ""
    for i,l in enumerate(mentah):
        if l not in universe:
            ret_plain += 1
        else:
            plain_index = universe.index(l)
            k = key2[i % k_len]
            key_index = universe.index(k)
            code = universe[(plain_index+key_index)%uni_len]
            ret_plain += code
    return ret_plain

def proccess_rail_fence(plain, rails, offset=0):
    cipher = ''
    plain = '#'*offset + plain
    length = len(plain)
    fence = [['#']*length for _ in range(rails)]
    rail = 0
    for x in range(length):
        fence[rail][x] = plain[x]
        if rail >= rails-1:
            dr = -1
        elif rail <= 0:
            dr = 1
        rail += dr
    for rail in range(rails):
        for x in range(length):
            if fence[rail][x] != '#':
                cipher += fence[rail][x]
    return cipher


@app.route('/decrypt')
def decrypt():
    form = decryptform()
    return render_template('decrypt.html', form = form)

@app.route('/decrypt/proc', methods=['POST'])
def decrypt2():
    form = decryptform()
    response = ""
    if request.method == "POST":
        chipertext = form.chipertext.data
        keyPadding = form.keyPadding.data
        key2 = form.key2.data
        mentah = decrypt_rail_fence(chipertext, keyPadding)
        setengah = decrypt_vigenere(mentah,key2)
        mateng = proccess_caesar(setengah,keyPadding)
        response = make_response(json.dumps(mateng))
        response.content_type = 'application/json'
    return response
    # else:
    #     return redirect('/decrypt')


def decrypt_rail_fence(cipher, rails, offset=0):
    plain = ''
    if offset:
        t = proccess_rail_fence('o' * offset + 'x' * len(cipher), rails)
        for i in range(len(t)):
            if (t[i] == 'o'):
                cipher = cipher[:i] + '#' + cipher[i:]

    length = len(cipher)
    fence = [['#'] * length for _ in range(rails)]
    i = 0
    for rail in range(rails):
        p = (rail != (rails - 1))
        x = rail
        while (x < length and i < length):
            fence[rail][x] = cipher[i]
            if p:
                x += 2 * (rails - rail - 1)
            else:
                x += 2 * rail
            if (rail != 0) and (rail != (rails - 1)):
                p = not p
            i += 1
    for i in range(length):
        for rail in range(rails):
            if fence[rail][i] != '#':
                plain += fence[rail][i]
    return plain

def decrypt_vigenere(plaintext, key2):
    universe = [c for c in (chr(i) for i in range(32,127))]
    uni_len = len(universe)
    k_len = len(key2)
    ret_plain = ""
    for i,l in enumerate(plaintext):
        if l not in universe:
            ret_plain += 1
        else:
            plain_index = universe.index(l)
            k = key2[i % k_len]
            key_index = universe.index(k)
            key_index *= -1
            code = universe[(plain_index+key_index)%uni_len]
            ret_plain += code
    return ret_plain

def proccess_caesar(plaintext,padding):
    mentah = []
    for i in range(len(plaintext)):
        if i%2 == 0:
            if 33 <= ord(plaintext[i]) <= 47:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) %33 % 14 + 33))
            elif 48 <= ord(plaintext[i]) <= 57:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 48 % 10 + 48))
            elif 58 <= ord(plaintext[i]) <= 64:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 58 % 7 + 58))
            elif 65 <= ord(plaintext[i]) <= 90:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 65 % 26 + 65))
            elif 91 <= ord(plaintext[i]) <= 96:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 91 % 6 + 91))
            elif 97 <= ord(plaintext[i]) <= 122:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 97 % 26 + 97))
            elif 123 <= ord(plaintext[i]) <= 126:
                mentah.append(chr((ord(plaintext[i]) - (padding+2)) % 123 % 4 + 123))
            else:
                mentah.append(plaintext[i])
        else:
            if 33 <= ord(plaintext[i]) <= 47:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) %33 % 14 + 33))
            elif 48 <= ord(plaintext[i]) <= 57:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) % 48 % 10 + 48))
            elif 58 <= ord(plaintext[i]) <= 64:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) % 58 % 7 + 58))
            elif 65 <= ord(plaintext[i]) <= 90:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) % 65 % 26 + 65))
            elif 91 <= ord(plaintext[i]) <= 96:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) % 91 % 6 + 91))
            elif 97 <= ord(plaintext[i]) <= 122:
                mentah.append(chr((ord(plaintext[i]) - (padding+3)) % 97 % 26 + 97))
            elif 123 <= ord(plaintext[i]) <= 126:
                mentah.append(chr((ord(plaintext[i]) + (padding+3)) % 123 % 4 + 123))
            else:
                mentah.append(plaintext[i])

    return ''.join(mentah)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8090)
