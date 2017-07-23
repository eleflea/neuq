#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import os
from io import BytesIO
import sqlite3
import base64

path = os.path
DI = path.dirname(__file__)

CREATE_TABLE_ITEMS_SCRIPT = '''
create table if not exists IMG(
ID INTEGER PRIMARY KEY  AUTOINCREMENT,
NAME           TEXT NOT NULL,
IMG0           BLOB NOT NULL,
IMG1           BLOB NOT NULL,
IMG2           BLOB NOT NULL,
IMG3           BLOB NOT NULL,
IMG4           BLOB NOT NULL,
IMG5           BLOB NOT NULL,
DES            TEXT
);
'''


def compress(name):
    # open
    try:
        img = Image.open(name)
    except:
        return BytesIO().getvalue()

    # convert to map
    img_converted = img.convert('P')
    # img_converted.save(path.join(img_dir, 'converted.png'), optimize=True)

    # compress and convert to bytes
    b = BytesIO()
    img_converted.save(b, format='PNG', optimize=True)
    return b.getvalue()


def build(dirname, name):
    conn = sqlite3.connect(
        path.join(DI, 'instance', '{name}.db'.format(name=name)))
    print("Connect {name} successfully.".format(name=name))
    conn.execute("drop table if exists IMG;")
    conn.execute(CREATE_TABLE_ITEMS_SCRIPT)
    print("Table created successfully.")
    cmd = "INSERT INTO IMG (NAME,IMG0,IMG1,IMG2,IMG3,IMG4,IMG5) VALUES (?,?,?,?,?,?,?);"
    cnt = 0
    for fpath, dirs, fs in os.walk(dirname):
        if not cnt % 10:
            print(cnt)
        for f in fs:
            if f[-1] == '0':
                imgs = [compress(path.join(fpath, f[:-1] + str(i))) for i in range(6)]
                conn.execute(cmd, (f[:-2], imgs[0], imgs[1], imgs[2], imgs[3], imgs[4], imgs[5]))
                cnt += 1
    conn.commit()
    conn.close()
    print("Successful.")


if __name__ == '__main__':
    # build(r'H:\questions\TeacherChoice\概率统计_GL', 'img_gl')
    conn = sqlite3.connect(path.join(DI, 'instance', 'img_gs.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select * from img where name="19_Hard_1a2618a1-1cb3-4c56-9f49-f4dbc16ff72d";')
    img_bytes = cur.fetchall()[0][6]
    img_64 = str(base64.b64encode(img_bytes))
    print(img_64)
    # img0 = Image.open(BytesIO(img_bytes))
    # img0.show()
