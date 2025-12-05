import tkinter as tk
import math, time, random, os 

ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♠", "♥", "♦", "♣"]


def Load_image(): 
    folder = PNG-cards-1.3
    for rank in ranks: 
        for suit in suits: 
            filename = f"{folder}/{suit}{rank}.png"
            card_images[(rank,suit)] = tk.PhotoImage(file=filename)

