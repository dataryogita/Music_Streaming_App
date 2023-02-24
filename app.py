from flask import Flask, flash, redirect,render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired, FileAllowed
from wtforms import StringField,SubmitField,validators

app = Flask(__name__)
app.config['SECRET_KEY'] = '5677474HEHBDBDBDERYRY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class SongDetails(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	song_url = db.Column(db.String(100),unique=True,nullable=False,default='h')
	title = db.Column(db.String(100),unique=True,nullable=False)
	artist = db.Column(db.String(100),unique=True,nullable=False)
	album = db.Column(db.String(100),unique=True,nullable=False)

	def __repr__(self):
		return f"id{self.id} {self.title}" 

class AddSongForm(FlaskForm):
	song=FileField('Song',validators=[FileAllowed(['.mp3'],'MP3 only!')])
	title=StringField('Title',[validators.Length(min=1,max=50),validators.DataRequired()])
	artist=StringField('Artist',[validators.length(min=1,max=50)])
	album=StringField('Album',[validators.length(min=1,max=50)])
	submit=SubmitField('Add Song')



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/song")
def song():
    return render_template('songs.html')

@app.route("/addsong",methods=['GET','POST'])
def add_song():
	form = AddSongForm()
	if form.validate_on_submit(): 
		sd = SongDetails(title=form.title.data,artist=form.artist.data,album=form.album.data)
		db.session.add(sd)
		db.session.commit()
		flash('Song Sucessfully Added!','success')
		return redirect(url_for('song'))
	return render_template('addsongs.html',title='AddSongs',form=form)



if __name__=='__main__':
	
	app.run(debug=True)
