import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
SOUND_DIR = ASSETS / "sounds"

BG_OUTER = "#aaaaaa"
BG_PAGE = "#202020"
BG_BANNER = "#aaaaaa"
BG_PANEL = "#5a5a5a"
BORDER = "#000000"
HIT = "#75ff69"
PRESENT = "#ffdb23"
MISS = "#555555"
EMPTY = "#ffffff"
CHAR_EMPTY = "#d3d6da"

def play_sound(name):
    if not sys.platform.startswith("win"):
        return
    import winsound
    winsound.PlaySound(str(SOUND_DIR / name), winsound.SND_FILENAME | winsound.SND_ASYNC)

def load_words(filename="solutions.txt"):
    with open(BASE / filename, "r") as f:
        return [w.strip().lower() for w in f if len(w.strip()) == 5]

def feedback(guess, answer):
    res = ["miss"] * 5
    pool = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            res[i] = "hit"
            pool[i] = None

    for i in range(5):
        if res[i] == "hit":
            continue
        g = guess[i]
        if g in pool:
            res[i] = "present"
            pool[pool.index(g)] = None

    return res

class WordleWindow:
    def __init__(self, master, words_file="solutions.txt"):
        self.master = master
        master.title("Wordle")
        master.configure(bg=BG_OUTER)

        self.words = load_words(words_file)
        self.valid = set(self.words)
        self.answer = random.choice(self.words)
        self.state = {}
        self.row = 0

        play_sound("new_game.wav")

        page = tk.Frame(master, bg=BG_PAGE, padx=40, pady=40)
        page.pack(padx=40, pady=40, fill="both", expand=True)

        banner = tk.Frame(page, bg=BG_BANNER, padx=20, pady=30)
        banner.pack(fill="x")
        tk.Label(banner, text="Wordle", font=("Georgia", 36, "bold"),
                 bg=BG_BANNER, fg="black").pack()

        outer = tk.Frame(page, bg=BORDER)
        outer.pack(fill="both", expand=True)

        panel = tk.Frame(outer, bg=BG_PANEL, bd=10, relief="solid")
        panel.pack(fill="both", expand=True)

        board = tk.Frame(panel, bg=BG_PANEL)
        board.pack(pady=(20, 10))

        self.tiles = []
        for r in range(6):
            row_tiles = []
            for c in range(5):
                lbl = tk.Label(board, width=4, height=2, font=("Consolas", 18, "bold"),
                               bg=EMPTY, relief="solid", bd=2)
                lbl.grid(row=r, column=c, padx=4, pady=4)
                row_tiles.append(lbl)
            self.tiles.append(row_tiles)

        self.char = {}
        char_frame = tk.Frame(panel, bg=BG_PANEL)
        char_frame.pack(pady=(5, 10))

        for row in ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"):
            rf = tk.Frame(char_frame, bg=BG_PANEL)
            rf.pack()
            for ch in row:
                lbl = tk.Label(rf, text=ch, width=3, height=1,
                               font=("Consolas", 14, "bold"),
                               bg=CHAR_EMPTY, fg="black")
                lbl.pack(side="left", padx=3, pady=3)
                self.char[ch.lower()] = lbl

        inp = tk.Frame(panel, bg=BG_PANEL)
        inp.pack(pady=(10, 10))

        self.entry = tk.Entry(inp, font=("Consolas", 16), width=10)
        self.entry.grid(row=0, column=0, padx=5)
        self.entry.bind("<Return>", lambda e: self.submit())

        tk.Button(inp, text="Submit", font=("Georgia", 12),
                  command=self.submit).grid(row=0, column=1, padx=5)

        self.msg = tk.StringVar()
        tk.Label(panel, textvariable=self.msg, bg=BG_PANEL,
                 fg="white", font=("Georgia", 12)).pack(pady=(5, 0))

        self.entry.focus_set()

    def set_msg(self, t=""):
        self.msg.set(t)

    def paint_char(self, guess, fb):
        for ch, s in zip(guess, fb):
            old = self.state.get(ch)
            if old == "hit":
                continue
            if s == "hit":
                self.state[ch] = "hit"
            elif s == "present" and old != "hit":
                self.state[ch] = "present"
            elif old not in ("hit", "present"):
                self.state[ch] = "miss"

        for ch, lbl in self.char.items():
            s = self.state.get(ch)
            if s == "hit":
                lbl.config(bg=HIT, fg="white")
            elif s == "present":
                lbl.config(bg=PRESENT, fg="white")
            elif s == "miss":
                lbl.config(bg=MISS, fg="white")
            else:
                lbl.config(bg=CHAR_EMPTY, fg="black")

    def submit(self):
        if self.row >= 6:
            return

        guess = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 5 or not guess.isalpha():
            return self.set_msg("Please enter exactly 5 letters.")
        if guess not in self.valid:
            return self.set_msg("That word is not in the word list.")

        play_sound("hit.wav")

        for i, ch in enumerate(guess):
            self.tiles[self.row][i].config(text=ch.upper())

        fb = feedback(guess, self.answer)
        for i, s in enumerate(fb):
            self.tiles[self.row][i].config(
                bg=HIT if s == "hit" else PRESENT if s == "present" else MISS,
                fg="white",
            )

        self.paint_char(guess, fb)

        if guess == self.answer:
            tries = self.row + 1
            self.set_msg(f"You got it in {tries} {'try' if tries == 1 else 'tries'}!")
            play_sound("wordle_win.wav")
            messagebox.showinfo("Wordle", "You win!")
            self.row = 6
            return

        self.row += 1
        if self.row == 6:
            ans = self.answer.upper()
            self.set_msg(f"Out of tries! The word was {ans}.")
            play_sound("wordle_lose.wav")
            messagebox.showinfo("Wordle", f"Out of tries!\nThe word was {ans}.")
        else:
            self.set_msg()

def open_wordle(parent, words_file="solutions.txt"):
    win = tk.Toplevel(parent)
    WordleWindow(win, words_file)
    return win

if __name__ == "__main__":
    root = tk.Tk()
    open_wordle(root)
    root.mainloop()