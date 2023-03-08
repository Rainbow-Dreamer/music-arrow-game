from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image as PIL_Image
from PIL import ImageTk
import time
import random
from copy import deepcopy as copy
import os, sys
import pygame
import mido_fix
from ast import literal_eval
import chunk
import dataclasses

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
sys.path.append('scripts')
with open('scripts/musicpy/__init__.py', encoding='utf-8') as f:
    exec(f.read())
with open('scripts/music arrow game.pyw') as f:
    exec(f.read())