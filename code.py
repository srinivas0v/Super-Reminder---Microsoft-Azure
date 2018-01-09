import csv

from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import base64
import time
from mysql.connector import errorcode
from os import listdir
from os.path import isfile, join

cnx = mysql.connector.connect(user="#########", password='#############',
                                  host="##################", port=3306, database='#######')


app = Flask(__name__)

upath = '##############'

dpath = '################'

spath = '#################'

cpath = '########################'

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
      if request.form['submit'] == 'list':
          print 'list'
          return redirect('/list/')
      elif request.form['submit'] == 'upload':
            Uploadimg()
            Uploadcsv()
      elif request.form['submit'] == 'download':
          stime = time.time()
          f = Download()
          etime = str(time.time()-stime)
          fi = f+'$$$$'+etime
          return redirect('/view/' + fi)
      elif request.form['submit'] == 'query8':
          stime = time.time()
          n1 = request.form['num1']
          n2 = request.form['num2']
          file = Download8(n1,n2)
          etime = str(time.time()-stime)
          fi = file+'$$$$'+etime
          return redirect('/view/' + fi)
      elif request.form['submit'] == 'query9':
          stime = time.time()
          ing = request.form['ing']
          file = Download9(ing)
          etime = str(time.time()-stime)
          fi = file+'$$$$'+etime
          return redirect('/view/' + fi)
      elif request.form['submit'] == 'count':
          return redirect('/count/')

      elif request.form['submit'] == 'lowcal':
            stime = time.time()
            cal = request.form['cal']
            file = lowcal(cal)
            etime = str(time.time() - stime)
            fi = file + '$$$$' + etime
            return redirect('/view/' + fi)


    return render_template('index.html')

@app.route('/list/',methods=['POST','GET'])
def count():
    print 'in func'
    cur = cnx.cursor()
    query = ('SELECT COUNT(*) FROM mydb.fimg;')
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    print data
    return render_template('result.html', count=data[0][0])


def Uploadimg():
    local_file_list = [f for f in listdir(upath) if isfile(join(upath, f))]
    file_num = len(local_file_list)
    for i in range(file_num):
        #local_file = join(upath, local_file_list[i])
            fname = local_file_list[i]
            name, ext = fname.split('.')
            with open(upath + fname, 'rb') as f:
                photo = base64.b64encode(f.read())

                data_query = {
                    'fname': name,
                    'img': photo,
                    'category': 'NULL'}
                #photo = f.read()
                #print photo
                #print fname
                cur1 = cnx.cursor()
                query = ('INSERT INTO mydb.fimg(fname,img,category) VALUES (%(fname)s,%(img)s,%(category)s);')
                cur1.execute(query,data_query)
                print 'done'
                f.close()
                cnx.commit()
            cur1.close()
    return 'successfully uploaded'


def Download():
    fname = []
    cur2 = cnx.cursor()
    query2 = ('select * from mydb.fimg;')
    #select img from mydb.fimg where fname = "VegetableSushi"
    cur2.execute(query2)
    data = cur2.fetchall()
    if len(data) > 0:
        for row in data:
            filename =  row[0]
            filename = filename +'.jpg'
            fname.append(filename)
            print fname
            data1 = base64.b64decode(row[1]+ "========")
            fl = open(dpath+filename, "wb")
            fl.write(data1)
            fl.close()
            f2 = open(spath+filename,"wb")
            f2.write(data1)
            f2.close()
        fn = '$$'.join(fname)
        print fn
    cur2.close()
    return fn


def Download8(n1,n2):
    fname = []
    cur8 = cnx.cursor()
    query8 = ('select distinct(fname) from mydb.fcsv where calories between %s and %s;')
    #select img from mydb.fimg where fname = "VegetableSushi"
    cur8.execute(query8,(n1,n2))
    data = cur8.fetchall()
    if len(data) > 0:
        for row in data:
            filename =  row[0]
            filename = filename +'.jpg'
            fname.append(filename)
            print fname
        fn = '$$'.join(fname)
        print fn
    cur8.close()
    return fn


def lowcal(cal):
    fname = []
    print cal
    cur9 = cnx.cursor()
    query9 = ('select fname,sum(calories) from mydb.fcsv group by fname having sum(calories)<'+cal+' order by sum(calories);')
    #select img from mydb.fimg where fname = "VegetableSushi"
    cur9.execute(query9)
    data = cur9.fetchall()
    if len(data) > 0:
        for row in data:
            filename =  row[0]
            filename = filename +'.jpg'
            fname.append(filename)
            print fname
        fn = '$$'.join(fname)
        print fn
    cur9.close()
    return fn

def Download9(ing):
    fname = []
    cur9 = cnx.cursor()
    query9 = ('select distinct(fname) from mydb.fcsv where ingredients = %(ingredients)s;')
    data_query = {
        'ingredients': ing}
    #select img from mydb.fimg where fname = "VegetableSushi"
    cur9.execute(query9,data_query)
    data = cur9.fetchall()
    if len(data) > 0:
        for row in data:
            filename =  row[0]
            filename = filename +'.jpg'
            fname.append(filename)
            print fname
        fn = '$$'.join(fname)
        print fn
    cur9.close()
    return fn

@app.route('/count/',methods=['POST','GET'])
def count9():
    cur9 = cnx.cursor()
    query9 = ('select ingredients,count(*) from mydb.fcsv group by ingredients order by count(*) desc limit 5;')
    #select img from mydb.fimg where fname = "VegetableSushi"
    cur9.execute(query9)
    data = cur9.fetchall()
    return render_template('count.html', flist=data)



def Uploadcsv():
    local_file_list = [f for f in listdir(cpath) if isfile(join(cpath, f))]
    file_num = len(local_file_list)
    for i in range(file_num):
        #local_file = join(upath, local_file_list[i])
            fname = local_file_list[i]

            with open(cpath + fname, 'rb') as f:

                #with open(upath + fname, "rb") as f:
                    print fname
                    name,ext = fname.split('.')
                    reader = csv.reader(f, delimiter="\t")
                    for i, line in enumerate(reader):
                        print 'line[{}] = {}'.format(i, line)
                        if i == 0:
                            list0 = line[0].split(',')
                        elif i == 1:
                            list1 = line[0].split(',')
                        else:
                            list2 = line[0].split(',')
                    for i in range(len(list1)):
                        cur1 = cnx.cursor()
                        query = ('INSERT INTO `mydb`.`fcsv` (`fname`, `calories`, `ingredients`, `catagory`)  '
                                  'VALUES (%(fname)s,%(calories)s,%(ingredients)s,%(catagory)s);')
                        data_query = {
                                'fname': name,
                                'calories': list0[i],
                                'ingredients': list1[i],
                                'catagory': list2[i]}
                        cur1.execute(query, data_query)
                        cnx.commit()
                    cur1.close()
    return 'success'



@app.route('/view/<fname>', methods=['POST', 'GET'])
def view(fname):
    print fname
    f,time = fname.split('$$$$')
    files = f.split('$$')
    return render_template('view.html', flist=files, time = time)


@app.route('/details/<fname>', methods=['POST', 'GET'])
def Details(fname):
    stime = time.time()
    name,ext = fname.split('.')
    print name
    cur3 = cnx.cursor()
    query3 = ('select * from mydb.fcsv where fname = %(fname)s;')
    data_query = {
        'fname': name}
    print query3
    #select img from mydb.fimg where fname = "VegetableSushi"
    print cur3.execute(query3,data_query)
    data = cur3.fetchall()
    print data
    etime = str(time.time()-stime)
    return render_template('details.html', fname = fname, detail = data,time= etime)



if __name__ == '__main__':
    app.run(debug='true', port= 8000 )
