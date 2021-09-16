#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np


# In[6]:


np.random.choice(5,5,replace=True)


# In[7]:


class BagLearner(object):
    
    def __init__(self,learner, kwargs = {"argument1":1, "argument2":2}, bags = 20, boost = False, verbose=False):
        self.learner = learner
        self.bags=bags
        slef.kwargs=kwargs
        
    
        self.learners=[]
        
        
        for i in range(0,bags):
            
            if kwargs=={}:
                self.learners.append(learner(verbose))
            
            elif 'leaf_size' in kwargs:
                self.learners.append(learner(leaf_size=kwargs['leaf_size']))
            
            else:
                self.learners.append(learner())
            
    def add_evidence(Xtrain,Ytrain):
        
        self.models = []
        for learner in self.learners:
            
            RowNum = Xtrain.shape[0]
            Row = np.random.choice(RowNum, size=RowNum,replace=True)
            learner.add_evidence(Xtrain[Row],Ytrain[Row])
            self.models.append(learner)
            
    def query(self,Xtest):
        
        result = np.zeros(Xtest.shape[0],1)
        for l in self.models:
            y=l.query(Xtest)
            result = np.column_stack((result, y))

        result = result[: , 1: ]

        return np.mean(result, axis=1)
        


# In[ ]:




