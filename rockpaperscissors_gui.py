import tkinter as tk
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

def play_sound(name):
    if not sys.platform.startswith("win"):
        return
    import winsound
    winsound.PlaySound(str(SOUND_DIR / name), winsound.SND_FILENAME | winsound.SND_ASYNC)

class RockPaperScissorsWindow:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")
        master.configure(bg=BG_OUTER)

        self.choices = ("rock", "paper", "scissors")
        self.ps = 0
        self.cs = 0

        play_sound("new_game.wav")

        page = tk.Frame(master, bg=BG_PAGE, padx=40, pady=40)
        page.pack(padx=40, pady=40, fill="both", expand=True)

        banner = tk.Frame(page, bg=BG_BANNER, padx=20, pady=30)
        banner.pack(fill="x")
        tk.Label(banner, text="Rock Paper Scissors", font=("Georgia", 28, "bold"),
                 bg=BG_BANNER, fg="black").pack()

        outer = tk.Frame(page, bg=BORDER)
        outer.pack(fill="both", expand=True)

        panel = tk.Frame(outer, bg=BG_PANEL, bd=10, relief="solid")
        panel.pack(fill="both", expand=True)

        bf = tk.Frame(panel, bg=BG_PANEL)
        bf.pack(pady=(20, 10))

        for i, ch in enumerate(self.choices):
            tk.Button(bf, text=ch.capitalize(), width=10, font=("Georgia", 14, "bold"),
                      command=lambda x=ch: self.play(x)).grid(row=0, column=i, padx=10)

        self.choice_var = tk.StringVar(value="Make your choice to start!")
        tk.Label(panel, textvariable=self.choice_var, font=("Georgia", 12),
                 bg=BG_PANEL, fg="white", wraplength=400, justify="center").pack(pady=(10, 5))

        self.result_var = tk.StringVar()
        tk.Label(panel, textvariable=self.result_var, font=("Georgia", 14, "bold"),
                 bg=BG_PANEL, fg="white").pack(pady=(5, 10))

        self.score_var = tk.StringVar()
        tk.Label(panel, textvariable=self.score_var, font=("Georgia", 12),
                 bg=BG_PANEL, fg="white").pack(pady=(5, 10))

        tk.Button(panel, text="Reset Score", font=("Georgia", 10),
                  command=self.reset).pack(pady=(5, 10))

        self.update_score()

    def update_score(self):
        self.score_var.set(f"Score - You: {self.ps}   Computer: {self.cs}")

    def play(self, user):
        comp = random.choice(self.choices)
        self.choice_var.set(f"You chose: {user.capitalize()}   |   Computer chose: {comp.capitalize()}")

        if user == comp:
            res = "It's a tie!"
        elif (user, comp) in (("rock","scissors"), ("paper","rock"), ("scissors","paper")):
            res = "You win!"
            self.ps += 1
            play_sound("win.wav")
        else:
            res = "You lose."
            self.cs += 1
            play_sound("lose.wav")

        self.result_var.set(res)
        self.update_score()

    def reset(self):
        self.ps = self.cs = 0
        self.result_var.set("")
        self.choice_var.set("Make your choice to start!")
        self.update_score()

def open_rockpaperscissors(parent):
    win = tk.Toplevel(parent)
    RockPaperScissorsWindow(win)
    return win

if __name__ == "__main__":
    root = tk.Tk()
    open_rockpaperscissors(root)
    root.mainloop()