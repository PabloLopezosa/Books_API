from flask import Flask, jsonify, request
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return {'books': result}

# 1.Ruta para obtener el conteo de libros por autor ordenador de forma descendente

@app.route('/api/v1/resources/books/ordered', methods=['GET'])
def get_ordered():
   connection = sqlite3.connect('books.db')
   cursor = connection.cursor()
   select_books = "SELECT author, count(author) as conteo FROM books GROUP BY 1 ORDER BY 2 DESC"
   result = cursor.execute(select_books).fetchall()
   connection.close()
   return jsonify(result)

# 2.Ruta para obtener los libros de un autor en la llamada

@app.route('/api/v1/resources/books/author', methods=['GET'])
def filter_author ():
   author = request.args['author']
   author = '%' + author + '%'
   connection = sqlite3.connect('books.db')
   cursor = connection.cursor()
   query = '''SELECT * 
            FROM books 
            WHERE author LIKE ?'''
   result = cursor.execute(query, (author,)).fetchall()
   connection.close()
   return jsonify(result)
#http://127.0.0.1:5000/api/v1/resources/books/author?author=Asimov

# 3.Ruta para obtener los libros filtrados por id, publicación y autor

@app.route('/api/v1/resources/books/filtered', methods=['GET'])
def filtered ():
   connection = sqlite3.connect('books.db')
   cursor = connection.cursor()
   query = '''SELECT * 
            FROM books 
            WHERE '''

   to_filter = []

   if 'author' in request.args():
      author = request.args['author']
      author = '%' + author + '%'
      query += ' author LIKE ? AND'
      to_filter.append(author)

   if 'year' in request.args():
      year = request.args['year']
      query += ' published = ? AND'
      to_filter.append(year)

   if 'title' in request.args():
      title = request.args['title']
      title = '%' + title + '%'
      query += ' title LIKE ? AND'
      to_filter.append(title)

   query = query[:-4] + ";"
   result = cursor.execute(query, to_filter).fetchall()
   connection.close()
   return jsonify(result)

app.run()