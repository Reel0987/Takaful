from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('takaful.db')
    conn.row_factory = sqlite3.Row
    return conn

# الصفحة الرئيسية - عرض الفئات
@app.route('/')
def home():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('index.html', categories=categories)

# عرض الاحتياجات داخل فئة معينة
@app.route('/category/<int:category_id>')
def category_needs(category_id):
    conn = get_db_connection()
    needs = conn.execute('SELECT * FROM needs WHERE category_id = ?', (category_id,)).fetchall()
    conn.close()
    return render_template('needs.html', needs=needs, category_id=category_id)

# عرض تفاصيل الحاجة
@app.route('/need/<int:need_id>')
def need_detail(need_id):
    conn = get_db_connection()
    need = conn.execute('SELECT * FROM needs WHERE id = ?', (need_id,)).fetchone()
    conn.close()
    return render_template('need_detail.html', need=need)

# صفحة التبرع
@app.route('/donate/<int:need_id>', methods=['GET', 'POST'])
def make_donation(need_id):
    if request.method == 'POST':
        amount = request.form['amount']
        payment_method = request.form['payment_method']
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO donations (need_id, amount, payment_method) VALUES (?, ?, ?)',
            (need_id, amount, payment_method)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('donation.html', need_id=need_id)

if __name__ == '__main__':
    app.run(debug=True)