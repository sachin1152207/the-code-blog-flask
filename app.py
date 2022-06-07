import os
import time
import json
import sqlite3
from math import ceil
from hashlib import md5
from datetime import datetime
from flask_session import Session
from flask_recaptcha import ReCaptcha
from werkzeug.utils import secure_filename
from package import fixDate, b64Encode, b64Decode
from flask import Flask, redirect, request, render_template, url_for, session


database = sqlite3.connect('the-coding-blog.db', check_same_thread=False)
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Contact(
    "sno"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"number"	TEXT,
	"message"	TEXT,
    "date" TEXT,
	PRIMARY KEY("sno" AUTOINCREMENT)
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS About(
    "name"	TEXT,
	"skill"	TEXT,
	"description"	TEXT,
    "image"	TEXT,
	"socialLinks"	TEXT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Post(
    "sno"	INTEGER,
	"slug"	TEXT,
    "title"	TEXT,
	"tag-line"	TEXT,
	"categories"	TEXT,
	"content"	TEXT,
	"picture"	TEXT,
    "date"	TEXT,
	PRIMARY KEY("sno" AUTOINCREMENT)
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Config(
    "sno"	INTEGER,
	"numberOfPost"	INTEGER,
    "fb_url"	TEXT,
	"git_url"	TEXT,
	"yt_url"	TEXT,
	"securityEmail"	TEXT,
    "admin_email"	TEXT,
    "admin_password"	TEXT,
	PRIMARY KEY("sno" AUTOINCREMENT)
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Gallery(
	"sno"	INTEGER,
	"captions"	TEXT,
	"pictures"	TEXT,
    "date"	TEXT,
	PRIMARY KEY("sno" AUTOINCREMENT)
)""")
database.commit()

allow_exetension = ['jpg', 'png', 'jpeg']

def verifySession():
    try:
        email = session['email']
        token = session['token']
    except:
        return False
    if email == dbConfig.showConfig()[6] and token == md5(f"{dbConfig.showConfig()[6]} {dbConfig.showConfig()[7]}".encode()).hexdigest():
        return True
    else:
        return False
def clearSession():
    session['email'] = None
    session['token'] = None
def killSession():
    session.pop('email')
    session.pop('token')


class dbAbout():
    def showAbout():
        return cursor.execute("SELECT * FROM About").fetchall()[0]
    def updateAbout(name, skill, description):
        cursor.execute(f"INSERT INTO About(name, skill, description) VALUES ('{name}', '{skill}','{description}')")
        database.commit()   
class dbPost():
    def showContent(slug):
        try:
            return (cursor.execute(f"SELECT * FROM Post WHERE slug='{slug}'").fetchall())
        except:
            return False
    def showPost():
        return (cursor.execute("SELECT * FROM Post").fetchall()[::-1])
    def showAll():
        return cursor.execute("SELECT * FROM Post").fetchall()
    def editPost(postSno, postTitle, postTagline, postCato, postContent, postImg):
        if (postImg !=""):
            cursor.execute(f""" UPDATE Post SET 'title'='{postTitle}', 'tag-line'='{postTagline}', categories='{postCato}', content='{b64Encode(postContent)}', 'picture'='{postImg}' WHERE sno='{postSno}'""")
            database.commit()
        cursor.execute(f""" UPDATE Post SET 'title'='{postTitle}', 'tag-line'='{postTagline}', categories='{postCato}', content='{b64Encode(postContent)}' WHERE sno='{postSno}'""")
        database.commit()
    def deletePost(postSno):
        rmImgName = cursor.execute(f"SELECT picture FROM 'Post' WHERE sno='{postSno}'").fetchall()[0][0]
        os.remove(f'static/img/blogs/{rmImgName}')
        cursor.execute(f"DELETE FROM Post WHERE sno='{postSno}'")
        database.commit()
    def addPost(postTitle, postTagline, postCato, postContent, imgName):
        date = fixDate(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(f"INSERT INTO Post(slug, title, 'tag-line', categories, content, picture, date) VALUES ('{md5(postTitle.encode()).hexdigest()[:15]}','{postTitle}', '{postTagline}', '{postCato}', '{b64Encode(postContent)}', '{imgName}', '{date}')")
        database.commit()
class dbContact():
    def dbContact(name, email, number, message):
        date = fixDate(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True)
        cursor.execute(f"INSERT INTO Contact(name, email, number, date, message) VALUES ('{name}', '{email}','{number}', '{date}', '{b64Encode(message)}')"
        )
        database.commit()
    def showAll():
        return (cursor.execute("SELECT * FROM Contact").fetchall()[::-1])
class dbConfig():
    def showConfig():
        return (cursor.execute("SELECT * FROM Config").fetchall()[0])
    def updateConfig(noPosts, fb_url, git_url, yt_url, securityEmail):
        cursor.execute(f"UPDATE Config SET 'numberOfPost'='{noPosts}', 'fb_url'='{fb_url}','git_url'='{git_url}', 'yt_url'='{yt_url}', 'securityEmail'='{securityEmail}' WHERE sno='1'")
        database.commit()
    def updateCredentials(email, password):
        cursor.execute(f"UPDATE Config SET 'admin_email'='{email}', 'admin_password'='{password}' WHERE sno='1' ")
        database.commit()
class dbGallery():
    def showGallery():
        return (cursor.execute("SELECT * FROM Gallery").fetchall()[::-1])
    def addGallery(captions, pictureName):
        date = fixDate(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(f"INSERT INTO Gallery(captions, pictures, date) VALUES ('{captions}', '{pictureName}', '{date}')")
        database.commit()
    def deletePhoto(photoSno):
        rmImgName = cursor.execute(f"SELECT pictures FROM 'Gallery' WHERE sno='{photoSno}'").fetchall()[0][0]
        os.remove(f'static/img/gallery/{rmImgName}')
        cursor.execute(f"DELETE FROM Gallery WHERE sno='{photoSno}'")
        database.commit()
app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = "6LdxkC4gAAAAADI2ZSnv8wciVajfsFXyXxSK1dk3"
app.config['RECAPTCHA_SECRET_KEY'] = "6LdxkC4gAAAAAFJ7D3UhYyuQeseYdUsnILFDjtxX"
app.config['UPLOAD_FOLDER'] = "static/img/blogs"
app.config['SESSION_PARMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
recaptcha = ReCaptcha(app)
Session(app)


@app.route('/')
def index():
    blogPost = dbPost.showPost()
    last = ceil(len(blogPost)/int(dbConfig.showConfig()[1]))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    blogPost = blogPost[(page - 1)* int(dbConfig.showConfig()[1]): (page - 1) * int(dbConfig.showConfig()[1]) + int(dbConfig.showConfig()[1])]
    if page == 1:
        prev = "#"
        next = "/?page="+str(page+1)
    elif page == last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+str(page+1)
    return render_template('index.html', posts = blogPost, prev = prev, next = next, b64Decode = b64Decode)

@app.route('/posts/<string:post_slug>')
def posts(post_slug):
    blogContent = dbPost.showContent(post_slug)
    if (blogContent == False):
        return render_template('noPost.html')
    elif (len(blogContent) == 0):
         return render_template('noPost.html')
    return render_template('post.html', content=blogContent[0], b64Decode = b64Decode)

@app.route('/gallery')
def gallery():
    gallery = dbGallery.showGallery()
    last = ceil(len(gallery)/int(dbConfig.showConfig()[1]))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    gallery = gallery[(page - 1)* int(dbConfig.showConfig()[1]): (page - 1) * int(dbConfig.showConfig()[1]) + int(dbConfig.showConfig()[1])]


    if page == 1:
        prev = "#"
        next = "/gallery?page="+str(page+1)
    elif page == last:
        prev = "/gallery?page="+ str(page-1)
        next = "#"
    else:
        prev = "/gallery?page="+ str(page-1)
        next = "/gallery?page="+str(page+1)
    return render_template('gallery.html', gallery = gallery, prev=prev, next=next)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    status = ""
    if request.method == "POST":
        if recaptcha.verify():
            status = True
            name = request.form.get('fullname')
            email = request.form.get('email')
            number = request.form.get('number')
            message = request.form.get('message')
            dbContact.dbContact(name, email, number, message)
        else:
            status = False
    return render_template('contact.html', status=status)

@app.route('/about')
def about():
    return render_template('about.html', about=dbAbout.showAbout(), setting = dbConfig.showConfig())

# Session used funtion here

@app.route('/login', methods = ['GET', 'POST'])
def login():
    status = ""
    if verifySession():
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            if recaptcha.verify():
                email = request.form.get('email')
                password = request.form.get('password')
                if email == dbConfig.showConfig()[6] and password == dbConfig.showConfig()[7]:
                    session['email'] = dbConfig.showConfig()[6]
                    session['token'] = md5(f"{dbConfig.showConfig()[6]} {dbConfig.showConfig()[7]}".encode()).hexdigest()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login.html', status = "wrong")
            else:
                return render_template('login.html', status = False)
        if request.method == 'GET':
            return render_template('login.html', status = status)
       

@app.route('/dashboard')
def dashboard():
    if verifySession():
        blogPost = dbPost.showPost()
        last = ceil(len(blogPost)/int(dbConfig.showConfig()[1]))
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        blogPost = blogPost[(page - 1)* int(dbConfig.showConfig()[1]): (page - 1) * int(dbConfig.showConfig()[1]) + int(dbConfig.showConfig()[1])]
        if page == 1:
            prev = "#"
            next = "/dashboard?page="+str(page+1)
        elif page == last:
            prev = "/dashboard?page="+ str(page-1)
            next = "#"
        else:
            prev = "/dashboard?page="+ str(page-1)
            next = "/dashboard?page="+str(page+1)
        return render_template('dashboard.html', blog = blogPost, prev = prev, next = next, b64Decode = b64Decode, b64Encode = b64Encode)
    else:
        clearSession()
        return redirect(url_for('login'))

@app.route('/dashboard/contact')
def contactShow():
    if verifySession():
        Contactlist = dbContact.showAll()
        return render_template('contactShow.html', contacts = Contactlist)
    else:
        clearSession()
        return redirect(url_for('index'))

@app.route('/dashboard/edit/<string:postSno>', methods=['POST'])
def editPost(postSno):
    if verifySession():
        postImg = request.files['choosePicCreate']
        if (postImg.filename !=""):
            if (postImg.filename.split(".")[len(postImg.filename.split(".")) - 1] in allow_exetension):
                postTitle = request.form.get("postTitle")
                postTagline = request.form.get("postTagline")
                postCato = request.form.get("postCato")
                postContent = request.form.get("postContent")
                imgName = secure_filename(md5((postImg.filename + str(time.time())).encode()).hexdigest() + '.' + postImg.filename.split(".")[len(postImg.filename.split(".")) - 1])
                postImg.save('static/img/blogs/' + imgName)
                dbPost.editPost(postSno, postTitle, postTagline, postCato, postContent, imgName)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        postTitle = request.form.get("postTitle")
        postTagline = request.form.get("postTagline")
        postCato = request.form.get("postCato")
        postContent = request.form.get("postContent")
        dbPost.editPost(postSno, postTitle, postTagline, postCato, postContent, postImg="")
        return redirect(url_for('dashboard'))
    else:
        clearSession()
        return redirect(url_for('index'))

@app.route('/dashboard/delete/<string:postSno>')
def delete(postSno):
    if verifySession():
        dbPost.deletePost(postSno)
        return redirect(url_for('dashboard'))
    else:
        clearSession()
        return redirect(url_for('index'))

@app.route('/dashboard/addpost', methods=['POST'])
def addPost():
    if verifySession():
            postImg = request.files['choosePicCreate']
            if (postImg.filename.split(".")[len(postImg.filename.split(".")) - 1] in allow_exetension):
                postTitle = request.form.get("postTitle")
                postTagline = request.form.get("postTagline")
                postCato = request.form.get("postCato")
                postContent = request.form.get("postContent")
                imgName = secure_filename(md5((postImg.filename + str(time.time())).encode()).hexdigest() + '.' + postImg.filename.split(".")[len(postImg.filename.split(".")) - 1])
                postImg.save('static/img/blogs/' + imgName)
                dbPost.addPost(postTitle, postTagline, postCato, postContent, imgName)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
    else:
        clearSession()
        return redirect(url_for('index'))

@app.route('/dashboard/gallery', methods=['GET', 'POST'])
def galleryAddPhoto():
    if verifySession():
        if request.method == 'POST':
            galleryPic = request.files['galleryPic']
            photoCaptions = request.form.get('photoCaptions')
            if (galleryPic.filename.split(".")[len(galleryPic.filename.split(".")) - 1] in allow_exetension):
                imgName = secure_filename(md5((galleryPic.filename + str(time.time())).encode()).hexdigest() + '.' + galleryPic.filename.split(".")[len(galleryPic.filename.split(".")) - 1])
                galleryPic.save('static/img/gallery/' + imgName)
                dbGallery.addGallery(photoCaptions, imgName)
                return redirect(url_for('galleryAddPhoto'))
        gallery = dbGallery.showGallery()
        last = ceil(len(gallery)/int(dbConfig.showConfig()[1]))
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        gallery = gallery[(page - 1)* int(dbConfig.showConfig()[1]): (page - 1) * int(dbConfig.showConfig()[1]) + int(dbConfig.showConfig()[1])]
        if page == 1:
            prev = "#"
            next = "/dashboard/gallery?page="+str(page+1)
        elif page == last:
            prev = "/dashboard/gallery?page="+ str(page-1)
            next = "#"
        else:
            prev = "/dashboard/gallery?page="+ str(page-1)
            next = "/dashboard/gallery?page="+str(page+1)
        return render_template('galleryShow.html', gallery = gallery, prev = prev, next = next)
    else:
        clearSession()
        return redirect(url_for('index'))

@app.route('/dashboard/setting/gallery/delete/<string:photoSno>')
def deleteGalleryPhoto(photoSno):
    if verifySession():
        dbGallery.deletePhoto(photoSno)
        return redirect(url_for('galleryAddPhoto'))

    else:
        clearSession()
        return redirect(url_for('index'))


@app.route('/dashboard/setting',methods=['GET', 'POST'])
def setting():
    if verifySession():
        if request.method == "POST":
            noPosts = request.form.get('noPosts')
            fb_url = request.form.get('fb_url')
            git_url = request.form.get('git_url')
            yt_url = request.form.get('yt_url')
            securityEmail = request.form.get('securityEmail')
            dbConfig.updateConfig(noPosts, fb_url, git_url, yt_url, securityEmail)
            return redirect(url_for('setting'))
        if request.method == "GET":
            return render_template('setting.html', setting = dbConfig.showConfig(), totalPost = len(dbPost.showAll()))
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/setting/account',methods=['GET', 'POST'])
def settingAccount():
    if verifySession():
        if request.method =="POST":
            email = request.form.get('email')
            password = request.form.get('password')
            dbConfig.updateCredentials(email, password)
            return redirect(url_for('setting'))
        return render_template('settingAccount.html', setting = dbConfig.showConfig())
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    killSession()
    return redirect(url_for('login'))

