from flask import Flask, render_template, request, redirect
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Fetch user from database
    response = supabase.table('users').select('*').eq('username', username).execute()
    user = response.data
    
    if user:
        if user[0]['password'] == password:
            return redirect('/welcome')
        else:
            return render_template('index.html', login_error='Incorrect password')
    else:
        return render_template('index.html', login_error='Username does not exist')




@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    # Check if username already exists
    existing_user_response = supabase.table('users').select('*').eq('username', username).execute()
    existing_user_data = existing_user_response.data
    
    if existing_user_data:
        return render_template('index.html', signup_error='Username already exists')
    
    # Create new user
    new_user_response = supabase.table('users').insert({'username': username, 'password': password}).execute()
    new_user_data = new_user_response.data
    if not new_user_data:
        return render_template('index.html', signup_error='Error creating user')
    else:
        return redirect('/welcome')





@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)
