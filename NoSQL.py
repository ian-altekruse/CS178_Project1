# name: Ian Altekruse 
# date: 03/04/2025
# description: Implementation of CRUD operations with DynamoDB database CS178 Lab #9
# proposed score: 5 (out of 5)  -- if I don't change this, I agree to get 0 points for the lab.

import boto3

TABLE_NAME = "Movies"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def create_movie():
    Title = input("Title: ")
    Ratings = input("Ratings: ").split(", ")
    for r in range(len(Ratings)):
        Ratings[r] = int(Ratings[r])
    Year = int(input("Year: "))
    Genre = input("Genre: ")
    table.put_item(
        Item={
            'Title': Title,
            'Ratings': Ratings,
            'Year': Year,
            'Genre': Genre,
        }
)

def print_movie(movie_dict):
    # print out the values of the movie dictionary
    print("Title: ", movie_dict["Title"])
    print(" Ratings: ", end="")
    for rating in movie_dict["Ratings"]:
        print(rating, end=" ")
    print(" Year: ", movie_dict.get("Year"))
    print(" Genre: ", movie_dict.get("Genre"))
    print()

def print_all_movies():
    response = table.scan() #get all of the movies
    for movie in response["Items"]:
        print_movie(movie)

def update_rating():
    try:
        title=input("What is the movie title? ")
        rating = int(input("What is the rating: "))
        table.update_item(
            Key = {"Title": title}, 
            UpdateExpression = "SET Ratings = list_append(Ratings, :r)", ExpressionAttributeValues = {':r': [rating],}
        )
    except:
        print("error in updating movie rating")
    print('updating movie')


def delete_movie():
    title=input("What is the movie title? ")
    table.delete_item(
    Key={
        'Title': title,
    }
    )    
    print("deleting movie")

def query_movie():
    try:
        title=input("What is the movie title? ")
        response = table.get_item(
        Key={
            'Title': title,
        }
        )
        item = response['Item']
        ratings_list = item['Ratings']

        total = 0
        for r in range(len(ratings_list)):
            total = total + ratings_list[r]

        if len(ratings_list) > 0:  # Prevents division by zero
            print(f"The average ratings for {title} is {round(total / len(ratings_list), 2)}")
        else:
            print(f"No ratings available for {title}.")
    except:
        print("movie not found")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a new movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to Query a movie's average ratings")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print('Not a valid option. Try again.')
main()
