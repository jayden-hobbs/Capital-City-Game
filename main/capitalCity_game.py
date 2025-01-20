#!/usr/bin/env python3

import json
import random

def load_data():
    with open('database.json', 'r') as file:
        return json.load(file)
    
def play_game(continent):
    points = 0
    random.shuffle(continent)
    for entry in continent:
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
    name = input("What is your name? ").capitalize()
    print(f"Hello {name}! Welcome to the Capital City Game!")
    vaild_continents = ['Africa', 'Asia' , 'Europe', 'North America', 'South America', 'Oceania']
    continent = input("Which continent would you like to play: ").capitalize()
    while continent not in vaild_continents:
        print("Invaild input. Please try again")
        continent = input("Which continent would you like to play: ").capitalize()

    data = load_data()
    points = play_game(data[continent])

if __name__ == '__main__':
    main()
