import os
import sqlite3
from base64 import b64encode

from flask import Flask, g, render_template, request, jsonify, make_response, abort

import config

app = Flask(__name__)
app.config.from_object(config.TestConfig)

def connect_db(name):
    # print(os.path.join(app.instance_path, name))
    conn = sqlite3.connect(os.path.join(app.instance_path, name))
    conn.row_factory = sqlite3.Row
    return conn

def get_db(name):
    if hasattr(g, 'db'):
        g.db.close()
    g.db = connect_db(name)
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def show_chapter():
    datas = []
    for db_data in app.config['DB_LIST']:
        db = get_db(db_data["db"])
        cur = db.execute('select name from chapter where pid=0;')
        data_list = []
        i = 1
        for row in cur.fetchall():
            num = db.execute("select count(*) from question where \
            chapter in (select id from chapter where name like '{0}.%' or \
            name like '第{0}章%');".format(i)).fetchone()[0]
            data_list.append([row[0], num])
            i += 1
        datas.append({"name": db_data["name"], "rep": db_data["rep"], "data": data_list})
    return render_template('index.html', datas=datas)

@app.route('/question')
def query_question():
    db = get_db(request.args.get('db') + '.db')
    name = db.execute("select name from question where chapter in (select id from chapter where name like '{0}.%' or \
            name like '第{0}章%') order by chapter,diff asc;".format(request.args.get('id')))
    page = int(request.args.get('page'))
    if page > 0:
        q_list = [n['name'] for n in name.fetchall()][(page - 1) * 5:page * 5]
    else:
        abort(404)
    db = get_db('img_' + request.args.get('db') + '.db')
    datas = []
    for name in q_list:
        question = db.execute("select * from img where name='{}';".format(name))
        q = question.fetchone()
        chapter, diff, _ = q['name'].split('_')
        imgs = [b64encode(img).decode() for img in q[2:8]]
        db2 = connect_db(request.args.get('db') + '.db')
        ch_name = db2.execute("select name from chapter where id={};".format(chapter)).fetchone()[0]
        datas.append({'chapter': ch_name, 'diff': diff, 'imgs': imgs})
    db2.close()
    return make_response(jsonify(q=datas))

@app.route('/page')
def show_question():
    db = request.args.get('db')
    num = request.args.get('id')
    db2 = get_db(db + '.db')
    title = db2.execute("select name from chapter where pid=0;").fetchall()[int(num) - 1][0]
    datas = {'db': db, 'num': num, 'title': title}
    return render_template('page.html', data=datas)

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)
