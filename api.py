import os
from flask import Flask
from flask import render_template
from flask import request
from flask_migrate import Migrate
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    roles = db.Column(db.ARRAY(db.Integer), server_default="{}")

    def __repr__(self):
        return "<Id: {0}>\n<Name: {1}>".format(self.id, self.name)

class Role(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return "<Id: {0}>\n<Name: {1}>".format(self.id, self.name)

@app.route("/", methods=["GET","POST"])
def home():
    users = User.query.order_by(User.id)
    roles = Role.query.order_by(Role.id)

    result = {}

    for role in list(roles):
        result[role.id] = role.name

    return render_template("home.html", users=users, roles=result)

@app.route("/user/add", methods=["POST"])
def addUser():
    user = User(name=request.form.get('user'))
    db.session.add(user)
    db.session.commit()
    return redirect('/')
    

@app.route("/user/roles/add", methods=["POST"])
def update():
    id = request.form.get("id")
    newRole = request.form.get("newRole")
    user = User.query.filter_by(id=id).first()
    roles = user.roles
    roles.append(int(newRole))
    User.query.filter_by(id=id).update({'roles':roles})
    db.session.commit()
    return redirect("/")

@app.route("/user/roles/delete", methods=["POST"])
def deleteRoleFromUser():
    id = request.form.get("id")
    deletingRole = request.form.get("role")    
    user = User.query.filter_by(id=id).first()
    roles = user.roles
    roles.remove(int(deletingRole))
    User.query.filter_by(id=id).update({'roles':roles})
    db.session.commit()

    return redirect("/")

@app.route("/roles/add", methods=["POST"])
def addRole():
    id = request.form.get("id")
    newRole = request.form.get("role")
    role = Role(name=newRole)
    db.session.add(role)
    db.session.commit()
    return redirect("/")

@app.route("/roles/delete", methods=["POST"])
def deleteRole():
    id = request.form.get("id")
    role = Role.query.filter_by(id=id).first()

    users = User.query.all()

    for user in users:
        roles = user.roles
        if (int(id) in roles):
            roles.remove(int(id))
            User.query.filter_by(id=id).update({'roles':roles}) # kostyl as fuck :(

    db.session.delete(role)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
