from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# Create Database
conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

conn.commit()
conn.close()


@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            """
            INSERT INTO users
            (fullname,email,password,role)
            VALUES (?,?,?,?)
            """,
            (fullname, email, password, role)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        user = c.fetchone()

        conn.close()

        if user:
            session["email"] = email
            session["fullname"] = user[1]
            session["role"] = user[4]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        role=session["role"]
    )


# FORGOT PASSWORD
@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


# RESET PASSWORD
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if request.method == "POST":

        email = request.form["email"]
        new_password = request.form["new_password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            """
            UPDATE users
            SET password=?
            WHERE email=?
            """,
            (new_password, email)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("reset_password.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)