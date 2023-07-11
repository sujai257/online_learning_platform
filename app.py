from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'  # Replace with your MongoDB connection string
mongo = PyMongo(app)
@app.route('/')

def index():
    return render_template('index.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        # mongo.db.users.insert_one({'name': name, 'email': email, 'password': password})
        if mongo.db.users.find_one({'email': email}) is None:
            mongo.db.users.insert_one({'name': name, 'email': email, 'password': password})
            return redirect('signin')
        else:
            return 'user is already register'
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        password = request.form['pass']
        email = request.form['email']
        user = mongo.db.users.find_one({'email': email})
        if user and user['password'] == password:
            return redirect('home')
        else:
            return "Invalid email or password"  
    return render_template('signin.html')
@app.route('/home')
def home():
    return render_template("homepage.html")
@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    email = request.form['email']  
    mongo.db.users.insert_one({'name': name, 'email': email})  
    return redirect('/')

@app.route('/update/<user_id>', methods=['POST'])
def update(user_id):
    name = request.form['name']
    email = request.form['email']
    mongo.db.users.update_one({'_id': user_id}, {'$set': {'name': name, 'email': email}})
    return redirect('/')

@app.route('/delete/<user_id>')
def delete(user_id):
    mongo.db.users.delete_one({'_id': user_id})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
