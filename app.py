from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# def c():
#     return SQLAlchemy(app)
db = SQLAlchemy(app)


class Todo(db.Model):
    NO = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    desc = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.NO} - {self.title}"
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    # print(alltodo)
    return render_template("index.html",alltodo=alltodo)
    # return "Hello1 world"
@app.route('/update/<int:NO>',methods=['GET','POST'])
def update(NO):
    if request.method=="POST":
        title = request.form["title"]
        desc = request.form["desc"]
        alltodo = Todo.query.filter_by(NO=NO).first()
        alltodo.title = title
        alltodo.desc = desc
        db.session.add(alltodo)
        db.session.commit()
        return redirect("/")
    alltodo = Todo.query.filter_by(NO=NO).first()
    return render_template("update.html",alltodo=alltodo)
@app.route('/delete/<int:NO>')
def delete(NO):
    alltodo = Todo.query.filter_by(NO=NO).first()
    db.session.delete(alltodo)
    db.session.commit()
    print(alltodo)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

    # with app.app_context():
    #     c()