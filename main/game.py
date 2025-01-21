#!/usr/bin/env python3

import json
import random
import firebase_admin
from firebase_admin import credentials, db
from tabulate import tabulate

def initialise_database():
    cred = credentials.Certificate('credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://capital-city-game-leaderboard-default-rtdb.firebaseio.com/'
    })

def validate_login_code(stored_code, entered_code):
    return stored_code == entered_code

def load_leaderboard(continent):
    ref = db.reference(f'leaderboard/{continent}')
    leaderboard = ref.get()
    if leaderboard is None:
        return []
    return leaderboard

def save_leaderboard(continent, leaderboard):
    ref = db.reference(f'leaderboard/{continent}')
    ref.set(leaderboard)

def display_leaderboard(leaderboard):
    if leaderboard:
        print("\nLeaderboard:")
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        
        table_data = []
        for idx, entry in enumerate(leaderboard, start=1):
            table_data.append([idx, entry['name'], entry['score']])

        print(tabulate(table_data, headers=["Rank", "Name", "Score"], tablefmt="fancy_grid"))
    else:
        print("\nLeaderboard is empty")

def load_data():
    with open('database.json', 'r') as file:
        return json.load(file)

def play_game(continent_data):
    points = 0
    random.shuffle(continent_data)
    for entry in continent_data:
        capital = entry['capital']
        country = entry['country']
        difficulty = entry['difficulty'].lower()
        answer = input(f"What is the capital of {country}? ").capitalize()
        if answer.lower() == capital.lower():
            print("Correct!")
            if difficulty == "easy":
                points += 1
                print("+1 point!")
            elif difficulty == "medium":
                points += 2
                print("+2 points!")
            elif difficulty == "hard":
                points += 3
                print("+3 points!")
        elif len(answer) == 0:
            print(f"Pass. The correct answer was {capital}")
        elif answer.lower() == "exit":
            print("Exiting game...")
            break
        else:
            print(f"Wrong! The capital of {country} is {capital}")
    return points

def main():
    initialise_database()

    played_before = input("Have you played before? (yes/no): ").lower()
    valid_continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

    if played_before == 'yes':
        name = input("What is your name? ").capitalize()
        login_code = input("Enter your 4-digit login code: ")

        valid_login = False
        continent = None

        for cont in valid_continents:
            leaderboard = load_leaderboard(cont)
            for entry in leaderboard:
                if entry['name'].lower() == name.lower():
                    if validate_login_code(entry['login_code'], login_code):
                        valid_login = True
                        continent = cont
                    break
            if valid_login:
                break

        if not valid_login:
            print("Invalid login. Please try again.")
            return

    else:
        name = input("What is your name? ").capitalize()
        login_code = input("Create your 4-digit login code: ")
        while len(login_code) != 4 or not login_code.isdigit():
            print("Invalid code. Please enter a 4-digit number.")
            login_code = input("Create your 4-digit login code: ")

        print(f"Welcome {name}! Your login code is: {login_code}")

    continent = input("Which continent would you like to play: ").capitalize()
    while continent not in valid_continents:
        print("Invalid input. Please try again.")
        continent = input("Which continent would you like to play: ").capitalize()

    data = load_data()
    continent_data = data[continent]
    points = play_game(continent_data)

    leaderboard = load_leaderboard(continent)
    player_exists = False
    for entry in leaderboard:
        if entry['name'].lower() == name.lower():
            player_exists = True
            if points > entry['score']:
                entry['score'] = points
            break

    if not player_exists:
        leaderboard.append({'name': name, 'score': points, 'login_code': login_code})

    save_leaderboard(continent, leaderboard)
    display_leaderboard(leaderboard)

if __name__ == '__main__':
    main()
