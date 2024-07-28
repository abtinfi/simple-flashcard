from fsrs import *
from datetime import datetime, timezone
import json
import os

flashcards = []

def save_file():
    global flashcards
    try:
        with open("flashcards.json", "w") as f:
            json.dump(flashcards, f, indent=4)
            print("File saved at:", os.path.abspath("flashcards.json"))
    except Exception as e:
        print(f"Error saving file: {e}")

def review_flashcard(flashcard):
    print(flashcard["question"])
    input("Press Enter to show the answer...")
    print(flashcard["answer"])
    print("How well did you remember the answer?\n1) Again\n2) Hard\n3) Good\n4) Easy")
    rate = None
    while True:
        try:
            n = int(input())
            if n in [1, 2, 3, 4]:
                rate = Rating(n)
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a number.")

    f = FSRS()
    card = Card.from_dict(flashcard["card"])
    if flashcard["review_log"]:
        card_log = ReviewLog.from_dict(flashcard["review_log"])
        card, card_log = f.review_card(card, rate)
    else:
        card, card_log = f.review_card(card, rate)

    flashcard["card"] = card.to_dict()
    flashcard["review_log"] = card_log.to_dict()
    return flashcard

def get_due_cards():
    global flashcards
    due_cards = []
    for i in flashcards:
        new_card = Card.from_dict(i["card"])
        if new_card.due <= datetime.now(timezone.utc):
            due_cards.append(i)
    return due_cards

def read_file():
    global flashcards
    try:
        with open("flashcards.json", "r") as f:
            flashcards = json.load(f)
            print("File loaded successfully.")
    except FileNotFoundError:
        print("No saved flashcards found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    except Exception as e:
        print(f"Error reading file: {e}")
    print(flashcards)

def add_flashcard():
    global flashcards
    while True:
        print("Enter question:")
        temp_question = input()
        print("Enter answer:")
        temp_answer = input()
        card = Card()
        flashcards.append(
            {
                "question": temp_question,
                "answer": temp_answer,
                "card": card.to_dict(),
                "review_log": None,
            }
        )
        save_file()
        n = input("Do you want to finish? Enter 0\n")
        if n == "0":
            break

def main_menu():
    while True:
        print("\nFlashcard System Menu")
        print("1. Add Flashcard")
        print("2. Review Due Flashcards")
        print("3. Save Flashcards")
        print("4. Load Flashcards")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_flashcard()
        elif choice == "2":
            due_cards = get_due_cards()
            if due_cards:
                for card in due_cards:
                    review_flashcard(card)
            else:
                print("No due cards to review.")
        elif choice == "3":
            save_file()
        elif choice == "4":
            read_file()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
