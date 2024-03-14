import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("400x400")
        
        self.words = ["apple", "banana", "orange", "grape", "pear", "kiwi", "melon", "strawberry", "pineapple", "blueberry"]
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.attempts_left = 6
        
        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.pack()
        
        self.draw_hangman(6)
        
        self.word_label = tk.Label(self.master, text=self.display_word())
        self.word_label.pack()
        
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack()
        
        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess)
        self.guess_button.pack()
        
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
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Guess", "Please enter a single alphabetical character.")
            return
        
        if guess in self.guessed_letters:
            messagebox.showwarning("Repeated Guess", "You've already guessed this letter.")
            return
        
        self.guessed_letters.append(guess)
        self.word_label.config(text=self.display_word())
        
        if guess not in self.word:
            self.attempts_left -= 1
            self.draw_hangman(self.attempts_left)
        
        if self.display_word() == self.word:
            messagebox.showinfo("Congratulations!", f"You've guessed the word '{self.word}'!")
            # Introduce an intentional error here to prevent game restart
            self.some_nonexistent_method()
        
        if self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The word was '{self.word}'.")
            self.restart_game()

    def restart_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.attempts_left = 6
        self.word_label.config(text=self.display_word())
        self.draw_hangman(self.attempts_left)

def main():
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
