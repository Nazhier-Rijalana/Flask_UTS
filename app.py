from flask import Flask, render_template, url_for
import json
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/encrypt')

@app.route('/encrypt/proc')
def encrypt():
    return "test"

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

def vigenere():
    pass

def proccess_rail_fence():
    pass


@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')

@app.route('/decrypt/proc')
def decrypt():
    return "Pass"

def decrypt_rail_fence():
    pass

def decrypt_vigenere():
    pass

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
    app.run()
