import hashlib

import pymongo
from flask import request, jsonify
from flask_keyvault import KeyVault, KeyVaultAuthenticationError

from . import app

key_vault = KeyVault()
print('Initializing key vault')
key_vault.init_app(app=app)
print('Initialized key vault')

key_vault_url = 'https://cloud-ra-key-vault.vault.azure.net/'


def encrypt(s: str):
    return hashlib.sha256(s.encode()).hexdigest()


@app.route('login', methods=['POST'])
def login():
    global key_vault_url, key_vault
    output = jsonify({'ok': False, 'message': 'Bad request method!'}), 400

    data = request.get_json()
    print('Received data from request: ' + str(data))

    if request.method == 'POST':
        print('Received a post request')
        if data.get('email', None) is not None and data.get('password', None):
            try:
                user = key_vault.get(key_vault_url, 'dbUser')
                password = key_vault.get(key_vault_url, 'dbPassword')
                mongo_uri = "mongodb+srv://%s:%s@cluster0-m83c8.mongodb.net/test?retryWrites=true&w=majority" % (
                    user, password)
                print('Connection URI ' + mongo_uri)
                client = pymongo.MongoClient(mongo_uri)
                db = client.flaskVault

                user = db.user.find_one({'email': data.get('email'), 'password': encrypt(data.get('password'))})
                if user:
                    output = jsonify({'ok': True, 'message': '%s %s logged in.' % (
                        user.get('first_name'), user.get('last_name'))}), 200
                else:
                    output = jsonify({'ok': False, 'message': 'Bad user credentials!'}), 400

            except KeyVaultAuthenticationError as error:
                output = jsonify({'ok': False, 'message': 'Bad vault configuration!'}), 400
        else:
            output = jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    return output
