from flask import Flask, render_template, url_for, request, make_response, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField, SubmitField
import json
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from hackercodecs import *
from itertools import cycle, chain


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jkbdsabdn23ub32u@#$@#!@$!@#'
app.config['DEBUG'] = True
Bootstrap(app)

class encryptform(FlaskForm):
    plaintext = TextAreaField("Plaintext", validators=[DataRequired()])
    keyPadding = IntegerField("KeyPadding", validators=[DataRequired()])
    key2 = StringField("Key2", validators=[DataRequired()])
    submit = SubmitField("encrypt")

class decryptform(FlaskForm):
    chipertext = TextAreaField("chipertext", validators=[DataRequired()])
    keyPadding = IntegerField("keyPadding", validators=[DataRequired()])
    key2 = StringField("key2", validators=[DataRequired()])
    submit = SubmitField("decrypt")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/encrypt', methods=['GET','POST'])
def enc():
    form = encryptform()
    mateng = ""
    print "disini12"
    if request.method == 'POST':
        print "disini"
        plaintext = form.plaintext.data
        keyPadding = form.keyPadding.data
        key2 = form.key2.data
        mentah = proccess_caesar_encrypt(plaintext)
        setengah = vigenere(mentah,key2)
        mateng = proccess_rail_fence(setengah,keyPadding)
    return render_template("encrypt.html", form=form, mateng=mateng)

def proccess_caesar_encrypt(plaintext):
    mentah = []
    for i in range(len(plaintext)):
        if i%2 == 0:
            mentah.append(plaintext[i].encode('rot12'))
        else:
            mentah.append(plaintext[i].encode('rot13'))
    return str(''.join(mentah))

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

def pattern(height, width):
    n = 2 * (height - 1)
    positions = (min(x, n - x) for x in cycle(range(n)))
    return sorted(zip(positions, range(width)))


def proccess_rail_fence(xs, height):
    positions = pattern(height, len(xs))
    return ''.join(xs[i] for _, i in positions)


@app.route('/decrypt', methods=['GET','POST'])
def decrypt():
    form = decryptform()
    mateng = ""
    if request.method == "POST":
        print "disini"
        chipertext = form.chipertext.data
        keyPadding = form.keyPadding.data
        key2 = form.key2.data
        mentah = decrypt_rail_fence(chipertext,keyPadding)
        setengah = decrypt_vigenere(mentah,key2)
        mateng = proccess_caesar(setengah)
    return render_template('decrypt.html', form = form, mateng=mateng)

def decrypt_rail_fence(xs, height):
    positions = pattern(height, len(xs))
    rectified = sorted(enumerate(positions), key=lambda t: t[1][1])
    return ''.join(xs[i] for i, _ in rectified)

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

def proccess_caesar(plaintext):
    mentah = []
    for i in range(len(plaintext)):
        if i%2 == 0:
            mentah.append(plaintext[i].decode('rot12'))
        else:
            mentah.append(plaintext[i].decode('rot13'))
    return str(''.join(mentah))


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8090)
