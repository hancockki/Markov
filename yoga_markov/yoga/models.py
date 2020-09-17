from django.db import models
from PIL import Image
import numpy as np, numpy.random
import pyprind
import random
import os
import pygame
from collections import defaultdict, Counter
import xlrd
from django.shortcuts import render
import math

image_png = []
states = []
"""
Define a MarkovChain class, which uses markov chains to create a unique sequence for a yoga class based on input data
The input data is in the asana master list xlsx document, which contains two sheets:

sheet1 --> list of poses with attributes
sheet2 --> list of classes, where each column is a class in order. We use this to calculate the probability of transitioning from one pose to another.

MarkovChain attributes:
    restorative--> whether we want a restorative class. If it is restorative, then we only allow easy poses
    states_info--> each pose is a STATE, and this is a dictionary mapping each state to its diffferent attributes
    states_list--> just a list of all the poses
    class_type--> to find out if the user wants a restorative class
    num_postures--> number of postures the user wants for their class
    index_dict--> useful data structure that maps each pose to its index in the transition matrix
    transition_matrix--> each entry is a number indicating the probability of transitioning from one pose (index of row is starting pose, found through index_dict)
                        to another (index of column is next pose)

"""
class MarkovChain(object):
    def __init__(self, restorative):
        self.restorative = restorative
        self.states_info, self.states_list = self.create_states('/Users/kimhancock/Desktop/Computational_Creativity/Markov/yoga_markov/yoga/asana_master_list.xlsx')
        self.class_type, self.num_postures = self.get_user_input()
        self.index_dict = {self.states_list[index]: index for index in 
                           range(len(self.states_list))}
        #we have to create the transition matrix
        transition_matrix = self.create_transition_matrix2('/Users/kimhancock/Desktop/Computational_Creativity/Markov/yoga_markov/yoga/asana_master_list.xlsx',len(self.states_list))
        self.transition_matrix = np.atleast_2d(transition_matrix)

        print(self.index_dict)

    """
    Returns the next pose in the class in the markov chain

    @params:
        current_state--> state we are in
        a --> list (or sublist) of states
        p --> probabilities for a of transitioning from the current state to every other state
    
    @returns:
        the next state
    """
    def next_state(self, current_state, a, p):
        return np.random.choice(a, p=p)
        #return np.random.choice(
         #self.states_list, 
         #p=self.transition_matrix[self.index_dict[current_state], :]
        #)
    
    """
        Generates the next states of the system, based on the type of class
 
        @params
        current_state--> The state of the current random variable, aka which pose we are on
 
        @returns
            future_states--> list of poses for the class
            image_png--> list of images to be displayed in browser
        """
    def generate_states(self, current_state):
        future_states = []
        #if it's restorative, we want them all to be easy
        if self.restorative:
            category = 'difficulty'
            pose_type = ['easy'*self.num_postures]
        #otherwise, we want to make sure we have both warming and cool down poses
        #FUTURE DELIVERABLE: make this more specific
        else:
            total = self.num_postures
            num_warmup = math.floor(self.num_postures * 0.2) #want 20% of class to be warmups
            warmup = ['warm up'] * num_warmup
            num_cool_down = math.floor(self.num_postures * 0.2) #want 20% of class to be cool down
            cool_down = ['cool down'] * num_cool_down
            rest = total - num_warmup - num_cool_down
            rest_of_poses = ['any'] * rest
            category = 'type'
            pose_type = warmup + rest_of_poses + cool_down #list of pose types in order
            #print(pose_type)
        #loop through to create our sequence
        for i in range(self.num_postures):
            if pose_type[i] == 'any': #we are in the middle of the class so it doesn't matter
                #call next state with the full row for the current state
                next_state = self.next_state(current_state, self.states_list, self.transition_matrix[self.index_dict[current_state], :])
            else:
                #we need to get sublist of easy poses
                specific_states_list, specific_tranisition_matrix = self.get_search_space(pose_type[i], current_state, category)
                #call next state with sublists
                next_state = self.next_state(current_state, specific_states_list, specific_tranisition_matrix)
            #add our next pose to list
            future_states.append(next_state)
            current_state = next_state #increment current state
        image_png = []
        for i in future_states:
            next_pose = i.replace(' ', '_') + ".png"
            image_png.append(next_pose) #image list based on sequence
        return future_states, image_png

    """
    This function gets the transition matrix and postures to choose in our markov chain based on the type of poses we want to choose from

    @params:
        pose_type--> the type of pose we want the next state to be
        current_state--> pose we are on
        category--> basically the dictionary key for the attribute we want, ex. 'difficulty' or 'type'
    
    @returns:
        the sub list of poses and sub list of probabilities to get the next state with
    """
    def get_search_space(self, pose_type, current_state, category):
        specific_states_list = []
        specific_tranisition_matrix = []
        for i in self.states_list:
            if pose_type in self.states_info[i][category]:
                specific_states_list.append(i)
                #print("element to add\n", self.transition_matrix[self.index_dict[current_state]][self.index_dict[i]])
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
        #print(nums)
        return nums

    """
    Reads in the excel file to create the data structure for our poses

    @params:
        filename--> name of file storing our data
    
    @returns:
        states_info--> dictionary mapping each pose to its attributes
        states_list--> list of all poses
    """
    def create_states(self, filename):
        asanas = xlrd.open_workbook(filename)
        asana_list = asanas.sheet_by_index(0)
        num_cols, num_rows = asana_list.ncols, asana_list.nrows
        states_info = {}
        #loop through each row, aka each pose
        for row in range(1,num_rows):
            asana = asana_list.cell(row, 0).value.lower() #pose name
            states_info[asana] = {}
            for col in range(1, num_cols):
                cell_obj = asana_list.cell(row, col).value.lower() #pertains to attributes of that pose, ex. easy or hard
                cell_type = asana_list.cell(0, col).value.lower() #category of attribute, ex. difficulty or type of pose
                states_info[asana][cell_type] = cell_obj
        
        states_list = asana_list.col_values(0)[1:]
        for i in range(len(states_list)): #we want to lowercase everything
            lower = states_list[i].lower()
            states_list[i] = lower
        print(states_list)
        return states_info, states_list


    """
    Here's our markov finally!!

    We need to create the probability of transitioning from any pose to any other pose based on our input data, 
    which is lists of sequences. we do this by adding up the number of times we transition from one pose to another and then dividing by
    the total number of times we transition from any one pose to any other pose

    @params:
        filename--> excel sheet with data
        num_states--> total number of poses

    @returns:
        transition_matrix--> matrix of probabilities
    """
    def create_transition_matrix2(self, filename, num_states):
        asanas = xlrd.open_workbook(filename)
        transition_matrix = []
        #initialize matrix as empty num_states x num_states
        for i in range(num_states):
            temp = []
            for i in range(num_states):
                temp.append(0)
            transition_matrix.append(temp)
        #populate matrix
        asana_classes = asanas.sheet_by_index(1)
        num_classes, num_poses = asana_classes.ncols, asana_classes.nrows
        for col in range(num_classes): #col is next pose
            current_pose = asana_classes.cell(0, col).value.lower() #first pose in sequence
            print(current_pose)
            for row in range(1, num_poses): #row is starting pose
                next_pose = asana_classes.cell(row, col).value.lower()
                if next_pose == '': #end of column
                    continue
                print(next_pose)
                #this gets us to the correct index
                transition_matrix[self.index_dict[current_pose]][self.index_dict[next_pose]] += 1
                current_pose = next_pose #ready to go to our next pose!
        print(transition_matrix)
        for i in range(num_states):
            temp = []
            sums = 0 #want to divide every number in the row by the sum of that row so the row adds up to 1
            for j in range(num_states):
                val = transition_matrix[i][j]
                sums += val
            for j in range(num_states):
                if sums == 0:
                    continue
                transition_matrix[i][j] = transition_matrix[i][j] / sums #calculate probability
        print(transition_matrix)
        return transition_matrix
            

    """
    Creates the transition matrix based off (hopefully) large amounts of data
    """
    def create_transition_matrix(self, num_states, filename=''):
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
    def get_user_input(self):
        print("What type of class would you like to teach? Choose between the following:\nRestorative, Basic Vinyasa, Power Vinyasa\nType answer below: ")
        class_type = input()
        print("How many postures would you like?\nType answer below:")
        num_postures = input()
        num_postures = int(num_postures)
        return class_type, num_postures

"""
def index(request):
    #images = ['bridge_pose.jpg', 'camel_pose.png','cat_cow_pose.png','balancing_table_pose.png', 'boat_pose.png', 'breathe_retention.png']
    #names = ['bridge pose', 'camel pose', 'cat cow pose', 'balancing table pose', 'boat_pose', 'breathe retention']
    print(image_png, states)
    information = {'data': zip(image_png, states)}
    return render(request, 'polls/index1.html', information)


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
    states, image_png = chain.generate_states(current_state='bird of paradise')
"""