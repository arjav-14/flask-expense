# from flask import Flask , render_template , redirect , request , session
# from flask_mysqldb import MySQL
# from flask_bcrypt import Bcrypt

# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'
# bcrypt = Bcrypt(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'expense_tracker'
# mysql = MySQL(app)


# @app.route('/')
# def home():
#     return redirect('/login')

# @app.route('/signup' , methods=['GET' , 'POST'])
# def signup():
#     if request.method == 'POST':
#         user = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
#         curr = mysql.connection.cursor()
#         curr.execute("INSERT INTO users (name , email , password) VALUES (%s , %s , %s)" , (user , email , hashed_password))
#         mysql.connection.commit()
#         curr.close()
#         return redirect('/login')
    
#     # Create a simple current_user object for template
#     current_user = {'is_authenticated': False}
#     return render_template('signup.html', current_user=current_user)


# @app.route('/login' , methods=['GET' , 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         curr = mysql.connection.cursor()
#         curr.execute("SELECT * FROM users WHERE email = %s" , (email,))
#         user = curr.fetchone()
#         curr.close()
        
#         if user and bcrypt.check_password_hash(user[3], password):
#             session['user_id'] = user[0]
#             return redirect('/dashboard')
#         else:
#             return redirect('/login')
    
#     # Create a simple current_user object for template
#     current_user = {'is_authenticated': False}
#     return render_template('login.html', current_user=current_user)


# @app.route('/dashboard')
# def dashboard():

#     if 'user_id' not in session:
#         return redirect('/login')

#     cur = mysql.connection.cursor()
#     cur.execute(
#         "SELECT * FROM expenses WHERE user_id=%s",
#         (session['user_id'],)
#     )

#     expenses = cur.fetchall()
    
#     # Get categories
#     cur.execute("SELECT * FROM categories ORDER BY name")
#     categories = cur.fetchall()
    
#     # Get user info for template
#     cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
#     user_data = cur.fetchone()
#     cur.close()
    
#     # Create current_user object with required attributes
#     current_user = {
#         'is_authenticated': True,
#         'name': user_data[1] if user_data else 'User'
#     }

#     return render_template("dashboard.html", expenses=expenses, categories=categories, current_user=current_user)




# @app.route('/add_expense', methods=['POST'])
# def add_expense():

#     if 'user_id' not in session:
#         return redirect('/login')

#     title = request.form['title']
#     amount = request.form['amount']
#     category = request.form['category']
#     date = request.form['date']

#     cur = mysql.connection.cursor()

#     cur.execute(
#         "INSERT INTO expenses(user_id,title,amount,category,date) VALUES(%s,%s,%s,%s,%s)",
#         (session['user_id'], title, amount, category, date)
#     )

#     mysql.connection.commit()

#     return redirect('/dashboard')



# @app.route('/delete/<int:expense_id>')
# def delete_expense(expense_id):
#     if 'user_id' not in session:
#         return redirect('/login')
    
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM expenses WHERE id=%s AND user_id=%s", (expense_id, session['user_id']))
#     mysql.connection.commit()
#     cur.close()
    
#     return redirect('/dashboard')


# @app.route('/edit/<int:id>')
# def edit_expense(id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     curr = mysql.connection.cursor()
#     curr.execute("SELECT * FROM expenses WHERE id=%s AND user_id=%s", (id, session['user_id']))
#     expense = curr.fetchone()
    
#     # Get categories
#     curr.execute("SELECT * FROM categories ORDER BY name")
#     categories = curr.fetchall()
#     curr.close()
    
#     # Create current_user object for template
#     current_user = {'is_authenticated': True}
#     return render_template('edit_expense.html', expense=expense, categories=categories, current_user=current_user)


# @app.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     title = request.form['title']
#     amount = request.form['amount']
#     category = request.form['category']
#     date = request.form['date']

#     cur = mysql.connection.cursor()

#     cur.execute("""
#         UPDATE expenses
#         SET title=%s,
#             amount=%s,
#             category=%s,
#             date=%s
#         WHERE id=%s AND user_id=%s
#     """, (title, amount, category, date, id, session['user_id']))

#     mysql.connection.commit()
#     cur.close()

#     return redirect('/dashboard')







# @app.route('/init_db')
# def init_db():
#     """Initialize database with default categories"""
#     cur = mysql.connection.cursor()
    
#     # Create categories table if not exists
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS categories (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) UNIQUE NOT NULL
#         )
#     """)
    
#     # Insert default categories
#     default_categories = [
#         'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
#         'Bills & Utilities', 'Healthcare', 'Education', 'Travel',
#         'Personal Care', 'Others'
#     ]
    
#     for category in default_categories:
#         cur.execute("INSERT IGNORE INTO categories (name) VALUES (%s)", (category,))
    
#     mysql.connection.commit()
#     cur.close()
    
#     return "Database initialized with default categories!"


# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect('/login')



# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, redirect, request, session, flash, send_file
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

bcrypt = Bcrypt(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'expense_tracker'

mysql = MySQL(app)


# ================= HOME =================
@app.route('/')
def home():
    return redirect('/login')


# ================= SIGNUP =================
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect('/signup')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name, email, hashed_password)
        )

        mysql.connection.commit()
        cur.close()

        flash("Signup successful! Please login.", "success")

        return redirect('/login')

    current_user = {'is_authenticated': False}
    return render_template('signup.html', current_user=current_user)


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[3], password):

            session['user_id'] = user[0]

            flash("Login successful!", "success")

            return redirect('/dashboard')

        flash("Invalid email or password", "danger")

    current_user = {'is_authenticated': False}
    return render_template('login.html', current_user=current_user)


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    search = request.args.get('search')

    if search:
        cur.execute("""
            SELECT * FROM expenses
            WHERE user_id=%s AND title LIKE %s
        """, (session['user_id'], '%' + search + '%'))
    else:
        cur.execute("""
            SELECT * FROM expenses
            WHERE user_id=%s
        """, (session['user_id'],))

    expenses = cur.fetchall()

    # Monthly total
    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id=%s
        AND MONTH(date)=MONTH(CURDATE())
    """, (session['user_id'],))

    monthly_total = cur.fetchone()[0]

    # Category summary
    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """ , (session['user_id'],))

    category_summary = cur.fetchall()

    # Categories dropdown
    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()

    # User info
    cur.execute("SELECT name FROM users WHERE id=%s", (session['user_id'],))
    user_data = cur.fetchone()

    cur.close()

    current_user = {
        'is_authenticated': True,
        'name': user_data[0] if user_data else 'User'
    }

    return render_template(
        "dashboard.html",
        expenses=expenses,
        categories=categories,
        monthly_total=monthly_total,
        category_summary=category_summary,
        current_user=current_user
    )


# ================= ADD EXPENSE =================
@app.route('/add_expense', methods=['POST'])
def add_expense():

    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO expenses(user_id,title,amount,category,date)
        VALUES (%s,%s,%s,%s,%s)
    """, (session['user_id'], title, amount, category, date))

    mysql.connection.commit()
    cur.close()

    flash("Expense added successfully!", "success")

    return redirect('/dashboard')


# ================= DELETE =================
@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        DELETE FROM expenses
        WHERE id=%s AND user_id=%s
    """, (expense_id, session['user_id']))

    mysql.connection.commit()
    cur.close()

    flash("Expense deleted", "warning")

    return redirect('/dashboard')


# ================= EDIT PAGE =================
@app.route('/edit/<int:id>')
def edit_expense(id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE id=%s AND user_id=%s
    """, (id, session['user_id']))

    expense = cur.fetchone()

    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()

    cur.close()

    current_user = {'is_authenticated': True}

    return render_template(
        'edit_expense.html',
        expense=expense,
        categories=categories,
        current_user=current_user
    )


# ================= UPDATE =================
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE expenses
        SET title=%s, amount=%s, category=%s, date=%s
        WHERE id=%s AND user_id=%s
    """, (title, amount, category, date, id, session['user_id']))

    mysql.connection.commit()
    cur.close()

    flash("Expense updated successfully!", "info")

    return redirect('/dashboard')


# ================= DATE FILTER =================
@app.route('/filter', methods=['POST'])
def filter_expenses():

    if 'user_id' not in session:
        return redirect('/login')

    start_date = request.form['start_date']
    end_date = request.form['end_date']

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id=%s
        AND date BETWEEN %s AND %s
    """, (session['user_id'], start_date, end_date))

    expenses = cur.fetchall()

    cur.close()

    return render_template("dashboard.html", expenses=expenses)


# ================= EXPORT CSV =================
@app.route('/export_csv')
def export_csv():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT title, amount, category, date
        FROM expenses
        WHERE user_id=%s
    """, (session['user_id'],))

    data = cur.fetchall()
    cur.close()

    df = pd.DataFrame(data, columns=["Title", "Amount", "Category", "Date"])

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="expenses.csv"
    )


# ================= INIT DEFAULT CATEGORIES =================
@app.route('/init_db')
def init_db():

    cur = mysql.connection.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    default_categories = [
        'Food & Dining', 'Transportation', 'Shopping',
        'Entertainment', 'Bills & Utilities',
        'Healthcare', 'Education', 'Travel',
        'Personal Care', 'Others'
    ]

    for category in default_categories:
        cur.execute(
            "INSERT IGNORE INTO categories(name) VALUES(%s)",
            (category,)
        )

    mysql.connection.commit()
    cur.close()

    return "Categories initialized successfully!"


# ================= LOGOUT =================
@app.route('/logout')
def logout():

    session.pop('user_id', None)

    flash("Logged out successfully", "info")

    return redirect('/login')


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)