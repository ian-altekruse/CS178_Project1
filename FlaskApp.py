from flask import Flask, render_template, request, redirect, url_for, flash, session 
from mysql_rds import *
from dynamoDB import * 

app = Flask(__name__)
app.secret_key = creds.secret_key


#------------------------------------------------------------------------
#Used ChatGPT to help with 'session' code and the RDS and DynamoDB connection
#------------------------------------------------------------------------

# - To Do

# - Error Handling for duplicate usernames
# - Error Handling for movies not in movies DB
# - List of removable movies instead of typing
# - Error Handling for view function when no movies in DB

#-------------------------------------------
# Flask Home Page (Defaults to login page)
#-------------------------------------------
@app.route('/')
def home():
    if 'username' not in session:
        return render_template('prelogin_home.html')
    return render_template('homepage.html')

#-------------------------------------------
# Flask Login Page
#-------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        
        response = table.get_item(Key={'Username': Username})
        user = response.get('Item')

        if user and user['Password'] == Password:
            session['username'] = Username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            return render_template('enter_credentials.html')
    
    return render_template('enter_credentials.html')

#-------------------------------------------
# Flask Sign-Up Page
#-------------------------------------------
@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':

        Username = request.form['Username']
        Password = request.form['Password']

        create_new_user(Username, Password)
        
        return render_template('prelogin_home.html')
                        
    else:
        return render_template('create_user.html')

#-------------------------------------------
# Add movie to user account
#-------------------------------------------
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    Username = session.get('username')
    if request.method == 'POST':
        if not Username:
            flash('You must be logged in to view your movies.', 'danger')
            return render_template('prelogin_home.html')

        Title = request.form['Title']        
        add_movie_db(Title, Username)
        
        return render_template('homepage.html')
    else:
        return render_template('add_movie.html')

#-------------------------------------------
# View movies in user account
#-------------------------------------------
@app.route('/view_movie', methods=['GET', 'POST'])
def view_movie():
    if request.method == 'POST':
        Username = session.get('username')
        if not Username:
            flash('You must be logged in to view your movies.', 'danger')
            return render_template('prelogin_home.html')

        list_of_movies = get_user_movies(Username)

        #Used ChatGPT here to handle the flow of movies stored in DynamoDB into SQL and the RDS
        escaped_titles = [title for title in list_of_movies]
        placeholders = ', '.join(['%s'] * len(escaped_titles))

        query = f"""
            SELECT 
                m.title,
                m.release_date,
                m.budget,
                m.revenue
            FROM 
                movie m
            WHERE 
                m.title IN ({placeholders});
            """

        results = execute_query(query, escaped_titles)
        
        return render_template('view_movie.html', movies=results)

    return render_template('view_movie.html')

#-------------------------------------------
# Delete movie from user account
#-------------------------------------------
@app.route('/delete_movie', methods=['GET', 'POST'])
def delete_movie():
    Username = session.get('username')
    if not Username:
            flash('You must be logged in to view your movies.', 'danger')
            return render_template('prelogin_home.html')
    if request.method == 'POST':
        Title = request.form['Title']
        Username = session.get('username')
        
        delete_movie_db(Title, Username)
        
        return render_template('homepage.html')

    else:
        return render_template('delete_movie.html')
    
#-------------------------------------------
# Logout route - clears session and returns to login page
#-------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return render_template('prelogin_home.html')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)