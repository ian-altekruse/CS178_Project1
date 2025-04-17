from flask import Flask, render_template, request, redirect, url_for, flash, session 
from mysql_rds import *
from dynamoDB import * 

app = Flask(__name__)
app.secret_key = creds.secret_key



#------------------------------------------------------------------------
#Used ChatGPT to help with 'session' code and the RDS and DynamoDB connection
#------------------------------------------------------------------------


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

        status = create_new_user(Username, Password)

        if status == False:
            flash('Username already in use.', 'danger')
            return render_template('prelogin_home.html')

        if status == True:
            flash('Account successfully created.', 'success')
            return render_template('prelogin_home.html')    
                            
    else:
        return render_template('create_user.html')

#-------------------------------------------
# Add movie to user account
#-------------------------------------------
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    Username = session.get('username')
    if not Username:
        flash('You must be logged in to add movies.', 'danger')
        return render_template('prelogin_home.html')

    if request.method == 'POST':
        Title = request.form['Title']
        
        status = add_movie_db(Title, Username)

        if status == 1:
            flash('Movie added successfully!', 'success')
        elif status == 2:
            flash('Invalid movie title.', 'warning')
        elif status == 3:
            flash('Movie already exists in your list.', 'info')

        return redirect(url_for('home'))  # After flashing, always redirect.

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
        if list_of_movies == []:
            flash('No movies found.', 'danger')
            return redirect(url_for('home'))
        else:
            #Used ChatGPT here to handle the flow of movies stored in DynamoDB into SQL and the RDS
            escaped_titles = [title for title in list_of_movies]
            placeholders = ', '.join(['%s'] * len(escaped_titles))

            #Had to chatGPT the group_concat part of the SQL query 
            query = f"""
                    SELECT 
                        m.title,
                        m.release_date,
                        m.budget,
                        m.revenue,
                        GROUP_CONCAT(pc.company_name ORDER BY pc.company_name SEPARATOR ', ') AS production_companies
                    FROM 
                        movie m
                    JOIN 
                        movie_company mc ON m.movie_id = mc.movie_id
                    JOIN 
                        production_company pc ON mc.company_id = pc.company_id
                    WHERE 
                        m.title IN ({placeholders})
                    GROUP BY 
                        m.movie_id;
                """


            results = execute_query(query, escaped_titles)
        
            return render_template('view_movie.html', movies=results)

    return redirect(url_for('home'))

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
        flash('Movie successfully deleted.', 'success')

        
        return redirect(url_for('home'))

    else:
        movies = get_user_movies(Username) 
        return render_template('delete_movie.html', movies = movies)
    
#-------------------------------------------
# Logout route - clears session and returns to login page
#-------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return render_template('prelogin_home.html')

#-------------------------------------------
# Change Password route
#-------------------------------------------
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form['username']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        if change_user_password(username, current_password, new_password):
            flash('Password updated successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password.', 'danger')
            return redirect(url_for('change_password'))
    
    return render_template('change_password.html')


    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)