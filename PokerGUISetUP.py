import raylibpy as rl
import os, random, time, math

# ----------------------------- #
# --------- Variables --------- #
# ----------------------------- #
PokerTableBackground_File = r"C:\Users\patri\Downloads\PokerTableBackGround_v3.png"
PokerTableBackground_Image = rl.load_image(str(PokerTableBackground_File))
Background_width = PokerTableBackground_Image.width
Background_height = PokerTableBackground_Image.height
rl.init_window(Background_width, Background_height, "PokerTable yo")
PokerTableBackground_Texture = rl.load_texture_from_image(PokerTableBackground_Image)

CARD_WIDTH = 86
CARD_HEIGHT = 129


RiverCardImages = {} # using dict cause board so dont change or maybe will break. Maybe wont idk 
DealerCardImages = {}
PlayerCardImages = {}
Ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
Suits = ['hearts', 'diamonds', 'clubs', 'spades']
# ----------------------------- #
# --------- Functions --------- #
# ----------------------------- #

def CardLoader(Rank, Suit, dict_ref, Dealt_card = None): # Pass cards into this to add it into the players/rivers hand 
    if Dealt_card != None:
        Rank = Dealt_card.rank
        Suit = Dealt_card.suit
    if isinstance(Rank, str): # In case the rank is a string, make sure its all lowercase. The png files are lowercase
        Rank = Rank.lower()    
    if isinstance(Suit, str): # In case the Suit is a string, make sure its all lowercase. The png files are lowercase
        Suit = Suit.lower()
    filename = rf"C:\Users\patri\Downloads\PNG-cards-1.3\{Rank}_of_{Suit}.png"
    
    if os.path.exists(filename):
        cardimg = rl.load_image(str(filename))
        rl.image_resize(cardimg, CARD_WIDTH, CARD_HEIGHT)
        dict_ref[Rank,Suit] = rl.load_texture_from_image(cardimg)
        rl.unload_image(cardimg)
        
    else: 
        return "No Card Found"
def Draw_cards(card_dict, start_x, start_y, spacing = 35): # draws the cards themselves onto the board
    n = len(card_dict)
    if n == 0:
        return
    x = start_x
    total_width = n * CARD_WIDTH + (n - 1) * spacing
    if card_dict != RiverCardImages:
        for (rank,suit), i in card_dict.items():
            x = int(753 - total_width / 2)

    for (rank,suit), i in card_dict.items():
        rl.draw_texture(i, x, start_y, rl.WHITE)
        x += (CARD_WIDTH + spacing)

#########################
# Note to WIll, if you dont like my BRILLIANT card overide cause its lowkey jank af heres a solution ( I REFUSE TO TEST IT SO SUCK IT NERD)
# Remember to remove the overide part from the other one if you do use this code but if you dont then dont i honestly dont care cause its 12:58 am rn so lowkey idc anymore
# def CardLoaderFromCard(card_obj, dict_ref):
#     CardLoader(card_obj.rank, card_obj.suit, dict_ref)
#################################

# --------------------------- #
# --------- Classes --------- #
# --------------------------- #
class card:
    def __init__(self, rank, suit,):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'
class Deck:
    def __init__(self, ranks_parameter, suits_parameter):
        self.deck = []
        for rank in ranks_parameter:
            for suit in suits_parameter:
                self.deck.append(card(rank, suit))

    def length(self):
        cardNum = 0
        for i in self.deck:
            cardNum += 1
        return cardNum

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        card_one = self.deck.pop()
        return card_one

deck = Deck(Ranks, Suits)
deck.shuffle()


CardLoader(5, "diamonds", RiverCardImages)
CardLoader(7, "spades", RiverCardImages)
CardLoader("ace", "hearts", RiverCardImages)
CardLoader("Ace", "spades", PlayerCardImages)
CardLoader("king", "spades", DealerCardImages)
CardLoader("Jack", "spades", DealerCardImages)
CardLoader("Queen", "spades", DealerCardImages)
CardLoader(None, None, RiverCardImages, deck.deal()) # This can be used as a dealt card override so its easier than making a function and all that. Basically just pass the deal a card class attr and it should graph it. 

for _ in range(4):
    CardLoader(None, None, PlayerCardImages, deck.deal())

while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_texture(PokerTableBackground_Texture , 0, 0, rl.WHITE)
        Draw_cards(RiverCardImages, 468, 426)
        Draw_cards(DealerCardImages, 710, 255, spacing = -60)
        Draw_cards(PlayerCardImages, 710, 615, spacing = -60 )
        rl.end_drawing()
        
rl.unload_texture(PokerTableBackground_Texture)
rl.close_window()
