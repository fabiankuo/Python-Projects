
# coding: utf-8

# In[ ]:


#functions needed for building a black jack game
#set up game:
#deal card
#check if gone over limit
#reset game
#point counting
#winner declaring
#score keeping
#declare a class for cards
#print results(doesn't have to be picture of a card, numbers should suffice)
#classes: Player, CardDeck, Dealer, Card


# In[ ]:


#import random for dealing cards
import random


# In[ ]:


class Player(object):
    
    def __init__(self,hand,name = 'player1',bank=100, bet = 0, win = False):
        self.name = name
        self.bank = bank
        self.hand = hand
        self.bet = bet
        self.win = win
    
    def setName(self, playerName):
        self.name = playerName
    
    def addCard(self, card):
        self.hand['cards'].append(card)
        if card.number == 1:
            self.hand['containsAce'] = True
        self.addPoints(card)
    
    def addPoints(self, card):
        if card.number > 10:
            self.hand['points']['normal']+=10
            self.hand['points']['ace']+=10
        elif card.number == 1:
            self.hand['points']['normal']+=card.number
            self.hand['points']['ace']+=11
        else:
            self.hand['points']['normal']+=card.number
            self.hand['points']['ace']+=card.number            
       
        if (self.hand['points']['ace']>21) & (self.hand['points']['normal']>21):
            self.hand['busted'] = True
        elif self.hand['points']['normal']> 21:
            self.hand['busted'] = True
        
    def placeBet(self):
        while True:
            try:
                bet = int(raw_input('Your bank:%d How much would you like to bet?'%self.bank))
            except:
                print 'Please Enter a valid bet.'
            else:
                if bet > self.bank:
                    print "You don't have enough money. Please enter valid bet."
                elif bet <1:
                    print "You cannot place a bet that is below 1"
                else:
                    self.bank -= bet
                    self.bet = bet
                    break
                    
    def clearBet(self):
        self.bet = 0
    
    def resetHand(self):
        del self.hand['cards'][:]
        self.hand['containsAce'] = False
        self.hand['busted'] = False
        self.hand['points']['ace'] = 0
        self.hand['points']['normal']=0
        self.clearBet()
        self.win = False
        
    def collectWins(self, winnings):
        self.bank += winnings
        
    def action(self, action):
        return action == True
    def checkHand(self):
        if len(self.hand['cards'])>0:
            for card in self.hand['cards']:
                print str(card.number) + ' '+ card.suit


# In[ ]:


class Card(object):
    def __init__ (self, hierarchy,suit, number):
        self.hierarchy = hierarchy
        self.suit = suit
        self.number = number
        


# In[ ]:


class Deck(object):
    def __init__ (self, deck=[], removedDeck=[]):
        self.deck = deck
        self.removedDeck = removedDeck
        
    def initDeck(self):
        del self.deck[:]
        del self.removedDeck[:]
        
        for x in xrange(1,5):
            for num in xrange(1,14):
                if x == 1:
                    card = Card(x,'Cloves',num)            
                elif x == 2:
                    card = Card(x,'Diamonds',num)
                elif x == 3:
                    card = Card(x,'Hearts', num)
                elif x == 4:
                    card = Card(x,'Spades',num)
                self.deck.append(card)
                
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def removeCard(self):
        self.checkForReShuffling()
        return self.deck.pop(random.randint(0,(len(self.deck)-1)))
    
    def recordDiscardedCard(self, player):
        for card in player.hand['cards']:
            self.removedDeck.append(card)
        player.resetHand()
        
    def __len__(self):
        return len(self.deck)
    
    def checkForReShuffling(self):
        if len(self.deck)<=21:
            print 'Current deck contains less than 20 cards, \nremoved cards will be added back to deck and deck will be reshuffled'
            for card in self.removedDeck:
                self.deck.append(self.removedDeck.pop())
                self.shuffleDeck()


# In[ ]:


class Dealer(Player):
    def __init__(self,hand):
        Player.__init__(self,hand, 'Dealer')
    def dealCard(self, deck):
        return deck.removeCard()
    
    def shuffleDeck(self, deck):
        deck.shuffleDeck()



# In[ ]:


def dealerAction(dealer,deck):
    global player
    points = 0
    if checkForBlackJack(dealer):
        return
    try:
         while True:
                if player.hand['busted']:
                    dealer.win = True
                    break
                if dealer.hand['busted']:
                    print 'The dealer had busted!'
                    break
                elif dealer.hand['containsAce']:
                    if (dealer.hand['points']['ace']>=17) & (dealer.hand['points']['normal']>=17):
                        dealer.hand['busted'] = True
                        break
                    elif (dealer.hand['points']['normal']>=17):
                        break
                    else:
                        dealer.addCard(dealer.dealCard(deck))
                        if dealer.hand['containsAce']:
                            print "Dealer's points with Ace as 11: "+ str(dealer.hand['points']['ace'])
                        dealer.checkHand()
                        print "Dealer's points"+ str(dealer.hand['points']['normal']) 
                elif dealer.hand['points']['normal']>=17:
                    break
                else:
                    dealer.addCard(dealer.dealCard(deck))
                    if dealer.hand['containsAce']:
                        print "Dealer's points with Ace as 11: "+ str(dealer.hand['points']['ace'])
                    dealer.checkHand()
                    print "Dealer's points"+ str(dealer.hand['points']['normal'])
    except Exception as inst:
        print str(Exception) 


# In[ ]:


def playerAction(player, deck, dealer):
    acceptInsurance = False
    
    if player.bet == 0:
        player.placeBet()        
    
    if checkForBlackJack(player):
        return
    
    print "Dealer's first card: "+ dealer.hand['cards'][0].suit+' '+ str(dealer.hand['cards'][0].number)
    
    if dealer.hand['cards'][0].number == 1:
        print "dealer's first card is Ace!"
        askForInsurance(player)
        if checkForBlackJack(dealer):
            return        
    print 'Your current hand: '
    player.checkHand()
    while True:
        if player.hand['busted']:
            print "Your hand had busted."
            break
        else:
            choice = askForInput()
            if choice.upper() == 'H':
                card = dealer.dealCard(deck)
                print 'dealed card: '+ str(card.number)+' '+ card.suit
                player.addCard(card)
                print 'Your current hand:'
                player.checkHand()
            else:
                break                     


# In[ ]:


def askForInsurance(player):
    global insuranceBet,placeInsurance
    while True:
        choice = raw_input("Enter 'Y' to place insurance or 'N' to pass")
        if choice.upper() == 'Y':
            placeInsurance = True
            break
        elif choice.upper() =='N':
            placeInsurance = False
            break
        else:
            placeInsurace = False
            print 'Please enter a valid input.'
    if placeInsurance:
        while True:
            if player.bet < 1:
                print "Your bet is 1, can't place insurance"
                break
            elif player.bank ==0:
                print "You don't have money to place an insurance"
                break
            try:
                insuranceBet = int(raw_input("Your bet: %d. Please place an insurance: "%player.bet))
            except:
                print 'Please place a valid bet.'
            else:
                if insuranceBet > player.bank:
                    print 'You have insufficient funds'
                elif insuranceBet > (player.bet*0.5):
                    print 'You cannot bet higher than 1/2 of your original bet.'
                else:
                    break
    return placeInsurance


# In[ ]:


def askForInput():
    while True:
        choice = raw_input("Enter 'H' to Hit or 'S' to Stand")
        if choice.upper() == 'H' or choice.upper() == 'S':
            break
        else: print 'Please enter a valid input.'
    return choice


# In[ ]:


def checkForBlackJack(player):
    blackJack = False
    if (len(player.hand['cards']) == 2) & (player.hand['points']['ace'] == 21):
        blackJack = True
    return blackJack


# In[ ]:


def declareWinner(player, dealer):
    global placeInsurance, insuranceBet, deck
    playerPoint = 0
    dealerPoint = 0
    
    if checkForBlackJack(player) & checkForBlackJack(dealer):
        print 'Draw Game!'
        player.collectWins(player.bet)
        
    elif checkForBlackJack(player):
        print 'Black Jack for ' + player.name+'!'
        player.win = True
        playerPoint = 21
        player.collectWins(player.bet*2.5)
        
    elif checkForBlackJack(dealer):
        print 'Black Jack for Dealer!'
        dealer.win = False
        dealerPoint = 21
        if placeInsurance:
            player.collectWins(insuranceBet*2+insuranceBet)
            
    else:
        if player.hand['busted']:
            dealer.win = True
            player.win = False
        else:
            playerPoint = returnHigherPoint(player)
            
        if dealer.hand['busted']:
            dealer.win = False
            player.win = True
            
        else:
            dealerPoint = returnHigherPoint(dealer)
        
        if playerPoint > dealerPoint:
            player.win = True
            
        elif playerPoint < dealerPoint:
            dealer.win = True
    print "Dealer's Hand:"
    dealer.checkHand()
    print "Dealer's Point: " + str(dealerPoint)
    print player.name+"'s Hand:"
    player.checkHand()
    print player.name+"'s Point: " + str(playerPoint)
    
    if player.win:
        print player.name+' Wins!'+player.name+"'s winnings: "+ str(player.bet*2)
        player.collectWins(player.bet*2)
    elif dealer.win:
        print 'Dealer Wins!'
    elif playerPoint == dealerPoint:
        print 'Draw Game!'
        player.collectWins(player.bet)
        
       
    deck.recordDiscardedCard(player)
    deck.recordDiscardedCard(dealer)


# In[ ]:


def returnHigherPoint(player):
    if player.hand['containsAce']:
        if (player.hand['points']['ace']<21) & (player.hand['points']['ace'] > player.hand['points']['normal']):
            return player.hand['points']['ace']
        else:
            return player.hand['points']['normal']
    else:
        return player.hand['points']['normal']


# In[ ]:


def showPlayerStats():
    global player
    print 'Your bank: '+ str(player.bank)


# In[ ]:


def newRound(player, dealer, deck):
    deck.recordDiscardedCard(player)
    deck.recordDiscardedCard(dealer)
    deck.checkForReShuffling()
    player.bet = 0
    insuranceBet = 0
    placeInsurance = False
    player.win = False
    dealer.win = False
    if player.bank ==0:
        print "You've gone bankrupt, adding 100 to your bank!"
        player.bank+= 100


# In[ ]:


def askForPlayerName():
    while True:
        name = raw_input('Please enter your name: ')
        if len(name.replace(' ',''))>0:
            return name
        else:
            print 'Please enter a valid name'


# In[ ]:


def dealCard(dealer, player, deck):
    player.addCard(dealer.dealCard(deck))    


# In[ ]:


def initGame():
    global player, dealer, deck
    print "Welcome to Fk's Black Jack Game!"
    choice = 'O'
    while True:
        choice = raw_input("Enter 'Y' to play or 'N' to leave")      
        if (choice.upper() != 'Y') and (choice.upper() != 'N'):
            print 'Please enter a valid input.'
        else:
            break
    if choice.upper() == 'N':
        print 'Good Bye!'
        return False
    else:
        deck.initDeck()
        dealer.shuffleDeck(deck)
        player.setName(askForPlayerName())
        #playGame()       
        return True


# In[ ]:


def playGame():   
    global player, dealer, deck
    for x in range (1,3):
        dealCard(dealer, player, deck)
        dealCard(dealer, dealer, deck)
    playerAction(player, deck, dealer)
    dealerAction(dealer, deck)
    declareWinner(player, dealer)
    showPlayerStats()
    if continueGame():
        newRound(player, dealer, deck)
        playGame()
    else:
        print 'Good Bye!'
    


# In[ ]:


def continueGame():
    choice = raw_input("Enter 'Y' if you wish to continue to play, or any key to quit: ")
    if choice.upper() == 'Y':

        return True
    else:
        return False


# In[ ]:


gameInProgress = True
restartGame=True
bust = False
action = {'stand': True, 'hit':False}
quitGame=True
insuranceBet = 0
playerHand ={'cards': [], 'containsAce':False, 'points':{'normal':0,'ace':0},'busted':False}
dealerHand ={'cards': [], 'containsAce':False, 'points':{'normal':0,'ace':0},'busted':False}
placeInsurance = False
dealer = Dealer(dealerHand)
player = Player(playerHand)
deck = Deck()


# In[ ]:


def game():
    if initGame():
        playGame()


# In[ ]:


game()

