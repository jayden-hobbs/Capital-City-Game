#!/usr/bin/env python3

import json
import random

def load_data():
    with open('country-capital.json', 'r') as file:
        return json.load(file)
    
def play_game(continent):
    points = 0
    random.shuffle(continent)
    for entry in continent:
        capital = entry['capital']
        country = entry['country']
        difficulty = entry['difficulty']
        answer = input(f"What is the capital of {country}? ").capitalize()
        if answer.lower() == capital.lower():
            if difficulty == "easy":
                points += 1
            elif difficulty == "medium":
                points += 2
            else:
                points += 3
            print("Correct!")
            print("+1 point!" if difficulty == "easy" else "+2 points!" if difficulty == "medium" else "+3 points!")
        else:
            print(f"Wrong! The capital of {country} is {capital}")
    return points

def main():
    name = input("What is your name? ").capitalize()
    print(f"Hello {name}! Welcome to the Capital City Game!")
    continent = input("Which continent would you like to play: ").capitalize()
    if continent in ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']:
        data = load_data()
        points = play_game(data[continent])
        print(f"Game over! You scored {points} points!")

if __name__ == '__main__':
    main()
