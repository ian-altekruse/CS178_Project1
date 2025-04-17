# CS178 Project 1 - Movie Manger - Ian Altekruse

## Project Summary
For my project, I created a movie manager website. Through my website, users can do the following...  
- Create a user with a username and password
- Login using that username and password
- Add movies to their watchlist
- View movies on their watchlist (along with other information pulled from the movies database, such as release date, revenue, etc.)
- Delete movies from their watchlist
- Change their password
- Logout

## Technologies Used
For this project, I used the following technologies...  
- Flask (for programming the website and routes)
- Python (for running code)
- AWS RDS (for hosting movies database)
- AWS EC2 (for hosting website)
- AWS DynamoDB (for hosting user information in NoSQL table)
- MySQL (for running queries to pull extra movie information)

## Setup and Run Instructions
### Steps for Setup  
- Clone Github Repo
- Add creds.py file and include RDS information (host, user, password, database)
- Run FlaskApp.py and make it persistent using 'nohup python3 FlaskApp.py &'
  
### Run Instructions
- Once you run the file, navigate to your EC2 instance public IP, followed by :8080 (ex: 100.0.000.00:8080/)
- You will then be directed to the main login page, which gives you the option to create an account or login
- Once you login, click add movie and enter a movie title (repeat as many times as you want)
- After adding movies, click view movies to see a list of all your added movies
- You can also delete movies using the delete movie movie button
- You can also change your password using the change password button
- Lastly, you can logout using the logout button
- 
