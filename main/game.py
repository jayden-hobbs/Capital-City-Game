#!/usr/bin/env python3

import json
import random
import firebase_admin
from firebase_admin import credentials, db
from tabulate import tabulate
from colorama import Fore, Back, Style, init

init(autoreset=True)

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
        print(Fore.CYAN + "\nLeaderboard:")
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        
        table_data = []
        for idx, entry in enumerate(leaderboard, start=1):
            table_data.append([idx, entry['name'], entry['score']])

        print(tabulate(table_data, headers=["Rank", "Name", "Score"], tablefmt="fancy_grid"))
    else:
        print(Fore.RED + "\nLeaderboard is empty")

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
        print(Fore.YELLOW + f"\nWhat is the capital of {country}?")
        answer = input("Your answer: ").capitalize()
        if answer.lower() == capital.lower():
            print(Fore.GREEN + "Correct!")
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
            print(Fore.MAGENTA + f"Pass. The correct answer was {capital}")
        elif answer.lower() == "exit":
            print(Fore.YELLOW + "Exiting game...")
            print(f"Your final score is: {points}")
            break
        else:
            print(Fore.RED + f"Wrong! The capital of {country} is {capital}")
    return points

def main():
    initialise_database()

    played_before = input(Fore.CYAN + "Have you played before? (yes/no): ").lower()
    valid_continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'All']

    if played_before == 'yes':
        name = input(Fore.CYAN + "What is your name? ").capitalize()
        login_code = input(Fore.CYAN + "Enter your 4-digit login code: ")

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
            print(Fore.RED + "Invalid login. Please try again.")
            return

    else:
        name = input(Fore.CYAN + "What is your name? ").capitalize()
        login_code = input(Fore.CYAN + "Create your 4-digit login code: ")
        while len(login_code) != 4 or not login_code.isdigit():
            print(Fore.RED + "Invalid code. Please enter a 4-digit number.")
            login_code = input(Fore.CYAN + "Create your 4-digit login code: ")

        print(Fore.GREEN + f"Welcome {name}! Your login code is: {login_code}")

    continent = input(Fore.CYAN + "Which continent would you like to play? (Enter 'All' for every continent): ").capitalize()
    while continent not in valid_continents:
        print(Fore.RED + "Invalid input. Please try again.")
        continent = input(Fore.CYAN + "Which continent would you like to play? (Enter 'All' for every continent): ").capitalize()

    data = load_data()
    if continent == 'All':
        continent_data = sum(data.values(), [])
    else:
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

    if continent == 'All':
        all_continents_leaderboard = load_leaderboard("All Continents")
        player_exists_in_all = False
        for entry in all_continents_leaderboard:
            if entry['name'].lower() == name.lower():
                player_exists_in_all = True
                if points > entry['score']:
                    entry['score'] = points
                break
        if not player_exists_in_all:
            all_continents_leaderboard.append({'name': name, 'score': points, 'login_code': login_code})


if __name__ == '__main__':
    main()
