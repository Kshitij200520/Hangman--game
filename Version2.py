import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Fruit Bliss Hangman Game")
        self.master.geometry("400x550")
        self.master.configure(bg="#E0FFFF")  # Setting the background color to a light blue
        
        self.heading_label = tk.Label(self.master, text="FRUIT BLISS HANGMAN GAME", font=("Helvetica", 16, "bold"), fg="green", bg="#E0FFFF")
        self.heading_label.pack(pady=10)
        
        self.words = ["apple", "banana", "orange", "grape", "pear", "kiwi", "melon", "strawberry", "pineapple", "blueberry"]
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.attempts_left = 6
        self.score = 0
        
        self.canvas = tk.Canvas(self.master, width=200, height=200, bg="white")
        self.canvas.pack()
        
        self.draw_hangman(6)
        
        self.word_label = tk.Label(self.master, text=self.display_word(), font=("Helvetica", 24), fg="blue", bg="#E0FFFF")
        self.word_label.pack()
        
        self.info_label = tk.Label(self.master, text=f"Length of word: {len(self.word)} | Attempts left: {self.attempts_left}", font=("Helvetica", 12), fg="green", bg="#E0FFFF")
        self.info_label.pack()
        
        self.instruction_label = tk.Label(self.master, text="Enter a single letter guess and click Guess.", font=("Helvetica", 12), fg="black", bg="#E0FFFF")
        self.instruction_label.pack()
        
        self.input_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.input_entry.pack()
        
        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess, font=("Helvetica", 14), bg="orange", fg="white")
        self.guess_button.pack()
        
        self.game_over = False  # Flag to track if the game is over
        self.game_played = False  # Flag to track if the game has been played
    
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
                display += '_'
        return display
    
    def make_guess(self):
        if self.game_over:  # Check if the game is over
            messagebox.showinfo("Game Over", "The game has already ended. Please restart.")
            return
        
        if self.game_played:  # Check if the game has been played already
            messagebox.showinfo("Game Over", "You've already played the game once. Please restart to play again.")
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
            self.score += 1
            messagebox.showinfo("Congratulations!", f"You've guessed the word '{self.word}'!\nYour score: {self.score}")
            self.game_played = True  # Set the flag to indicate the game has been played
        
        if self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The word was '{self.word}'.\nYour score: {self.score}")
            self.game_over = True  # Set the flag to indicate the game is over
        
        self.info_label.config(text=f"Length of word: {len(self.word)} | Attempts left: {self.attempts_left}")

def main():
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
