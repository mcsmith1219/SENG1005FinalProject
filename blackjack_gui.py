import tkinter as tk
import random
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
CARD_DIR = ASSETS
SOUND_DIR = ASSETS / "sounds"

BG_OUTER = "#aaaaaa"
BG_PAGE = "#202020"
BG_BANNER = "#aaaaaa"
BG_PANEL = "#5a5a5a"
BORDER = "#000000"

MAX_W, MAX_H = 100, 150
VALUES = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10,"A":11}

def play_sound(name):
    if not sys.platform.startswith("win"):
        return
    import winsound
    winsound.PlaySound(str(SOUND_DIR / name), winsound.SND_FILENAME | winsound.SND_ASYNC)

def create_deck():
    return [f"{r}{s}" for r in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
            for s in ["S","H","D","C"]]

def hand_value(hand):
    total = sum(VALUES[c[:-1]] for c in hand)
    aces = sum(1 for c in hand if c[:-1] == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

class BlackjackWindow:
    def __init__(self, master):
        self.master = master
        master.title("Blackjack")
        master.configure(bg=BG_OUTER)

        self.deck, self.p, self.d = [], [], []
        self.over = False
        self.cache = {}
        self.back = self._img(CARD_DIR / "dealercard.png")

        page = tk.Frame(master, bg=BG_PAGE, padx=40, pady=40)
        page.pack(padx=40, pady=40, fill="both", expand=True)

        banner = tk.Frame(page, bg=BG_BANNER, padx=20, pady=30)
        banner.pack(fill="x")
        tk.Label(banner, text="Blackjack", font=("Georgia", 32, "bold"),
                 bg=BG_BANNER, fg="black").pack()

        outer = tk.Frame(page, bg=BORDER)
        outer.pack(fill="both", expand=True)

        panel = tk.Frame(outer, bg=BG_PANEL, bd=10, relief="solid")
        panel.pack(fill="both", expand=True)

        df = tk.Frame(panel, bg=BG_PANEL); df.pack(pady=(10,10), fill="x")
        tk.Label(df, text="Dealer", font=("Georgia", 16, "bold"),
                 bg=BG_PANEL, fg="white").pack(anchor="w")
        self.d_cards = tk.Frame(df, bg=BG_PANEL); self.d_cards.pack(anchor="w", pady=(5,0))
        self.d_total = tk.StringVar(value="Dealer total: ?")
        tk.Label(df, textvariable=self.d_total, font=("Georgia", 12),
                 bg=BG_PANEL, fg="white").pack(anchor="w", pady=(5,0))

        pf = tk.Frame(panel, bg=BG_PANEL); pf.pack(pady=(10,10), fill="x")
        tk.Label(pf, text="Player", font=("Georgia", 16, "bold"),
                 bg=BG_PANEL, fg="white").pack(anchor="w")
        self.p_cards = tk.Frame(pf, bg=BG_PANEL); self.p_cards.pack(anchor="w", pady=(5,0))
        self.p_total = tk.StringVar(value="Player total: 0")
        tk.Label(pf, textvariable=self.p_total, font=("Georgia", 12),
                 bg=BG_PANEL, fg="white").pack(anchor="w", pady=(5,0))

        self.status = tk.StringVar(value="Click New Game to begin.")
        tk.Label(panel, textvariable=self.status, font=("Georgia", 12),
                 bg=BG_PANEL, fg="white", wraplength=400, justify="center").pack(pady=(10,10))

        bf = tk.Frame(panel, bg=BG_PANEL); bf.pack(pady=(5,10))
        self.hit_btn = tk.Button(bf, text="Hit", width=10, font=("Georgia", 14, "bold"),
                                 command=self.hit, state="disabled")
        self.hit_btn.grid(row=0, column=0, padx=10)
        self.stand_btn = tk.Button(bf, text="Stand", width=10, font=("Georgia", 14, "bold"),
                                   command=self.stand, state="disabled")
        self.stand_btn.grid(row=0, column=1, padx=10)
        tk.Button(bf, text="New Game", width=10, font=("Georgia", 14),
                  command=self.new_game).grid(row=0, column=2, padx=10)

        self.new_game()

    def _img(self, path):
        img = tk.PhotoImage(file=str(path))
        w, h = img.width(), img.height()
        s = max(w // MAX_W, h // MAX_H, 1)
        return img.subsample(s, s) if s > 1 else img

    def card_img(self, code):
        if code not in self.cache:
            self.cache[code] = self._img(CARD_DIR / f"{code}.png")
        return self.cache[code]

    def show(self, frame, hand, hide_second=False):
        for w in frame.winfo_children():
            w.destroy()
        for i, card in enumerate(hand):
            img = self.back if (hide_second and i == 1) else self.card_img(card)
            lbl = tk.Label(frame, image=img, bg=BG_PANEL)
            lbl.image = img
            lbl.pack(side="left", padx=4)

    def refresh(self, hide_dealer=False):
        if hide_dealer:
            self.show(self.d_cards, self.d, hide_second=True)
            self.d_total.set("Dealer total: ?")
        else:
            self.show(self.d_cards, self.d)
            self.d_total.set(f"Dealer total: {hand_value(self.d)}")

        self.show(self.p_cards, self.p)
        self.p_total.set(f"Player total: {hand_value(self.p)}")

    def end(self, msg, win=False):
        self.over = True
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.refresh(hide_dealer=False)
        self.status.set(msg)
        play_sound("win.wav" if win else "lose.wav")

    def new_game(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.p = [self.deck.pop(), self.deck.pop()]
        self.d = [self.deck.pop(), self.deck.pop()]
        self.over = False
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")
        self.refresh(hide_dealer=True)
        self.status.set("Hit or Stand?")
        play_sound("new_game.wav")

    def hit(self):
        if self.over:
            return
        self.p.append(self.deck.pop())
        self.refresh(hide_dealer=True)
        play_sound("hit.wav")
        if hand_value(self.p) > 21:
            self.end("Player busts! Dealer wins.", win=False)

    def stand(self):
        if self.over:
            return
        while hand_value(self.d) < 17:
            self.d.append(self.deck.pop())

        pt, dt = hand_value(self.p), hand_value(self.d)
        if dt > 21:
            self.end("Dealer busts! You win!", win=True)
        elif dt > pt:
            self.end("Dealer wins.", win=False)
        elif dt < pt:
            self.end("You win!", win=True)
        else:
            self.end("It's a tie!", win=False)

def open_blackjack(parent):
    win = tk.Toplevel(parent)
    BlackjackWindow(win)
    return win

if __name__ == "__main__":
    root = tk.Tk()
    open_blackjack(root)
    root.mainloop()