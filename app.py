from flask import Flask, flash, redirect,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,validators
from werkzeug.utils import secure_filename
import os


app = Flask(__name__,static_folder='static')
app.config['SECRET_KEY'] = '5677474HEHBDBDBDERYRY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)



class SongDetails(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	song_url = db.Column(db.String(100),unique=True,nullable=False,default='')
	title = db.Column(db.String(100),unique=True,nullable=False)
	artist = db.Column(db.String(100),nullable=False)
	album = db.Column(db.String(100),nullable=False)

	def __repr__(self):
		return f"song('{self.id}','{self.song_url}', '{self.title}','{self.artist}','{self.album}')" 

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
	songs = SongDetails.query.all()
	return render_template('songs.html',songs=songs)


@app.route("/addsong",methods=['GET','POST'])
def add_song():
	form = AddSongForm((request.form))
	if form.validate_on_submit():
		path = os.getcwd()
		song_obj = request.files['song']
		if song_obj:
			filename = secure_filename(song_obj.filename)
			file_ext = filename.split('.')[-1]
			if file_ext != 'mp3':
				flash('Please Upload only mp3 files','danger')
			else:
				song_obj.save(f'{path}/static/' + filename)
				song_url = f'{path}/static/' + filename
				sd = SongDetails(song_url=song_url,title=form.title.data,artist=form.artist.data,album=form.album.data)
				db.session.add(sd)
				db.session.commit()
				flash('Song Sucessfully Added!','success')
				return redirect(url_for('song'))
	return render_template('addsongs.html',title='AddSongs',form=form)


@app.route('/delete_song/<int:id>',methods=['GET'])
def delete_song(id):
	song = SongDetails.query.get(id)
	db.session.delete(song)
	db.session.commit()
	flash("Song successfully deleted",'success')
	return redirect(url_for('song'))

@app.route('/play_song/<int:id>')
def play_song(id):
	song = SongDetails.query.get(id)
	name = song.song_url.split('/')[-1]
	return render_template('play_song.html',title='PlaySong',song_name=name)



if __name__=='__main__':
	
	app.run(debug=True)
