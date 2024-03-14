from flask import Flask, render_template, request, redirect
from supabase import create_client

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = 'https://dkjkjakmxugzporrkhyl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRramtqYWtteHVnenBvcnJraHlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAwNTE0NTAsImV4cCI6MjAyNTYyNzQ1MH0.M_1JS1IGIduoQCheZJB8HwXML1he7ff954bNIAfKJFQ'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')


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
