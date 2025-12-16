import pyray as rl
import os, random, time, math, re
from pokerkit import * 
from itertools import combinations

# --------- Variables --------- #

PokerTableBackground_File = r"PokerTableBackGround_v3.png" # BackGround Image. Being used as the poker table. 
PokerTableBackground_Image = rl.load_image(str(PokerTableBackground_File)) #Load Image
Background_width = PokerTableBackground_Image.width # Sets the width of the game to the width of the background image. Same with height. 
Background_height = PokerTableBackground_Image.height

rl.init_window(Background_width, Background_height, "PokerTable yo") 
PokerTableBackground_Texture = rl.load_texture_from_image(PokerTableBackground_Image)

RevealDealerCards = False
CARD_WIDTH = 86
CARD_HEIGHT = 129
Dealt = False # if cards have been dealt
startTime=time.time()
card_images = {}

Ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
Suits = ['hearts', 'diamonds', 'clubs', 'spades']

players = [] # List of every player in the game
activePlayers = [] # list of every player still in the game

betting_mode = False # Moide that allows the player to change their bet amount. 
bet_buffer = "" 
Turn = "Player" 

PlayerChipConvert = {} # Used to convert the names and chips of players back and forth. 
PlayerNameConvert = {}

# --------- Classes --------- #

class card: # Class to define the attributes of the card. The card is defined by its rank and suit so we can make a class to create cards easily with its rank and suits for later use. 
    def __init__(self, Rank, Suit,):
        self.Rank = Rank
        self.Suit = Suit

    def __str__(self):
        return f'{self.Rank} of {self.Suit}'
class Deck: # The deck being used in the game. Is created by all the ranks and suits in the deck, for each card we add it to a list to represent the deck info. 
    def __init__(self, ranks_parameter, suits_parameter):
        self.deck = []
        for rank in ranks_parameter:
            for suit in suits_parameter:
                self.deck.append(card(rank, suit))

    def shuffle(self): # Function to shuffle deck
        random.shuffle(self.deck)

    def deal(self): # Deals a single card out. 
        card_one = self.deck.pop()
        return card_one
class Hand: # Class to create the persons hand. Has information on its name, cards in deck. 
    def __init__(self, Name):
        global players
        self.name = Name

        self.cards = []

        if Name != "River": # if the hand is a actual hand (aka not the river), add the persons data into a list of players and active players so we know who is playing. 
            if Name is not None:
                players.append(self)
                activePlayers.append(self)
           
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return self.name


class Chips: # Class to define the chips a person has. Has information of their total money, their bet, their name, and then adds that info into a dict so we can convert between hands and chips later.
    def __init__(self, Name):
        self.total = 1000
        self.betamount = 0 
        self.name = Name
        PlayerChipConvert[Name] = self
        PlayerNameConvert[Name] = self

        
    def __str__(self):
        return f'{self.name}'
        
    def __repr__(self):
        return self.name   
    



# --------- Functions --------- #

def CheckWin(players, RiverHand): 
    # Function to check the winner of the game. If you pass the list of total players and the riverhand itself you are able to determine, for each player, who had the best hand and then says that player wins. 

    Rank_map = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:"T", "Jack":"J", "Queen":"Q", "King":"K", "Ace":"A"} # Used to convert how we handle numbers and names for cards into format pokerkit enjoys. PokerKit is a library to determine hand strength as imported
    Suit_map = {'hearts':"h", 'diamonds':"d", 'clubs':"c", 'spades':"s"} # Used to convert the name of the suits into format that pokerkit enjoys.
    
    bestIndex = -1 # There is no card index(value) yet so we define it to none.
    winner = None
    
    for player in players: # for each player in the list of players
        totalHand = RiverHand.cards + player.cards # Add the rivers hand and the persons hand together so we can have their total 7 card hand.
        ComboList = list(combinations(totalHand,5)) # Makes all the combinations of 5 cards given their 7 card hand. Adds each tuple (combo of hand) into a list. 


        for combo in ComboList: # for each possible varriation 
            handstr = '' 
            for c in combo: # for each card in that varration
                handstr += str(Rank_map[c.Rank]) + Suit_map[c.Suit] # Add the name information of the cards to a str to pass to pokerkit 


            HandStrength = StandardHighHand(handstr) # The strength of that hand 

            HandStrengthValue = HandStrength.entry.index
            
            if bestIndex == -1: # if there isnt yet a card strenght to compare it to, best index is that hand strength. 
                bestIndex = HandStrengthValue
                winner = player
            if HandStrengthValue > bestIndex: # if there is a hand strength to compare it to and its stronger than the best index then thats the new best index. 
                bestIndex = HandStrengthValue
                winner = player
                
    print(f"The Best index is {bestIndex}, the player who won is {winner}; this is running as check win 2")
    return winner
        
        

def CardLoader(Rank, Suit):
    # function to load the card into memory when called upon. When given the rank and suit of the card, we load it. 

    # Just loads the cards into the game from the folder when needed. Shouldnt ever need  to use this. 
    Suit = Suit.lower()
    if isinstance(Rank, str): # if str, make sure the text is lowercase
        Rank = Rank.lower()
        
        
        
    if (Rank,Suit) in card_images: # if the card is already loaded, return the card image data
        return card_images[(Rank,Suit)]
    
    
    
    filename = rf"png-cards-1.3\{Rank}_of_{Suit}.png" # The path location for the cards. 
    if os.path.exists(filename):
        # if the filepath exists
        # ---> Load the image from the filelocation, resize the image to fit our dimensitions
        # ---> Unload the card image from memory and place the card texture intoo a dictionary so we can use it later. 
        
        # The card_images dictionary allows us to give it the rank and suit and it will give us the card texture to load on the board. 


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

    if len(Hand.cards) == 0: # if no cards return nonething
        return None
    n = len(Hand.cards)

    x = Start_x
    total_width = n * CARD_WIDTH + (n - 1) * spacing 
    if Hand != RiverHand: #
        x = int(753 - total_width / 2)
    # The code above centers the card in the middle so if its not the river cards the players cards are in the center of the board so it looks nice. 



    for c in Hand.cards: # for each card in the persons hand
        tex = CardLoader(c.Rank, c.Suit) 
        if tex:
            rl.draw_texture(tex, x, Start_y, rl.WHITE) # Draw the card
        x += CARD_WIDTH + spacing

def HittingCard(Hand):
    # Function to add a card to a hand, if given the hand. 

    newcard = deck.deal() # Card we are adding to hand
    Hand.cards.append(newcard) # Add to hand


def Fold(UserHand):
    AdvanceTurn() # Goes to the next players turn
    # fold Function which removes the player from the active player list
    global players, activePlayers
    IndexNumb = activePlayers.index(UserHand) # Removes the player from the activeplayers list
    activePlayers.pop(IndexNumb)


        
def AdvanceTurn():
    # Function to the next persons turn.  
    global Turn
    CurrentPlayers = []
    for p in activePlayers: # For each player in active players, add their name to a current players list with just their name as a str
        CurrentPlayers.append(p.name)
    print (activePlayers)
    print(CurrentPlayers)
    current_turn = CurrentPlayers.index(Turn) # Get the current persons turn 
    NextTurn = current_turn + 1 # Add one to the turn index number
    if NextTurn > len(activePlayers)-1:
        NextTurn = 0
    NextPlayer = activePlayers[NextTurn]

    Turn = NextPlayer
    return Turn
    
    
def Check_or_call(Userhand):
    # A function that checks a persons hand if there is no higher bet, call if there is. 
    try:
        otherBets = [] # List of other peoples bet amount. Appends into. 
        if Userhand.name is not ["River", "Dealer"]:
            global nameUser
            nameUser = str(Userhand) 
            userChips = PlayerChipConvert.get(nameUser)
            
        for p in activePlayers: # For each player
            if p.name not in ["Dealer, Player", nameUser]: 

                try: 
                    #Get the persons chips from their hand
                    othername = str(p)
                    OtherChips = PlayerChipConvert.get(othername)
                    otherBets.append(OtherChips.betamount)
                except:
                    print(f"{p.name} has no chips")
                    
            elif p in ["Dealer, Player", nameUser]: 
                print("member in rejected list")

                
        if otherBets: # if there are other bets 

            highestBet = max(otherBets) # get the highest bet that others have
            if userChips.betamount < highestBet: # if the user's bet is less than the highestbet, then set the usersbet to that amount
                userChips.betamount = highestBet
                if userChips.betamount > userChips.total: # if the new bet is greater than the amount of money player has, they go all in 
                    userChips.betamount = userChips.total 
                print(userChips.betamount, userChips.name, "New Bet")
    except:
        pass
            
    AdvanceTurn() # Switch turns
    return 


def ManageMoney(winner):
    pot = 0 
    for player in players:
        try: # if the player has chips
            chips = PlayerChipConvert[player]
            pot += chips.betamount # Add the betamount to the pot
            chips.total -= chips.betamount # remove the bet from their total
            chips.betamount = 0 # set bet to zero 
            
            if player == winner: # FOr the winner, give them the pot
                chips.total += pot
        except:
            print(f"{player} has no chips")
        
        
  
def Start(DealerHand, PlayerHand):
    # Function to start the game. If it isnt already dealt, give both the dealer and the player cards.
    global Dealt, players


    if Dealt: 
        return

    for i in range(2):# Give the dealer and player two cards to start
        HittingCard(DealerHand)
        HittingCard(PlayerHand)

        
    Dealt = True
    return Dealt


# --------- Draw GUI --------- #

deck = Deck(Ranks,Suits)
for i in range(100): # Shuffles the deck hundred times
    deck.shuffle() 
RiverHand = Hand("River")
DealerHand = Hand("Dealer")
PlayerHand = Hand("Player")

PlayerChips = Chips("Player")
BotChips = Chips("Bot")
BotChips.betamount = 100

# The blank hand is a hand that has only backside of card cards so we can "hide' the persons hand. This is used to hide the dealers hand for example. 
BlankHand=Hand(None) 
BlankHand.cards=[card('blank','clubs'),card('blank','clubs')]


DealerChips=Chips("Dealer")
firstThree = False # boolean for if we have given down the first 3 middle cards. 
'''
def myAiFunction(winner,playerBet):
    
    if winner==1:
        chips=25
    else:
        chips=0
    if chips<playerBet and chips>0:
        Check_or_call(chips,True)
    else:
        Fold(DealerHand)
'''


while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.draw_texture(PokerTableBackground_Texture , 0, 0, rl.WHITE)
    rl.draw_text(f"turn: {Turn}_", 100, 120, 30, rl.BLUE)
    if Turn == "Player": 
        if rl.is_key_pressed(rl.KEY_B): # When you push the B button, it allows u to change ur bet
            betting_mode = True

            
        if rl.is_key_pressed(rl.KEY_C): # When you push the C button, it checks or calls
            Check_or_call(PlayerHand)
                
        if rl.is_key_pressed(rl.KEY_F): # When you push the F button, it folds the players hand

            Fold(PlayerHand)

        

    if betting_mode: 
        # After the person pushes B it enables 'betting mode'
        # When the person types numbers from 0 to 9 on the keyboard it will type it into 'bet buffer' which is the temp bet
        # When enter is pushed it sets the bet buffer to the actual players bet amount
        # when backspace is pushed it removes a number in the bet buffer so you can adjust your bet if you mess up typing 
        
        key = rl.get_key_pressed()
        while key > 0: 
            if key == rl.KEY_ENTER:
                if bet_buffer != "":
                    PlayerChips.betamount = int(bet_buffer)

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
        # During the bet mode, draw text to explain how bet mode works
        rl.draw_text(f"Bet: {bet_buffer}_", 100, 60, 30, rl.BLUE)
        rl.draw_text("Press Enter to finish betting. Type numbers in to bet", 100, 950, 25, rl.BLUE)
    else:
        # Else, draw the betamount and total 
        rl.draw_text(f"Bet: {PlayerChips.betamount}", 100, 60, 30, rl.BLUE)
        rl.draw_text(f"Total: {PlayerChips.total}", 100, 30, 30, rl.BLUE)



    if rl.is_key_pressed(rl.KEY_W): # When w is pushed, start the game 
        Start(DealerHand, PlayerHand)



    # Draw text to say start game
    if not Dealt: 
        rl.draw_text("Press W to Start", 620, 700, 30, rl.BLUE)

    Turn=str(Turn) # In case the turn is not a str set it to a str


    # Draws the control info on the screen
    rl.draw_text("Press B to Hit", 100, 800, 25, rl.BLUE) 
    rl.draw_text("Press F to Fold", 100, 850, 25, rl.BLUE)
    rl.draw_text("Press C to Check/call", 100, 900, 25, rl.BLUE)
    
    if Dealt:
        
        deltaTime=time.time()-startTime # Delta time so we can sequenctially draw the cards on the screen


        if deltaTime>3: # Draws the middle cards last
            DrawCards(RiverHand, 468, 426)
        if deltaTime>2: # Draws the dealers cards second
            if RevealDealerCards:  # if it should reveal the dealers cards, 
                DrawCards(DealerHand, 710, 255, spacing = -60)
            else: # if not

                DrawCards(BlankHand, 710, 255, spacing = -60)

        if deltaTime>1: # Draw the players cards first
            DrawCards(PlayerHand, 710, 615, spacing = -60 )
            
        if len(RiverHand.cards) == 5 and Turn == "Dealer": # If the middle cards are all dealt and it is now the dealers turn (after the player finishes their last move)
            RevealDealerCards = True # Reveal the dealer cards

            winner = CheckWin(players, RiverHand) # Check the winner
            ManageMoney(winner) # Remove money from losers and give the winner money
            print(winner)
            Turn = "Game Over" # Make it so the turn is now gameover so the game stops trying to allow hitting etc
            
        if Turn == "Game Over":
            # Draw the winner and how to restart the game
            rl.draw_text(f"The winner is: {winner}", 660, 550, 50, rl.BLUE)
            rl.draw_text(f"To Play Again Press P", 700, 100, 30, rl.BLUE)
        if rl.is_key_pressed(rl.KEY_P) and Turn == "Game Over":
            # if the game is over and they push p
            # Reset the every player's cards, make dealt to false cause it isnt yet dealt, reset the middle cards, etc
            print("Fixing game now")
            for player in players:
                player.cards = []
            Dealt = False
            firstThree = False
            bet_buffer = ''
            Turn = "Player"
            RiverHand.cards = []
            RevealDealerCards = False
            startTime = time.time()
            activePlayers[:] = players[:]
            Start(DealerHand, PlayerHand)
    if Turn == "Dealer":#the dealer just makes reandom moves 

        if firstThree == False:
            Check_or_call(DealerHand)
        else:
            randnum=random.randint(0,3)-1#it either bets checks or folds
            if randnum==0:
                DealerChips.betamount=int(random.randint(0,100))
            elif randnum==1:
                Fold(DealerHand)
                print("FOlding dealer")
            else:
                Check_or_call(DealerHand)
        if firstThree==False:
            HittingCard(RiverHand)
            HittingCard(RiverHand)
            firstThree=True
        HittingCard(RiverHand)
    if len(activePlayers)==1:
            
            RevealDealerCards = True # Reveal the dealer cards

            winner = CheckWin(players, RiverHand) # Check the winner
            ManageMoney(winner) # Remove money from losers and give the winner money
            print(winner)
            Turn = "Game Over" # Make it so the turn is now gameover so the game stops trying to allow hitting etc
            
    rl.end_drawing()
        
rl.unload_texture(PokerTableBackground_Texture)

rl.close_window()
