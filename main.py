import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from wordle_gui import open_wordle
from rockpaperscissors_gui import open_rockpaperscissors
from blackjack_gui import open_blackjack

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"

BG_OUTER = "#aaaaaa"
BG_PAGE  = "#202020"
BG_BANNER = "#aaaaaa"
BG_PANEL = "#5a5a5a"
BORDER_COLOR = "#000000"

class ThreeGamesApp:
    def __init__(self, root):
        self.root = root
        root.title("3Games")
        root.configure(bg=BG_OUTER)

        page = tk.Frame(root, bg=BG_PAGE, padx=40, pady=40)
        page.pack(padx=40, pady=40, fill="both", expand=True)

        banner = tk.Frame(page, bg=BG_BANNER, padx=20, pady=50)
        banner.pack(fill="x")
        tk.Label(banner, text="3Games", font=("Georgia", 48, "bold"),
                 bg=BG_BANNER, fg="black").pack()

        panel_outer = tk.Frame(page, bg=BORDER_COLOR)
        panel_outer.pack(fill="both", expand=True)

        content_panel = tk.Frame(panel_outer, bg=BG_PANEL)
        content_panel.pack(fill="both", expand=True)

        tabs_frame = tk.Frame(content_panel, bg=BG_PANEL)
        tabs_frame.pack(anchor="w", pady=(0, 30))

        self.make_tab_button(tabs_frame, "Homepage", self.show_home_info)
        self.make_tab_button(tabs_frame, "About 3Games", self.show_about_info)
        self.make_tab_button(tabs_frame, "Contact Us", self.show_contact_info)

        games_frame = tk.Frame(content_panel, bg=BG_PANEL)
        games_frame.pack(pady=(0, 20))

        self.images = {
            "blackjack": tk.PhotoImage(file=str(ASSETS / "BlackjackLogo.png")),
            "wordle": tk.PhotoImage(file=str(ASSETS / "WordleLogo.png")),
            "rockpaperscissors": tk.PhotoImage(file=str(ASSETS / "RockPaperScissorsLogo.png")),
        }

        tk.Button(games_frame, image=self.images["blackjack"], bg=BG_PANEL, bd=0,
                  relief="flat", command=self.open_blackjack).grid(row=0, column=0, padx=30, pady=10)
        tk.Button(games_frame, image=self.images["wordle"], bg=BG_PANEL, bd=0,
                  relief="flat", command=self.open_wordle_game).grid(row=0, column=1, padx=30, pady=10)
        tk.Button(games_frame, image=self.images["rockpaperscissors"], bg=BG_PANEL, bd=0,
                  relief="flat", command=self.open_rockpaperscissors).grid(row=0, column=2, padx=30, pady=10)

    def make_tab_button(self, parent, text, command):
        tk.Button(parent, text=text, font=("Georgia", 14, "bold"),
                  bg=BG_PANEL, fg="#FFFFFF",
                  activebackground="#5a5a5a", activeforeground="#5a5a5a",
                  relief="flat", bd=0, padx=20, pady=8,
                  command=command).pack(side="left", padx=5)

    def show_home_info(self):
        messagebox.showinfo("Homepage", "You're on the homescreen, bozo.")

    def show_about_info(self):
        messagebox.showinfo(
            "About 3Games",
            "3Games is a small collection of mini-games: Blackjack, Wordle, and Rock Paper Scissors built using Python and Tkinter! "
            "If you enjoy casual gaming, give them a try!.. And if you don't, ALT-F4!"
        )

    def show_contact_info(self):
        messagebox.showinfo("Contact Us", "Literally don't do that LOL.")

    def open_wordle_game(self):
        open_wordle(self.root)

    def open_blackjack(self):
        open_blackjack(self.root)

    def open_rockpaperscissors(self):
        open_rockpaperscissors(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    ThreeGamesApp(root)
    root.mainloop()