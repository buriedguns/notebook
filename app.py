from contextlib import closing
import re

from flask import Flask, make_response, jsonify, request
import sqlite3

app = Flask(__name__)


def execute(*sql, get_id=False):
    with closing(sqlite3.connect("sample.db")) as connection:
        cur = connection.cursor()
        try:
            cur.execute(*sql)
            connection.commit()
        except Exception as exc:
            print(exc)
        if cur.description:
            return cur.fetchall()
        if get_id:
            return cur.lastrowid


@app.route('/get-all', methods=["GET"])
def get_all_info():
    raw_info = execute("SELECT * FROM phonebook")
    response = []
    for i in raw_info:
        data = {
            "id": i[0],
            "name": i[1],
            "phone": i[2]
        }
        response.append(data)

    return make_response(jsonify(response), 200)


@app.route('/add-phone', methods=["POST"])
def add_new_phone():
    content = request.json
    name = content.get("name")
    phone = content.get("phone")
    phone_regex = r'\+\d{11}'

    errors = {
        "name": "The name param is not set",
        "phone": "The phone param is not set",
        "wrong_format": "The format of phone number should be: '+7**********'"
    }

    if not name:
        return make_response(jsonify(errors["name"]), 400)
    if not phone:
        return make_response(jsonify(errors["phone"]), 400)
    if not re.search(phone_regex, phone):
        return make_response(jsonify(errors["wrong_format"]), 400)

    phonebook_id = execute(f"INSERT INTO phonebook(name, phone) VALUES('{name}', '{phone}')", get_id=True)
    response = {
        "message": "Congrats! The phone has been added",
        "phone_info": {
            "id": phonebook_id,
            "name": name,
            "phone": phone
        }
    }

    return make_response(jsonify(response), 200)


@app.route('/remove-phone/<raw_phone_id>', methods=["DELETE"])
def remove_phone_by_id(raw_phone_id):
    try:
        phone_id = int(raw_phone_id)
    except ValueError:
        return make_response(jsonify("Please use the ID number to delete the phone"), 400)
    response = {"message": f"The phone with ID: {phone_id} is not present in DB anymore"}
    execute(f"DELETE FROM phonebook WHERE id = '{phone_id}'")
    return make_response(jsonify(response), 200)


@app.route('/search/<name>', methods=["GET"])
def search_by_name(name):
    raw_info = execute(f"SELECT * FROM phonebook WHERE name='{name}' COLLATE NOCASE")
    response = []
    for i in raw_info:
        data = {
            "id": i[0],
            "name": i[1],
            "phone": i[2]
        }
        response.append(data)

    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    execute("CREATE TABLE IF NOT EXISTS phonebook(id INTEGER PRIMARY KEY ASC AUTOINCREMENT, name text, phone text)")
    app.run()
