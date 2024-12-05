import random
from numpy import zeros
#hello
class cards():
    def __init__(self):
        self.numbers =[]
        self.colours =[]
        self.sum = 0
        
    def initial_deal(self):
        #deal 
        number = int(random.uniform(1, 11))
        
        card="black"
        self.numbers.append(number)
        self.colours.append(card)
        
        self.calc_sum()
        return 
    
    def deal(self):
        #deal 
        number = int(random.uniform(1, 11))
        colour = int(random.uniform(0, 3))
        
        if colour == 0:
            card = "red"
        else:
            card = "black"
        
        self.numbers.append(number)
        self.colours.append(card)
        
        self.calc_sum()
        return

    def calc_sum(self):
        #sum the card numbers, black cards get added, red cards get subtracted
        self.sum=0
        for i in range(len(self.numbers)):
            if self.colours[i] == "black":
                self.sum += self.numbers[i]
            else:
                self.sum -= self.numbers[i]
        
class game():
    def __init__(self):
        #State consists of dealers first card, my cards sum    
        self.state = []
        self.reward=0
        self.actions=[]
        self.terminate=False
        
        self.myCards= cards()
        self.dealerCards = cards()
        self.myCards.initial_deal()
        self.dealerCards.initial_deal()
        self.update()
        
        
        while self.terminate==False:
            self.action()
        
        self.finish()
    def update(self):
        self.state = [self.myCards.sum, self.dealerCards.numbers[0]]
        return
    
    
    def action(self):
        print("---------------------------------")
        print("Your cards are: ", self.myCards.numbers)
        print("Your card colours are: ", self.myCards.colours)
        print("The dealers card is: ", self.dealerCards.numbers[0])
        print("The current sum of your cards is: ", self.myCards.sum)
        
        action = int(input("What is your next move? Hit(0) or Stick(1)"))
        
        while action!=0 and action!=1:
            print("Please enter a valid action")
            action = int(input("What is your next move? Hit(0) or Stick(1)"))
        if action==0:
            action="hit"
        else:
            action="stick"
        
        self.actions.append(action)
        self.step(action)

        return
    
    def step(self, action):
    #game environment
    #decide dealers next move and next state for game0
    
    #action
        if action=="hit":
            self.myCards.deal()
            if self.myCards.sum>21 or self.myCards.sum<1:
                print("You bust, game over")
                self.terminate=True
                self.reward=-1
                
                return
        else:
            while 0<self.dealerCards.sum<17:
                print("Dealer hits")
                self.dealerCards.deal()
                print("Dealers cards are: ", self.dealerCards.numbers)
                
        if self.dealerCards.sum>21 or self.dealerCards.sum<1:
            print("Dealer busts, you win")
            self.terminate=True
            self.reward=1
            return
            #Calculate reward

        #Calculate reward 
        if self.dealerCards.sum>=17:
            self.terminate=True
            if  self.myCards.sum>self.dealerCards.sum:
                self.reward=1
            elif self.myCards.sum==self.dealerCards.sum:
                self.reward=0
            else:
                self.reward=-1
        return 
    def finish(self):
        print("---------------------------------")
        print("The dealers cards are: ", self.dealerCards.numbers)
        print("The dealers card colours are: ", self.dealerCards.colours)
        print("The dealers sum is: ", self.dealerCards.sum)
        print("---------------------------------")
        print("Your cards are: ", self.myCards.numbers)
        print("Your card colours are: ", self.myCards.colours)
        print("Your sum is: ", self.myCards.sum)
        print("---------------------------------")
        print("The reward is: ", self.reward)
        return
    
    
    
#Game structure


thisGame= game()




#next state is dealers first card plus the sum of the players cards
