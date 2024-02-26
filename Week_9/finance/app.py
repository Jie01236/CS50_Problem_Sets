import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id= ? GROUP BY symbol", user_id)
    money_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    money = money_db[0]["cash"]
    for row in transactions_db:
        row["total"] = row["shares"] * row["price"]

    return render_template("index.html", data = transactions_db, money=money,usd_format=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method=="GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not shares.isdigit():
            return apology("Please enter a valid number of shares")

        shares = int(shares)

        if not symbol:
            return apology("please give a symbol")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("sorry, we didn't find it")

        if shares <= 0:
            return apology("please choose a positive number")

        transactions_value = shares * stock["price"]
        user_id = session["user_id"]

        #user_money 是一个列表，其中包含一个字典作为其唯一的元素 （db.execute 通常是一个表示查询结果的列表)
        user_money = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        #这个字典有一个键 "cash" 赋值给money
        money = user_money[0]["cash"]

        if money < transactions_value:
            return apology ("sorry, there isn't enough money")
        update_money = money - transactions_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_money, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol,shares, price, date) VALUES(?,?,?,?,?)", user_id, stock["symbol"],shares, stock["price"], date)

        flash("Bought")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions = transactions_db,usd_format=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET": # display quote page for typying the symbol
        return render_template("quote.html")
    else: #show the resulte of searching
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("please give a symbol")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("sorry, we didn't find it")
        return render_template("quoted.html", name = stock["name"], price = stock["price"], symbol = stock["symbol"],usd_format=usd)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET": # display registration form
        return render_template("regis_form.html")
    else:  # insert the new user into users table then log user in
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        #check for possible errors
        if not username:
            return apology("please give a username")
        if not password:
            return apology("please give a password")
        if not confirmation:
            return apology("please confirm password")
        if password != confirmation:
            return apology("password do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)

        except:
            return apology("username already existed")

        session["user_id"] = new_user

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method=="GET":
        user_id = session["user_id"]
        symbol_bought = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbol_bought])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("please give a symbol")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("sorry, we didn't find it")
        if shares < 0:
            return apology("please choose a positive number")

        transactions_value = shares * stock["price"]
        user_id = session["user_id"]

        #user_money 是一个列表，其中包含一个字典作为其唯一的元素 （db.execute 通常是一个表示查询结果的列表)
        user_money = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        #这个字典有一个键 "cash" 赋值给money
        money = user_money[0]["cash"]

        users_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        users_shares_new = users_shares[0]["shares"]
        if shares > users_shares_new:
            return apology("sorry, you don't have enough shares")

        update_money = money + transactions_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_money, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol,shares, price, date) VALUES(?,?,?,?,?)", user_id, stock["symbol"],(-1)*shares, stock["price"], date)

        flash("Sold!")
        return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """add cash"""
    if request.method=="GET":
        return render_template("add.html")
    else:
        new_money = int(request.form.get("add"))
        if not new_money:
            return apology("please write a number")

        user_id = session["user_id"]
        user_money = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        money = user_money[0]["cash"]

        update_money = money + new_money

        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_money, user_id)
        return redirect("/")