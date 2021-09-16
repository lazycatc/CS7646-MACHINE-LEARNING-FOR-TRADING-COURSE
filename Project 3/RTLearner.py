#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[ ]:


class RTLearner(object):
    def __init__(self, leaf_size =1, verbose=False):  
        self.leaf_size=1

    def author(self):  
        return "tb34" 
    
    def add_evidence(self, data_x, data_y):  
        """  
        Add training data to learner 
        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray   
        :param data_y: The value we are attempting to predict given the X data  		  	   		   	 			  		 			 	 	 		 		 	
        :type data_y: numpy.ndarray
        """  
        if data_x.shpae[0]==1:
            self.tree = np.array([[-1,data_y,-1,-1]])
            return self.tree
        
        if np.isclose(data_y,data_y[0]).all():
            self.tree = np.array(([-1,data_y,-1,-1]))
            return self.tree
        
        if data_x.shpae[0]<=leaf_size:
            self.tree=np.array([[-1,np.mean(data_y),-1,-1]])
            return self.tree
        
        else:
            # determine best feature to split on
            index = np.random.randint(0,data_x.shape[1]-1)
            
            while True:
                
                SplitVal=np.median(data_x[:,index],axis=0) 
                if np.isclose(data_x[:,index],data_x[0,index]).all():
                    iindex = np.random.randint(0,data_x.shape[1]-1)
                    continue

                elif SplitVal >= np.max(data_x[:,index]):
                    SplitVal = (np.max(data_x[:,index])+np.min(data_x[:,index]))/2
                    break
                
                else:
                    break
                    
            lefttree = np.array(self.add_evidence(data_x[data_x[:,index]<= SplitVal],data_y[data_x[:,index]<=SplitVal]))
            righttree = np.array(self.add_evidence(data_x[data_x[:, index] > SplitVal], data_y[data_x[:, index] > SplitVal]))
            
            root = np.array([[index, SplitVal, 1, lefttree.shape[0] + 1]], dtype= float)

            self.tree = np.vstack((root, lefttree))
            self.tree = np.vstack((self.tree, righttree))
            
            return self.tree
       
    
    def query(self, points): 
        
        
        """  
        
        Estimate a set of test points given the model we built. 
        
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		   	 			  		 			 	 	 		 		 	
        :type points: numpy.ndarray  
        :return: The predicted result of the input data according to the trained model  		  	   		   	 			  		 			 	 	 		 		 	
        :rtype: numpy.ndarray  
        """  
        result = []
        tree = np.array(self.tree)
        
        for i in range(0,points.shape[0]):
            j = 0
            
            while tree[j,0] != -1:
                index = tree[j,0]
                SplitVal = tree[j,1]
                if points[i,index] <= SplitVal:
                    j = j+1
                    
                else:
                    j=j+tree[j,3]
                    
            result.append(tree[j,1])
                
        
        
        return result
    
 



    if __name__ == "__main__": 
        print('This is a Random Tree Learner\n')      

