import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def plot_best_action(Q_s_a, action, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(1, 11)
    y = np.arange(1, 22)
    x, y = np.meshgrid(x, y)
    
    z = np.zeros((21,10))
    for i in range(len(Q_s_a)):
        for j in range(len(Q_s_a[i])):
            z[i][j]=Q_s_a[i][j][action]
            
    
    ax.plot_surface(x, y, z, cmap=cm.coolwarm)
    ax.set_xlabel('Dealer showing')
    ax.set_ylabel('Player sum')
    ax.set_zlabel('Value')
    ax.set_title('Value function of: ' + title)
    
    fig.savefig(str('images/' + title + '.png'))
    
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
        self.terminate=False
        
        self.myCards= cards()
        self.dealerCards = cards()
        self.myCards.initial_deal()
        self.dealerCards.initial_deal()
        
        
        while self.terminate==False:
            self.action()
        
        self.finish()
    def update(self,action):
        self.state.append([self.myCards.sum, self.dealerCards.numbers[0], action])
        
        return
    
    
    def action(self):
        
        
        #
        # action = int(input("What is your next move? Hit(0) or Stick(1)"))
        action = agent.choose_action([self.myCards.sum, self.dealerCards.numbers[0]])
                
        self.update(action)
        self.step(action)

        return
    
    def step(self, action):
    #game environment
    #decide dealers next move and next state for game0
    
    #action
        if action==0:
            self.myCards.deal()
            if self.myCards.sum>21 or self.myCards.sum<1:
                self.terminate=True
                self.reward=-1
                
                return
        else:
            while 0<self.dealerCards.sum<17:
                self.dealerCards.deal()
                
        if self.dealerCards.sum>21 or self.dealerCards.sum<1:
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
        print("States are: ", self.state)
        print("Reward is: ", self.reward)
        return
    
class monte_carlo():
    def __init__(self):
        
        #For the following: rows are dealers first card, columns are sum of players cards, element 0 is hit, 1 is stick
        self.N_s=np.zeros((21,10))  # Number of times state has been visited
        self.Q_s_a=np.zeros((21,10,2)) # Value of each action in each state
        self.N_s_a=np.zeros((21,10,2)) # Number of times action has been taken in each state
        
        
        self.policy="epsilon_greedy"
        
        return
    def choose_action(self,state):
        
        #Choose action based on policy
        if self.policy=="greedy":
            return self.greedy(state)
        elif self.policy=="epsilon_greedy":
            return self.epsilon_greedy(state)
        
        return 
    
    def calc_epsilon(self, no_visits):
        
        #Calculate the epsilon value - dictates the exploration
        #epsilon=100/(100+N(s))
        self.epsilon=100/(100+no_visits)
        return
    
    def greedy(self,state):
        
        #Get action values
        action_values=self.Q_s_a[state[0]-1][state[1]-1]
        
        #Choose action with highest action value
        if action_values[0]==action_values[1]: #If both actions have the same value, choose randomly
            action=random.randint(0, 1)
        else:
            action=np.argmax(action_values)
        print("Action is: ", action)
        return action
    
    def epsilon_greedy(self,state):
        #Choose action with highest value
        action=np.argmax(self.Q_s_a[state[0]-1][state[1]-1])
        self.calc_epsilon(self.N_s[state[0]-1][state[1]-1])
        #Choose random action with probability epsilon
        if random.uniform(0, 1)<self.epsilon:
            action=random.randint(0, 1)
        
        return action
    def end_episode(self):
        
        for state in thisGame.state:
            
            #Get state and action values
            # p_sum=state[0]
            # d_card=state[1]
            # action=state[2]
            [p_sum, d_card, action]=state
                        
            #Update number of times action has been taken
            if action==0:
                self.update_value(p_sum,d_card,0)
            else:
                self.update_value(p_sum,d_card,1)
            
            
        return    

        
    def update_value(self,p_sum,d_card,action):
        
        #increment times in state
        self.N_s[p_sum-1][d_card-1]+=1
        #increment times action selected
        self.N_s_a[p_sum-1][d_card-1][action]+=1
        
        #a_t=1/N(s_t,a_t)
        step_size=1/self.N_s_a[p_sum-1][d_card-1][action]

        #V(S_t_a)<-V(S_t_a)+1/N(S_t)*(G_t-V(S_t_a))
        self.Q_s_a[p_sum-1][d_card-1][action]=self.Q_s_a[p_sum-1][d_card-1][action]+step_size*(thisGame.reward-self.Q_s_a[p_sum-1][d_card-1][action])
        
        
        
        return
        

agent= monte_carlo()
for i in range(10):
    for j in range(10000):
        thisGame= game()
        agent.end_episode()

    hit_title='Hit VF, ' +'run' +str((i+1)*10000)
    stick_title='Stick VF, ' +'run' +str((i+1)*10000)
    plot_best_action(agent.Q_s_a,0,hit_title)
    plot_best_action(agent.Q_s_a,1,stick_title)



np.save("Q_s_a", agent.Q_s_a)
np.save("N_s", agent.N_s)
np.save("N_s_a", agent.N_s_a)



#next state is dealers first card plus the sum of the players cards
