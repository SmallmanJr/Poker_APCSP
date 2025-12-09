import pyray as rl
import os, random, time, math
import re
from pokerkit import * 
from itertools import combinations
# ----------------------------- #
# --------- Variables --------- #
# ----------------------------- #
PokerTableBackground_File = r"PokerTableBackGround_v3.png"
PokerTableBackground_Image = rl.load_image(str(PokerTableBackground_File))
Background_width = PokerTableBackground_Image.width
Background_height = PokerTableBackground_Image.height

rl.init_window(Background_width, Background_height, "PokerTable yo")
PokerTableBackground_Texture = rl.load_texture_from_image(PokerTableBackground_Image)

CARD_WIDTH = 86
CARD_HEIGHT = 129
Dealt = False
startTime=time.time()
card_images = {}
Ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
Suits = ['hearts', 'diamonds', 'clubs', 'spades']

players = []
activePlayers = []
List_of_PlayersChips = []

betting_mode = False
bet_buffer = ""

current_turn_index = 0  # 0 = Dealer, 1 = Player NOTE: Will replace later just am so tired rn
Turn = "Player"
# --------------------------- #
# --------- Classes --------- #
# --------------------------- #
class card:
    def __init__(self, Rank, Suit,):
        self.Rank = Rank
        self.Suit = Suit

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
    
class Hand:
    def __init__(self, Name):
        global players
        self.name = Name

        self.cards = []
        self.value = 0
        self.PokerKitStr = ""
        if Name != "River": 
            if Name is not None:
                players.append(self)
                activePlayers.append(self)
           
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
class Chips:
    def __init__(self, Name):
        self.total = 1000
        self.betamount = 0 
        self.name = Name
        List_of_PlayersChips.append(self)
        
    def __str__(self):
        return f'{self.name}'
        
    def __repr__(self):
        return f'{self.name}'   
    
Rank_map = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:"T", "Jack":"J", "Queen":"Q", "King":"K", "Ace":"A"}
Suit_map = {'hearts':"h", 'diamonds':"d", 'clubs':"c", 'spades':"s"}

# ----------------------------- #
# --------- Functions --------- #
# ----------------------------- #
'''
def ConvertTextToFormat(CardHand):
    TempList = []
    for i, card in enumerate(CardHand.cards):
        rank = card.Rank
        suit = card.Suit
        Rank_temp = Rank_map[rank]
        Suit_temp = Suit_map[suit]
        card = f"{Rank_temp}{Suit_temp}"
        TempList.append(card)
        Combined = ''.join(TempList)
        CardHand.PokerKitStr = str(Combined)
    return CardHand.PokerKitStr
'''
def CheckWin(Cheating = False):
    if Cheating:
        
        for player in enumerate(activePlayers):
            print(player.cards, "Cards")
    else:
        strengthList=[]
        lookup = StandardLookup()
        for i, player in enumerate(activePlayers):
            total_hand = RiverHand.cards + player.cards
            result = list(combinations(total_hand,5))
            
            
            best_strength = max( # Had to use chatgpt because the documentation for pokerkit was subpar so i could understand how to properly interate through the tuple (each combo of hand) in the list of all possible hands so i could create the dumb syntax pokerkit wants. Sorry.
                StandardHighHand("".join(f"{Rank_map[c.Rank]}{Suit_map[c.Suit]}" for c in combo))
                for combo in result
            )
            strengthList.append((player, best_strength))
            print(f"The best hand for {player} is {best_strength.entry.label}" )
            print(best_strength.entry.index)
        print(f"the stregnth list is{strengthList}")

        
        winner = None
        Firshand = strengthList[0]
        for t in strengthList:
            print('stage one')
            print("t is equal to", t)
            if t[1].entry.index > Firshand[1].entry.index:
                print("stage two")
                strongest_tuple = t
                winner = t[0]
                break

                
        
        print("The winner is", winner)
        
        return winner
        
        

def CardLoader(Rank, Suit):
    # Just loads the cards into the game from the folder when needed. Shouldnt ever need  to use this. 
    Suit = Suit.lower()
    if isinstance(Rank, str):
        Rank = Rank.lower()
        
        
        
    if (Rank,Suit) in card_images:
        return card_images[(Rank,Suit)]
    
    
    
    filename = rf"png-cards-1.3\{Rank}_of_{Suit}.png"
    if os.path.exists(filename):
        cardimg = rl.load_image(filename)
        rl.image_resize(cardimg, CARD_WIDTH, CARD_HEIGHT)
        texture = rl.load_texture_from_image(cardimg)
        rl.unload_image(cardimg)
        card_images[(Rank, Suit)] = texture
        return texture
    else:
        print("No Card")
        return


def DrawCards(Hand, Start_x, Start_y, spacing = 35):
    # Function to draw cards at a x and y value based on their hand. Can control the spacing of the cards.     

    if len(Hand.cards) == 0:
        return None
    n = len(Hand.cards)

    x = Start_x
    total_width = n * CARD_WIDTH + (n - 1) * spacing
    if Hand != RiverHand:
        x = int(753 - total_width / 2)



    for c in Hand.cards:
        tex = CardLoader(c.Rank, c.Suit)
        if tex:
            rl.draw_texture(tex, x, Start_y, rl.WHITE)
        x += CARD_WIDTH + spacing

def HittingCard(Hand):
    # add card to hand function. Just pass it the hand you want to add a card to. 
    newcard = deck.deal()
    Hand.cards.append(newcard)
def testing(Userhand):
    print(Userhand)
def Check_or_call(UserChips, OverRide = False): 
    # Check and call function. First it checks for a override (such as it they dont have a chip sent), then for each player that isnt the userchip(target user) add their bet to a list. if there are other bets, pick the highest bet. If that highest bet is greater than the userchips bet then set userchips bet equal to highest. 
    # Check what turn number it is in the list of chips then adds one to add the dealer. Add +1 for the next turn then returns it. 
    
    #note i think i need to fix the turn system cause its a little dumb
    global Turn

    Other_bets = []
    if not OverRide: 
        for p in List_of_PlayersChips:
            print(p)
            if p is not UserChips:
                Other_bets.append(p.betamount) 
                print("Player ")
  
            
    if Other_bets:
        highestbet = max(Other_bets)
        if UserChips.betamount < highestbet:
            UserChips.betamount = highestbet
    print("Advancing")
    advance_turn()
    '''        
    current_turn = List_of_PlayersChips.index(UserChips) + 1 # Dealer will never be in the list but will have a turn of 0 
    next_turn = current_turn +1
    Turn = players[next_turn]
    print(f'Current turn is {current_turn}, next turn is {next_turn}, now turn is {Turn}')
    '''
def Fold(UserHand): # fold Function which removes the player from the active player list
    global players, activePlayers
    IndexNumb = activePlayers.index(UserHand)
    activePlayers.pop(IndexNumb)
    advance_turn()

def advance_turn(): #ill replace later just am so tired bro 
    global current_turn_index, Turn
    current_turn_index = (current_turn_index + 1) % len(players)
    Turn = players[current_turn_index]
    
def Start(DealerHand, PlayerHand): # Function to start the game. If it isnt already dealt, give both the dealer and the player cards.
    global Dealt, players


    if Dealt:
        return

    for i in range(2):
        HittingCard(DealerHand)
        HittingCard(PlayerHand)

        
    Dealt = True
    return Dealt

# ----------------------------- #
# --------- Draw GUI --------- #
# ----------------------------- # 
deck = Deck(Ranks,Suits)
deck.shuffle(), deck.shuffle() # Proper double shuffle baby
RiverHand = Hand("River")
DealerHand = Hand("Dealer")
PlayerHand = Hand("Player")

PlayerChips = Chips("Player")
BotChips = Chips("Bot")
BotChips.betamount = 100

BlankHand=Hand(None)
BlankHand.cards=[card('blank','clubs'),card('blank','clubs')]
testing(RiverHand)
print("Type is", type(RiverHand))
firstThree = False
current_turn_index = 1  # 0 = Dealer, 1 = Player
betamountsaved = 1000
while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.draw_texture(PokerTableBackground_Texture , 0, 0, rl.WHITE)
    rl.draw_text(f"turn: {Turn}_", 100, 120, 30, rl.BLUE)
    if Turn == "Player":
        if rl.is_key_pressed(rl.KEY_B):
            betting_mode = True
            #bet_buffer = "" # clears that shit 
            
        if rl.is_key_pressed(rl.KEY_C):
            if Turn == "Player":
                Check_or_call(PlayerChips)
                
        if rl.is_key_pressed(rl.KEY_F):
            print(players)
            Fold(PlayerHand)
            print(players)
        
    
    if betting_mode:
        key = rl.get_key_pressed()
        while key > 0: 
            if key == rl.KEY_ENTER:
                if bet_buffer != "":
                    PlayerChips.betamount = int(bet_buffer)
                    PlayerChips.total -= PlayerChips.Betamount # makes the player bet from the bet buffer 
                    if PlayerChips.betamount  > PlayerChips.total:
                        PlayerChips.betamount  = PlayerChips.total # all in function 
                betting_mode = False
                break
            elif key == rl.KEY_BACKSPACE:
                bet_buffer = bet_buffer[:-1] # had to google what would remove the last value of the str which is this dumb thing :-1 which means the last number we remove which is nice
            elif rl.KEY_ZERO <= key <= rl.KEY_NINE:
                # Every key has a keycode so if you just add the key to the bet buffer it adds the keycode to it not the number (learned the hard way) 
                # To remove the keycode subtract the keycode of what you want from the keycode of zero so you have the difference
                
                digit = key - rl.KEY_ZERO   # 0–9
                bet_buffer += str(digit)

            key = rl.get_key_pressed()

    if betting_mode:
        rl.draw_text(f"Bet: {bet_buffer}_", 100, 60, 30, rl.BLUE)
        rl.draw_text("Press Enter to finish betting. Type numbers in to bet", 100, 950, 25, rl.BLUE)
    else:
        rl.draw_text(f"Bet: {PlayerChips.betamount}", 100, 60, 30, rl.BLUE)



    if rl.is_key_pressed(rl.KEY_W):
        Start(DealerHand, PlayerHand)



        
    if not Dealt:
        rl.draw_text("Press W to Start", 620, 700, 30, rl.BLUE)

    
    if len(RiverHand.cards) == 5 and Turn == "Dealer" and Dealt:
        CheckWin()
        winner = CheckWin
        rl.draw_text(f"The winner is: {winner}", 700, 500, 30, rl.BLUE)
        break
        
    if Turn == "Dealer":
        print("Trying to play for dealer")
        Check_or_call(Playerchips, OverRide = True)
        print("Trying to play for deale 2r")
        if firstThree == False:
            HittingCard(RiverHand)
        else:
            HittingCard(RiverHand)
    rl.draw_text("Press B to Hit", 100, 800, 25, rl.BLUE)
    rl.draw_text("Press F to Fold", 100, 850, 25, rl.BLUE)
    rl.draw_text("Press C to Check/call", 100, 900, 25, rl.BLUE)
    if Dealt:
        deltaTime=time.time()-startTime

        if deltaTime>3:
            pass

        if deltaTime>3:
            DrawCards(RiverHand, 468, 426)
        if deltaTime>2:
            DrawCards(BlankHand, 710, 255, spacing = -60)

        if deltaTime>1:
            DrawCards(PlayerHand, 710, 615, spacing = -60 )

    rl.end_drawing()
        
rl.unload_texture(PokerTableBackground_Texture)

rl.close_window()
