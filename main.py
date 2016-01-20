# Mini-project - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
HSDtext = ""
infotext = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        our_hand="Hand contains "
        for i in range(len(self.cards)):
            our_hand += str(self.cards[i]) + " "
        return our_hand
            

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.get_rank() == "A":
                num_aces += 1
            value += VALUES[card.get_rank()]
        if num_aces > 0:
            if value + 10 > 21:
                return value
            else:
                return value + 10
        else:
            return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos = (pos[0]+ 90, pos[1])
        
      

        
# define deck class 
class Deck:
    def __init__(self):
        self.card_deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.card_deck.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_deck)

    def deal_card(self):
        # deal a card object from the deck
        self.dc = self.card_deck.pop()
        return self.dc
    
    def __str__(self):
        self.our_deck="Deck contains "
        for i in range(len(self.card_deck)):
            self.our_deck += str(self.card_deck[i]) + " "
        return self.our_deck

#define event handlers for buttons
def deal():
    global outcome, in_play, pl_hand, my_deck, com_hand, HSDtext, score, infotext

    # your code goes here
    my_deck = Deck()
    my_deck.shuffle()
    
    pl_hand = Hand()
    com_hand = Hand()
    
    pl_hand.add_card(my_deck.deal_card())
    com_hand.add_card(my_deck.deal_card())
    pl_hand.add_card(my_deck.deal_card())
    com_hand.add_card(my_deck.deal_card())

    
    #score decreased if deal pressed in the middle of a game
    if outcome == "" and in_play == True:
        score -= 1
        infotext = "New deal counted as loss"  
    in_play = True
    HSDtext = "Hit or Stand?"
    outcome = ""

def hit():
    global pl_hand, my_deck, outcome, score, HSDtext, infotext
    # if the hand is in play, hit the player
    
    #remove deal text when hit is pressed again
    infotext = ""
    
    if pl_hand.get_value() <= 21:
        pl_hand.add_card(my_deck.deal_card())
        
        # if busted, assign a message to outcome, update in_play and score
        if pl_hand.get_value() > 21:
            outcome = "You have busted"
            score -= 1
            HSDtext = "New Draw?"
       
def stand():
    global pl_hand, my_deck, com_hand, in_play, HSDtext, outcome, score
    
    if pl_hand.get_value() > 21:
        print "You have busted"
    else:
        while com_hand.get_value() < 17:
            com_hand.add_card(my_deck.deal_card())
        
        if com_hand.get_value() > 21:
            outcome = "Player wins"
            score += 1
        elif com_hand.get_value() >= pl_hand.get_value():
            outcome = "Dealer wins"
            score -= 1
        else:
            outcome = "Player wins"
            score += 1
        # assign a message to outcome, update in_play and score
        in_play = False
        HSDtext = "New draw?"
    
# draw handler    
def draw(canvas):
    global pl_hand, my_deck, com_hand, CARD_BACK_CENTER, CARD_BACK_SIZE, in_play, HSDtext, outcome, score, infotext

    canvas.draw_text('Black Jack', [230, 60], 50, 'Grey')
    canvas.draw_text('Black Jack', [232, 62], 50, 'Black')
    
    #HSDtext
    canvas.draw_text(HSDtext, [260, 550], 30, 'Grey')
    canvas.draw_text(HSDtext, [261, 551], 30, 'Black')
    
    #New deal counted as loss
    canvas.draw_text(infotext, [225, 580], 20, 'Grey')
    canvas.draw_text(infotext, [226, 581], 20, 'Red')
    
    #Score
    canvas.draw_text("Score", [510, 35], 20, 'Grey')
    canvas.draw_text("Score", [511, 36], 20, 'Black')
    canvas.draw_text(str(score), [530, 60], 20, 'Grey')
    canvas.draw_text(str(score), [531, 61], 20, 'Black')
    
    #outcome text
    canvas.draw_text(outcome, [320, 170], 30, 'Grey')
    canvas.draw_text(outcome, [321, 171], 30, 'Black')
    
    #Dealer
    canvas.draw_text('Dealer', [100, 170], 30, 'Grey')
    canvas.draw_text('Dealer', [101, 171], 30, 'Black')
    com_hand.draw(canvas, [100,200])
    #Draw back card
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (135, 245), (75, 100))
    
    #Player
    canvas.draw_text('Player', [100, 370], 30, 'Grey')
    canvas.draw_text('Player', [101, 371], 30, 'Black')
    pl_hand.draw(canvas, [100,400])
    
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_label("")
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
