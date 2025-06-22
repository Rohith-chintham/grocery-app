from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS groceries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM groceries')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    unit = request.form['unit']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO groceries (name, quantity, unit) VALUES (?, ?, ?)', (name, quantity, unit))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM groceries WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE groceries SET quantity = ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
