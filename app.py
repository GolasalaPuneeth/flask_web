from flask import*
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import *
from datetime import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///work.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class work(db.Model):
  Sno = db.Column(db.Integer, primary_key=True)
  Title = db.Column(db.String(200), nullable=False)
  Description = db.Column(db.String(500), nullable=False)
  Date_created = db.Column(db.DateTime,default=datetime.utcnow)

  def __repr__(self) -> str:
    return f"{self.Sno} - {self.Title}"

@app.route('/',methods=['GET', 'POST'])
def welcome():
  if request.method=='POST':
    Title=request.form['title']
    Description=request.form['desc']
    todo = work(Title=Title, Description=Description)
    db.session.add(todo)
    db.session.commit()
  Allwork = work.query.all()
  return render_template("index.html", allwork = Allwork)

@app.route('/update/<int:Sno>',methods=['GET', 'POST'])
def update(Sno):
  if request.method=='POST':
    Title=request.form['title']
    Description=request.form['desc']
    Allwork=work.query.filter_by(Sno=Sno).first()
    Allwork.Title=Title
    Allwork.Description=Description
    db.session.add(Allwork)
    db.session.commit()
    return redirect('/')
  Allwork=work.query.filter_by(Sno=Sno).first()
  return render_template("update.html", Allwork = Allwork)

@app.route('/delete/<int:Sno>')
def delete(Sno):
  Allwork = work.query.filter_by(Sno=Sno).first()
  db.session.delete(Allwork)
  db.session.commit()
  return redirect('/')

if __name__ == '__main__':
  app.run(debug= True,port=8000)