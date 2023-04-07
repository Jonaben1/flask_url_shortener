from db_connection import get_db_connection
from hashids import Hashids
from flask import Flask, flash, render_template, request, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your secret key'

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')


@app.route('/stats')
def stats():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT * FROM urls').fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    return render_template('stats.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)

