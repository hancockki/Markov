from PIL import Image
import numpy as np, numpy.random
import pyprind
import random
import os
import pygame
from collections import defaultdict, Counter
import xlrd
from django.shortcuts import render
import collage


class MarkovChain(object):
    def __init__(self, num_postures, states_info, states_list, transition_matrix, restorative=False):
        self.num_postures = num_postures
        self.restorative = restorative
        self.states_list = states_list
        self.states_info = states_info
        self.transition_matrix = np.atleast_2d(transition_matrix)
        self.index_dict = {self.states_list[index]: index for index in 
                           range(len(self.states_list))}
        print(self.index_dict)

    """
    Returns the next pose in the class in the markov chain
    """
    def next_state(self, current_state, a, p):
        return np.random.choice(a, p=p)
        #return np.random.choice(
         #self.states_list, 
         #p=self.transition_matrix[self.index_dict[current_state], :]
        #)
    
    """
        Generates the next states of the system, based on the type of class
 
        Parameters
        ----------
        current_state: str
            The state of the current random variable, aka which pose we start with
 
        no: int
            The number of future states to generate.
        """
    def generate_states(self, current_state, no=10):
        future_states = []
        if self.restorative:
            category = 'difficulty'
            pose_type = 'easy'
        for i in range(self.num_postures):
            specific_states_list, specific_tranisition_matrix = self.get_search_space(pose_type, current_state, category)
            print("STATEs LIST:", specific_states_list, "TRANSITION MATRIX", specific_tranisition_matrix)
            next_state = self.next_state(current_state, specific_states_list, specific_tranisition_matrix)
            future_states.append(next_state)
            current_state = next_state
        return future_states

    """
    This function gets the transition matrix and postures to choose in our markov chain
    """
    def get_search_space(self, pose_type, current_state, category):
        specific_states_list = []
        specific_tranisition_matrix = []
        for i in self.states_list:
            if pose_type in self.states_info[i][category]:
                specific_states_list.append(i)
                print("element to add\n", self.transition_matrix[self.index_dict[current_state]][self.index_dict[i]])
                specific_tranisition_matrix.append(self.transition_matrix[self.index_dict[current_state]][self.index_dict[i]])
        
        temp_trans_matrix = self.create_temp_transition_matrix(len(specific_tranisition_matrix))
        return specific_states_list, temp_trans_matrix

    """
    This function creates the transition matrix for the subset of poses we are choosing from
    """
    def create_temp_transition_matrix(self, num_states, filename=''):
        #transition_matrix = [np.random.dirichlet(np.ones(5), size=1) for _ in range(5)]
        #print(transition_matrix, transition_matrix[0])
        nums = []
        sums=0
        for i in range(num_states):
            val = random.random()
            nums.append(val)
            sums += val
        for i in range(num_states):
            nums[i] = nums[i] / sums
        print(nums)
        return nums

"""
Reads in the excel file to create the data structure for our poses

"""
def create_states(filename):
    asanas = xlrd.open_workbook('asana_master_list.xlsx')
    asana_list = asanas.sheet_by_index(0)
    num_cols, num_rows = asana_list.ncols, asana_list.nrows
    #print(num_rows)
    states_info = {}
    for row in range(1,num_rows):
        asana = asana_list.cell(row, 0).value.lower()
        states_info[asana] = {}
        for col in range(1, num_cols):
            cell_obj = asana_list.cell(row, col).value.lower()
            cell_type = asana_list.cell(0, col).value.lower()
            states_info[asana][cell_type] = cell_obj
    
    states_list = asana_list.col_values(0)[1:]
    for i in range(len(states_list)):
        lower = states_list[i].lower()
        states_list[i] = lower
    #print(states_list)
    return states_info, states_list
"""
Creates the transition matrix based off (hopefully) large amounts of data
"""
def create_transition_matrix(num_states, filename=''):
        #transition_matrix = [np.random.dirichlet(np.ones(5), size=1) for _ in range(5)]
        #print(transition_matrix, transition_matrix[0])
    nums = []
    for i in range(num_states):
        temp = []
        sums = 0
        for i in range(num_states):
            val = random.random()
            temp.append(val)
            sums += val
        for i in range(num_states):
            temp[i] = temp[i] / sums
        nums.append(temp)
        #print(nums)
    return nums

"""
Ask the user what type of class they would like and how many poses

"""
def get_user_input():
    print("What type of class would you like to teach? Choose between the following:\nRestorative, Basic Vinyasa, Power Vinyasa\nType answer below: ")
    class_type = input()
    print("How many postures would you like?\nType answer below:")
    num_postures = input()
    num_postures = int(num_postures)
    return class_type, num_postures

def home(request):
    return render(request, 'Web_App/home.html')

if __name__ == "__main__":
    import sys
    states_info, states_list = create_states('asana_master_list.xlsx')
    class_type, num_postures = get_user_input()
    print(type(num_postures), class_type)
    num_states = len(states_info.keys())
    #print(states_info)
    transition_matrix = create_transition_matrix(num_states)
    chain = MarkovChain(num_postures=num_postures, restorative=True, states_info=states_info, 
                        states_list=states_list, transition_matrix=transition_matrix)
    states = chain.generate_states(current_state='bird of paradise')
    print(states)




