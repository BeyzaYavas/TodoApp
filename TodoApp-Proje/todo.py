from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/LEGION/Desktop/TodoApp-Proje/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    complete=db.Column(db.Boolean) #todo tamamlanmışsa true tamamlanmamışsa false döndürebileceğiz

@app.route("/")
def index():
    todoGet=Todo.query.all() #tablodaki özelliklerimiz sözlük yapısıyla liste şeklinde gelecek
    return render_template("index.html",todoGet=todoGet)

@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit() #değişiklik yapıldığı için commit yapıyoruz
    return redirect(url_for("index"))

@app.route("/update/<string:id>")
def update(id):
    todo=Todo.query.filter_by(id=id).first()
    """if todo.complete == False:
        todo.complete=True
    else:
        todo.complete=False"""
    todo.complete = not todo.complete

    #db de bir değişiklik yaptığımız için commit gerek
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__=="__main__":
    db.create_all() #oluşan tablolar tekrar oluşmayacak.
    app.run(debug=True)

