from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "customer"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/customers", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from customers""")
    return make_response(jsonify(data), 200)


@app.route("/customers/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM customers where customer_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/customers", methods=["POST"])
def add_customerr():
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["customer_first_name"]
    last_name = info["customer_last_name"]
    gender = info["gender"]
    email = info["email_address"]
    phone = info["phone_number"]
    address = info["address"]
    town = info["town_city"]
    country = info["country"]
    cur.execute(
        """ INSERT INTO customers (customer_first_name, customer_last_name,gender,email_address,phone_number,address,town_city,country) VALUE (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (first_name, last_name,gender,email,phone,address,town,country),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/customers/<int:id>", methods=["PUT"])
def update_cutomer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["customer_first_name"]
    last_name = info["customer_last_name"]
    gender = info["gender"]
    email = info["email_address"]
    phone = info["phone_number"]
    address = info["address"]
    town = info["town_city"]
    country = info["country"]
    cur.execute(
        """ UPDATE customers SET customer_first_name = %s, customer_last_name = %s, gender = %s,email_address = %s,phone_number = %s,address = %s,town_city = %s,country = %s WHERE customer_id = %s """,
        (first_name, last_name,gender,email,phone,address,town,country, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_cutomer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM customers where customer_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer deleted successfully", "rows_affected": rows_affected}
        ), 
        200,
    )

@app.route("/customers/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)