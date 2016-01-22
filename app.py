import os
import psycopg2
from flask import Flask, render_template
import urlparse
from os.path import exists
from os import makedirs
import logging
from logging.handlers import RotatingFileHandler
from flask import request

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
schema = "schema.sql"
conn = psycopg2.connect(db)

cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return 'Hello World!'

@app.route('/contacts')
def contacts():
    try:
        cur.execute("""SELECT name from salesforce.contact""")
        rows = cur.fetchall()
        response = ''
        my_list = []
        for row in rows:
            my_list.append(row[0])

        return render_template('template.html',  results=my_list)
    except Exception as e:
        print e
        return []

@app.route('/url', methods=['POST','GET'])
def url():
    #return "hi"
    app.logger.info('****')
    app.logger.error('Entered /url')
    errors = []
    results = {'A':'1','B':'2'}
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url-box']
            app.logger.info('url:' + url)
            r = requests.get(url)
            app.logger.info('r.text ' + r.text)
        except:
            app.logger.error('An error occurred')
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again.**"
            )
    return render_template('result.html', errors=errors, results=results)
    
if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()

	
