from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Temporary user storage (use a database for real apps)
# Structure: users[email] = {'username': username, 'password': hashed_password}
users = {}

@app.route('/')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)

# ---------------- SIGN UP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if email in users:
            return "Email already registered ❌"

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Store user
        users[email] = {'username': username, 'password': hashed_password}

        # Log in automatically
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('signup.html')

# ---------------- SIGN IN ----------------
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and check_password_hash(users[email]['password'], password):
            session['username'] = users[email]['username']
            return redirect(url_for('home'))
        else:
            return "Invalid email or password ❌"

    return render_template('signin.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/latte_page')
def latte_page():
    return render_template('caramel_latte_page.html')

@app.route('/ShopNow')
def ShopNow():
    return render_template('Shop_Now.html')


if __name__ == '__main__':
    app.run(debug=True)
