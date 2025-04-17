import boto3
from mysql_rds import *

TABLE_NAME = "Users"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

#-----------------------------------------------------------
# Creating Users with username and password
#------------------------------------------------------------
def create_new_user(User, Password):
    response = table.get_item(Key={'Username': User})
    user_data = response.get('Item')
    if user_data:
        return False
    else:
        table.put_item(
         Item={
             'Username': User,
             'Password': Password,
         }
         
 )
        return True

#-----------------------------------------------------------
# Adding movies to list in DynamoDB
#------------------------------------------------------------
def add_movie_db(Title, Key):
    current_movies = get_user_movies(Key)
    if Title not in current_movies:
        if test_movie(Title) == True:
            table.update_item(
                Key={'Username': Key},
                UpdateExpression="SET Movies = list_append(if_not_exists(Movies, :empty_list), :new_movie)", ExpressionAttributeValues={':new_movie': [Title],':empty_list': []}
            )
            return 1
        else:
            return 2
    else:
        return 3

#-----------------------------------------------------------
# Deleting movies from list in DynamoDB
#------------------------------------------------------------

def delete_movie_db(Title, Key):
    response = table.get_item(Key={'Username': Key})
    user_data = response.get('Item')
    
    if 'Movies' in user_data:
        movies_list = user_data['Movies']
        if Title in movies_list:
            movies_list.remove(Title)
        
            table.update_item(
                Key={'Username': Key},
                UpdateExpression="SET Movies = :new_movies",ExpressionAttributeValues={':new_movies': movies_list}
            )


#---------------------------------------------------
# Get movies for the logged-in user from DynamoDB
#---------------------------------------------------
def get_user_movies(username):
    response = table.get_item(Key={'Username': username})
    user = response.get('Item')
    
    if user and 'Movies' in user:
        return user['Movies']
    return []

#---------------------------------------------------
# Change Password
#---------------------------------------------------
def change_user_password(User, Password, New_Password):
    response = table.get_item(Key={'Username': User})
    user_data = response.get('Item')
    
    if user_data and user_data['Password'] == Password:
        table.update_item(
            Key={'Username': User}, UpdateExpression='SET Password = :p',ExpressionAttributeValues={':p': New_Password}
        )
        return True
    else:
        return False





