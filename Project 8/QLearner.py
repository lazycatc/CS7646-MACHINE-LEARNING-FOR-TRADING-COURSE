#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import random as rand
from copy import deepcopy

# In[ ]:


'''
num_states integer, the number of states to consider
num_actions integer, the number of actions available.


alpha float, the learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.
gamma float, the discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.
    
    
rar float, random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.
radr float, random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.
    
    
dyna integer, number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.
verbose boolean, if True, your class is allowed to print debugging statements, if False, all printing is prohibited.
'''


# In[3]:


class QLearner(object):
    
    def __init__(self,num_states=100,num_actions=4,alpha=0.2,gamma=0.9,
                rar=0.5,radr=0.99,dyna=0,verbose=False):
        self.num_states=num_states
        self.num_actions=num_actions
        self.alpha=alpha
        self.gamma=gamma
        self.rar=rar
        self.radr=radr
        self.dyna=dyna
        self.verbose=verbose
        
        self.s=0
        self.a=0
        
        self.Q=np.zeros((num_states,num_actions))
        self.T={}
        self.R=np.zeros((num_states,num_actions))
     
    
    
    def querysetstate(self,s):
        '''
        sets the state to s, and returns an integer action
        '''
        num_actions = self.num_actions
        if rand.uniform(0.0,1.0)<= self.rar:
            action=rand.randint(0,num_actions-1)
        else:
            action=np.argmax(self.Q[s])
            
        self.s=s
        self.a=action
        
        if self.verbose:
            print('s=',s,'a=',action)
        
        return action
        
               
        
    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
                    r + self.gamma * self.Q[s_prime, np.argmax(self.Q[s_prime])])
        
        

        """dyna implementation"""
        if self.dyna>0:
            self.R[self.s,self.a]=(1-self.alpha)*self.R[self.s,self.a]+self.alpha*r
            if (self.s,self.a) in self.T:
                if s_prime in self.T[(self.s,self.a)]:
                    self.T[(self.s,self.a)][s_prime]+=1
                else:
                    self.T[(self.s,self.a)][s_prime] = 1
        else:
            self.T[(self.s,self.a)]={s_prime:1}
            
        
        Q=deepcopy(self.Q)
        for i in range(0,self.dyna-1):
            s=rand.randint(0,num_states-1)
            a=rand.randint(0,num_actions-1)
            if (s,a) in self.T:
                s_pr = max(self.T[(s,a)],key=lambda k:self.T[(s,a)][k])
                Q[s, a] = (1 - self.alpha) * Q[s, a]                                 + self.alpha * (self.R[s, a] + self.gamma 
                                * Q[s_pr, Q[s_pr, :].argmax()])
            # Update the Q table of the learner once Dyna-Q is complete
            self.Q = deepcopy(Q)
        
        # Find the next action to take and update the latest state and action
        a_prime = self.querysetstate(s_prime)
        self.rar *= self.radr
        if self.verbose: 
            print ("s =", s_prime,"a =",a_prime,"r =",r)
        return a_prime    


# In[4]:


if __name__=='__main__':
    print('Remember Q from Star Trek? Well, this is not him')


# In[ ]:




