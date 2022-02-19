# 01010111 00101110 01010101 00101110 01000011 00101110
from moduls import *


@login_manager.user_loader
def load_user(name):
    return Userlogin(name)


@app.route("/")
def start():
    return redirect(url_for("autpage"))


@app.route("/sing", methods=["GET"])
def autred():
    logout_user()
    session["name"] = None
    return redirect(url_for("autpage"))


@app.route("/auth", methods=["GET"])
def autpage():
    base.DoDIctUsers()
    base.RecordAllName()
    if request.values.get("name") != None:
        name = request.values.get("name")
        password = request.values.get("psw")
        if name in base.usersname:
            if password == base.users[name]["password"]:
                userlog = Userlogin(name)
                login_user(userlog)
                session["name"] = name
                return redirect(url_for("mainpage", username=name))
            else:
                flash('Name or password invalid!')
                return render_template("auth.html")
        else:
            flash('Name or password invalid!')
            return render_template("auth.html")
    else:
        return render_template("auth.html")


@app.route("/user/<name>/postmoney", methods=["GET"])
@login_required
def postmoney(name):
    if session["name"] == name:
        postman = request.values.get("postman")
        value = request.values.get("value")
        valuename = request.values.get("valuename")
        if postman:
            if user.UserCheak(postman) == True:
                if name == session["name"]:
                    flash("You cant send money to you")
                    return render_template("postmoney.html", name=name)
                else:
                    if base.PostMoney(name, postman, valuename, value,) == True:
                        flash("Success")
                        return render_template("postmoney.html", name=name)
                    else:
                        flash("Insufficient funds")
                        return render_template("postmoney.html", name=name)
            else:
                flash("People not found")
                return render_template("postmoney.html", name=name)
        else:
            return render_template("postmoney.html", name=name)
    else:
        return render_template("dontdothis.html")


@app.route("/reg", methods=["GET", "POST"])
def regpage():
    base.DoDIctUsers()
    if request.method == "GET":
        if request.values.get("name") != None:
            name = request.values.get("name")
            password = request.values.get("psw")
            password_true = request.values.get("psw-repeat")
            cheak = user.UserRegister(name, password, password_true)

            if cheak == "Passwords not same":
                flash("Your passwords not same")
                return render_template("register.html")
            elif cheak == "int password":
                flash("Your name must have 1 letter")
                return render_template("register.html")
            elif cheak == "User with your name alredy registed":
                flash(f"User with name: '{name}' alredy registed")
                return render_template("register.html")
            else:
                session["name"] = name
                userlog = Userlogin(name)
                login_user(userlog)
                return redirect(url_for("mainpage", username=name))
        else:
            return render_template("register.html")


@app.route("/user/<username>", methods=["GET"])
@login_required
def mainpage(username):
    if session["name"] == username:
        base.DoDIctUsers()
        if username in base.usersname:
            return render_template('main.html', name=username, USD=base.users[username]["money"]["USD"], UAH=base.users[username]["money"]["UAH"], RUB=base.users[username]["money"]["RUB"])
    else:
        return render_template("dontdothis.html")


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.103")
