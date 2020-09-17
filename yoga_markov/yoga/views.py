from django.shortcuts import render
from PIL import Image
import numpy as np, numpy.random
import pyprind
import random
import os
import pygame
from collections import defaultdict, Counter
import xlrd
from django.shortcuts import render
from .models import MarkovChain



def index(request):
    chain = MarkovChain()

    #states_info, states_list = chain.create_states('asana_master_list.xlsx')
    #class_type, num_postures = chain.get_user_input()
    #print(type(num_postures), class_type)
    #num_states = len(states_info.keys())
    #print(states_info)
    #transition_matrix = chain.create_transition_matrix(num_states)

    states, image_png = chain.generate_states(current_state='child pose')
    #images = ['bridge_pose.jpg', 'camel_pose.png','cat_cow_pose.png','balancing_table_pose.png', 'boat_pose.png', 'breathe_retention.png']
    #names = ['bridge pose', 'camel pose', 'cat cow pose', 'balancing table pose', 'boat_pose', 'breathe retention']
    information = {'data': zip(image_png, states)}
    return render(request, 'polls/index1.html', information)