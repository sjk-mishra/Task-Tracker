from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Class to define the Todo table 
class Todo(db.Model):
    __tablename__ = 'todos'

    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    todo= db.Column(db.String(100), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.task}-{self.todo}"
    
with app.app_context():
    db.create_all()
    
@app.route("/", methods=['POST','GET']) 
def todo_submit():
    if request.method == "POST":
        todo= Todo(task= request.form["title"], todo= request.form["desc"])
        db.session.add(todo)
        db.session.commit()
    allTodo= Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.task = title
        todo.todo = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ("/")

if __name__ == '__main__':
    app.run(debug=True) 