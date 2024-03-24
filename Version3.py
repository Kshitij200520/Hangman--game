import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("400x600")
        self.master.configure(bg="#F0F8FF")  # Setting the background color to a light blue
        
        self.words = {"Fruits": {"Easy": ["apple", "banana", "orange", "grape", "pear"],
                                  "Medium": ["kiwi", "melon", "strawberry", "pineapple", "blueberry"],
                                  "Hard": ["mango", "pomegranate", "avocado", "watermelon", "guava"]},
                      "Animals": {"Easy": ["dog", "cat", "fish", "bird", "rabbit"],
                                  "Medium": ["lion", "tiger", "elephant", "monkey", "giraffe"],
                                  "Hard": ["hippopotamus", "crocodile", "chimpanzee", "penguin", "rhinoceros"]},
                      "Cars": {"Easy": ["ford", "toyota", "honda", "nissan", "chevrolet"],
                               "Medium": ["volkswagen", "mercedes", "bmw", "audi", "hyundai"],
                               "Hard": ["maserati", "lamborghini", "ferrari", "bugatti", "bentley"]}}
        
        self.categories = list(self.words.keys())
        
        self.category = tk.StringVar(master)
        self.category.set(self.categories[0])  # Default category
        
        self.difficulty = tk.StringVar(master)
        self.difficulty.set("Easy")  # Default difficulty level
        
        self.previous_score = 0
        
        self.game_frame = tk.Frame(self.master, bg="#F0F8FF")  # Light blue background
        self.game_frame.pack(pady=20)
        
        self.game_heading = tk.Label(self.game_frame, text="HANGMAN GAME", bg="#F0F8FF", font=("Helvetica", 20, "bold"), padx=10, pady=5)
        self.game_heading.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        self.category_label = tk.Label(self.game_frame, text="Select Category:", bg="#F0F8FF", font=("Helvetica", 12))
        self.category_label.grid(row=1, column=0, sticky="nsew")
        
        self.category_menu = tk.OptionMenu(self.game_frame, self.category, *self.categories)
        self.category_menu.config(bg="#E0FFFF", font=("Helvetica", 10))  # Light cyan background
        self.category_menu.grid(row=1, column=1, sticky="nsew")
        
        self.difficulty_label = tk.Label(self.game_frame, text="Select Difficulty:", bg="#F0F8FF", font=("Helvetica", 12))
        self.difficulty_label.grid(row=1, column=2, sticky="nsew")
        
        self.difficulty_menu = tk.OptionMenu(self.game_frame, self.difficulty, *self.words[self.categories[0]].keys())
        self.difficulty_menu.config(bg="#E0FFFF", font=("Helvetica", 10))  # Light cyan background
        self.difficulty_menu.grid(row=1, column=3, sticky="nsew")
        
        self.start_button = tk.Button(self.game_frame, text="Start Game", command=self.start_new_game, bg="#FFA500", fg="white", font=("Helvetica", 12))
        self.start_button.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        
        self.instructions_button = tk.Button(self.game_frame, text="Instructions", command=self.show_instructions, bg="#FFA500", fg="white", font=("Helvetica", 12))
        self.instructions_button.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        
        self.hint_button = tk.Button(self.game_frame, text="Hint", command=self.get_hint, bg="#FFA500", fg="white", font=("Helvetica", 12))
        self.hint_button.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        
        self.previous_score_label = tk.Label(self.game_frame, text=f"Previous Score: {self.previous_score}", bg="#F0F8FF", font=("Helvetica", 12))
        self.previous_score_label.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.master, width=200, height=200, bg="#FFFFFF")  # White background
        self.canvas.pack()
        
        self.word_label = tk.Label(self.master, text="", font=("Helvetica", 24), fg="#0000FF", bg="#F0F8FF")  # Blue text, light blue background
        self.word_label.pack()
        
        self.info_label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="#008000", bg="#F0F8FF")  # Green text, light blue background
        self.info_label.pack()
        
        self.input_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.input_entry.pack()
        
        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess, bg="#FFA500", fg="white", font=("Helvetica", 14))
        self.guess_button.pack()
        
        self.game_over = False  # Flag to track if the game is over
        self.game_played = False  # Flag to track if the game has been played
        
        self.time_limits = {"Easy": 50, "Medium": 40, "Hard": 30}  # Time limits for each difficulty level
        self.time_label = tk.Label(self.game_frame, text="", bg="#F0F8FF", font=("Helvetica", 12))
        self.time_label.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        self.time_remaining = 0
        
        self.timer_running = False  # Flag to track if the timer is running
        self.timer_id = None

    def start_new_game(self):
        if not self.timer_running:
            self.start_button.config(state="disabled")
            self.start_game()
            self.update_time()

    def start_game(self):
        self.game_over = False
        self.game_played = False
        
        self.word = random.choice(self.words[self.category.get()][self.difficulty.get()])
        self.guessed_letters = []
        self.attempts_left = 6
        
        self.draw_hangman(6)
        self.word_label.config(text=self.display_word())
        self.info_label.config(text=f"Length of word: {len(self.word)} | Attempts left: {self.attempts_left}")
        
        self.time_remaining = self.time_limits[self.difficulty.get()]  # Set time limit based on difficulty
        self.timer_running = True

    def update_time(self):
        if self.timer_running and not self.game_over:  # Check if the timer is running and the game is not over
            if self.time_remaining > 0:
                self.time_label.config(text=f"Time Left: {self.time_remaining} seconds")
                self.time_remaining -= 1
                self.timer_id = self.master.after(1000, self.update_time)
            else:
                self.timer_running = False
                self.master.after_cancel(self.timer_id)
                self.game_over = True
                messagebox.showinfo("Time's Up", "Sorry, you ran out of time!")
                self.start_button.config(state="normal")

    def make_guess(self):
        if not self.timer_running:
            messagebox.showinfo("Game Over", "Please start a new game.")
            return
        
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)
        
        if not guess.isalpha():  # Check if the guess contains special characters
            messagebox.showwarning("Invalid Guess", "Please enter only alphabetical characters.")
            return
        
        if len(guess) != 1:
            messagebox.showwarning("Invalid Guess", "Please enter a single alphabetical character.")
            return
        
        if guess in self.guessed_letters:
            messagebox.showinfo("Repeated Guess", "You've already guessed this letter. Try a different one.")
            return
        
        self.guessed_letters.append(guess)
        self.word_label.config(text=self.display_word())
        
        if guess not in self.word:
            self.attempts_left -= 1
            self.draw_hangman(self.attempts_left)
        
        if self.display_word() == self.word:
            self.previous_score += 1
            self.previous_score_label.config(text=f"Previous Score: {self.previous_score}")
            messagebox.showinfo("Congratulations!", f"You've guessed the word '{self.word}'!\nYour score: {self.previous_score}")
            self.game_played = True  # Set the flag to indicate the game has been played
            self.timer_running = False
            self.start_button.config(state="normal")
        
        if self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The word was '{self.word}'.\nYour score: {self.previous_score}")
            self.game_over = True  # Set the flag to indicate the game is over
            self.timer_running = False
            self.start_button.config(state="normal")
        
        if self.game_over:
            self.master.after_cancel(self.timer_id)  # Stop the timer if the game ends
        
        self.info_label.config(text=f"Length of word: {len(self.word)} | Attempts left: {self.attempts_left} | Time Left: {self.time_remaining} seconds")

    def get_hint(self):
        if not self.timer_running:
            messagebox.showinfo("Game Over", "Please start a new game.")
            return
        
        if not self.guessed_letters:
            hint = random.choice(self.word)
            messagebox.showinfo("Hint", f"One of the letters in the word is '{hint}'.")
        else:
            remaining_letters = [letter for letter in self.word if letter not in self.guessed_letters]
            if remaining_letters:
                hint = random.choice(remaining_letters)
                messagebox.showinfo("Hint", f"One of the remaining letters in the word is '{hint}'.")
            else:
                messagebox.showinfo("Hint", "No hints available. You've guessed all the letters!")
        
        self.previous_score -= 1  # Deduct score for using hint
        self.previous_score_label.config(text=f"Previous Score: {self.previous_score}")

    def draw_hangman(self, attempts_left):
        self.canvas.delete("all")
        if attempts_left < 6:
            self.canvas.create_line(10, 190, 100, 190, width=2)
        if attempts_left < 5:
            self.canvas.create_line(55, 190, 55, 10, width=2)
        if attempts_left < 4:
            self.canvas.create_line(55, 10, 135, 10, width=2)
        if attempts_left < 3:
            self.canvas.create_line(135, 10, 135, 35, width=2)
        if attempts_left < 2:
            self.canvas.create_oval(120, 35, 150, 65, width=2)
        if attempts_left < 1:
            self.canvas.create_line(135, 65, 135, 110, width=2)
            self.canvas.create_line(135, 75, 120, 90, width=2)
            self.canvas.create_line(135, 75, 150, 90, width=2)
            self.canvas.create_line(135, 110, 120, 125, width=2)
            self.canvas.create_line(135, 110, 150, 125, width=2)
    
    def display_word(self):
        display = ''
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter
            else:
                display += '_ '
        return display
    
    def show_instructions(self):
        messagebox.showinfo("Instructions",
                            "Welcome to Hangman Game!\n\n"
                            "Instructions:\n"
                            "1. Select a category of words from the dropdown menu.\n"
                            "2. Select the difficulty level.\n"
                            "3. Click 'Start Game' to begin playing.\n"
                            "4. Guess letters by typing them in the entry box and pressing 'Guess'.\n"
                            "5. You have 6 attempts to guess the word correctly.\n"
                            "6. Use the 'Hint' button to get a hint (score penalty for using hint).\n"
                            "7. Your previous game score is displayed at the bottom.\n"
                            "8. Have fun!")

def main():
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
