from flask import Flask, render_template, request, redirect, url_for, flash, session 
from dbTesting import *
from dynamoDB import *

app = Flask(__name__)
app.secret_key = creds.secret_key

#-------------------------------------------
# Flask Home Page (Defaults to login page)
#-------------------------------------------
@app.route('/')
def home():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('homepage.html')

#-------------------------------------------
# Flask Login Page
#-------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Get form data
        Username = request.form['Username']
        Password = request.form['Password']
        
        # Example: Fetch user from DynamoDB (you might want a real check)
        response = table.get_item(Key={'Username': Username})
        user = response.get('Item')

        if user and user['Password'] == Password:
            session['username'] = Username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # or redirect to url_for('home')
        else:
            flash('Invalid username or password.', 'danger')
            return render_template('enter_credentials.html')
    
    return render_template('enter_credentials.html')


#-------------------------------------------
# Flask Sign-Up Page
#-------------------------------------------
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form['Username']
        Password = request.form['Password']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        create_user(Username, Password)
        
        return render_template('login.html')
                        
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')



#-------------------------------------------
# Add movie to user account
#-------------------------------------------
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    Username = session.get('username')
    if request.method == 'POST':
        if not Username:
            flash('You must be logged in to view your movies.', 'danger')
            return render_template('login.html')
        # Extract form data
        Title = request.form['Title']
        Username = session.get('username')
        
        # Add the movie to the user's Movies list in DynamoDB
        add_movie_db(Title, Username)
        
        return render_template('homepage.html')  # Redirect back to the home page

    else:
        # Render the form page if the request method is GET
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
            return render_template('login.html')

        list_of_movies = get_user_movies(Username)
        print("Movies List:", list_of_movies)  # Add this line to check the list of movies

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
            return render_template('login.html')
    if request.method == 'POST':
        Title = request.form['Title']
        Username = session.get('username')
        
        delete_movie_db(Title, Username)
        
        return render_template('homepage.html')

    else:
        return render_template('delete_movie.html')
    
@app.route('/logout')
def logout():
    session.clear()  # Clears the session data, logging the user out
    flash('You have been logged out successfully.', 'success')  # Optional: Flash message
    return render_template('login.html')  # Redirect to the login page after logout
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)