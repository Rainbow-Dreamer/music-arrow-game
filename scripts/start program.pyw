from tkinter import *
from tkinter import ttk
from PIL import Image as PIL_Image
from PIL import ImageTk
import time
import random
import keyboard
from copy import deepcopy as copy
import os, sys
import pygame
import keyboard
import mido
import midiutil
from musicpy import *
from ast import literal_eval

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
with open('scripts/music arrow game.pyw') as f:
    exec(f.read())