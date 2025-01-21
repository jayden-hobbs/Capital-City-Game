#!/usr/bin/env python3

import json
import random
import firebase_admin
from firebase_admin import credentials, db

def initialise_database():
    cred = credentials.Certificate('credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://capital-city-game-leaderboard-default-rtdb.firebaseio.com/'
    })

def load_leaderboard(continent):
    ref = db.reference(f'leaderboards/{continent}')
    leaderboard = ref.get()
    if leaderboard is None:
        return []
    return leaderboard

def save_leaderboard(continent, leaderboard):
    ref = db.reference(f'leaderboards/{continent}')
    ref.set(leaderboard)

def display_leaderboard(continent, leaderboard):
    if leaderboard:
        print(f"\nLeaderboard for {continent}:")
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        for idx, entry in enumerate(leaderboard, start=1):
            print(f"{idx}. {entry['name']} - {entry['score']} points")
    else:
        print(f"\nLeaderboard for {continent} is empty")

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
        else:
            print(f"Wrong! The capital of {country} is {capital}")
    return points

def main():
    initialise_database()

    name = input("What is your name? ").capitalize()
    print(f"Hello {name}! Welcome to the Capital City Game!")
    
    valid_continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    continent = input("Which continent would you like to play: ").capitalize()
    while continent not in valid_continents:
        print("Invalid input. Please try again.")
        continent = input("Which continent would you like to play: ").capitalize()

    data = load_data()
    continent_data = data[continent]
    points = play_game(continent_data)

    leaderboard = load_leaderboard(continent)
    leaderboard.append({'name': name, 'score': points})
    save_leaderboard(continent, leaderboard)

    display_leaderboard(continent, leaderboard)

if __name__ == '__main__':
    main()
