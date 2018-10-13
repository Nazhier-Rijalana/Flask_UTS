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
            mentah.append(plaintext[i].encode('rot12'))
        else:
            mentah.append(plaintext[i].encode('rot13'))
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

def fence_pattern(rails, size):
    zig_zag = cycle(chain(range(rails), range(rails - 2, 0, -1)))
    return zip(zig_zag, range(size))


def proccess_rail_fence(msg, rails):
    fence = fence_pattern(rails, len(msg))
    return ''.join(msg[i] for _, i in sorted(fence))


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


def decrypt_rail_fence(msg, rails):
    fence = fence_pattern(rails, len(msg))
    fence_msg = zip(msg, sorted(fence))
    return ''.join(
        char for char, _ in sorted(fence_msg, key=lambda item: item[1][1]))

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
            mentah.append(plaintext[i].decode('rot12'))
        else:
            mentah.append(plaintext[i].decode('rot13'))
    return ''.join(mentah)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8090)
