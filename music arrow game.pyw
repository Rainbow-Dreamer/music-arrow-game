from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import random
import keyboard
from copy import deepcopy as cop
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
with open('settings.py', encoding='utf-8-sig') as f:
    exec(f.read())


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


pygame.mixer.init(frequency, sound_size, channel, buffer)
pygame.mixer.set_num_channels(maxinum_channels)
note_sounds = load(notedict, sound_path, sound_format, global_volume)


def play_note(name):
    if name in note_sounds:
        note_sounds[name].play(maxtime=note_play_last_time)


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Music Arrow Game")
        self.minsize(1200, 600)

        style = ttk.Style()
        style.configure('TButton', font=(font_type, font_size))

        self.draw_board()
        self.msg = ttk.Label(self, text='')
        self.msg.place(x=600, y=400)
        self.set_notes()
        self.set_size_button = ttk.Button(self,
                                          text='Change Size',
                                          command=self.set_size)
        self.set_size_button.place(x=0, y=10)
        self.set_size_width_label = ttk.Label(self, text='Width')
        self.set_size_height_label = ttk.Label(self, text='Height')
        self.set_size_width_entry = ttk.Entry(self, width=10)
        self.set_size_width_entry.insert(END, self.block_size[0])
        self.set_size_height_entry = ttk.Entry(self, width=10)
        self.set_size_height_entry.insert(END, self.block_size[1])
        self.set_size_width_label.place(x=100, y=10)
        self.set_size_width_entry.place(x=150, y=10)
        self.set_size_height_label.place(x=250, y=10)
        self.set_size_height_entry.place(x=300, y=10)

        self.set_block_size_button = ttk.Button(self,
                                                text='Change Block Size',
                                                command=self.set_block_size)
        self.set_block_size_button.place(x=420, y=10)
        self.set_block_size_width_label = ttk.Label(self, text='Width')
        self.set_block_size_height_label = ttk.Label(self, text='Height')
        self.set_block_size_width_entry = ttk.Entry(self, width=10)
        self.set_block_size_width_entry.insert(END, self.unit_size[0])
        self.set_block_size_height_entry = ttk.Entry(self, width=10)
        self.set_block_size_height_entry.insert(END, self.unit_size[1])
        self.set_block_size_width_label.place(x=550, y=10)
        self.set_block_size_width_entry.place(x=600, y=10)
        self.set_block_size_height_label.place(x=700, y=10)
        self.set_block_size_height_entry.place(x=750, y=10)

        self.set_chord_type = ttk.Button(self,
                                         text='Change Chord Type',
                                         command=self.change_chord_type)
        self.set_chord_type_label = ttk.Label(self, text='Chord Type')
        self.set_chord_type_entry = ttk.Entry(self, width=10)
        self.set_chord_type_entry.insert(END, self.chord_type)
        self.set_chord_type_label.place(x=600, y=200)
        self.set_chord_type_entry.place(x=680, y=200)
        self.set_chord_type.place(x=770, y=200)

        self.set_chord_root = ttk.Button(self,
                                         text='Change Chord Root',
                                         command=self.change_chord_root)
        self.set_chord_root_label = ttk.Label(self, text='Chord Root')
        self.set_chord_root_entry = ttk.Entry(self, width=10)
        self.set_chord_root_entry.insert(END, self.chord_root)
        self.set_chord_root_label.place(x=600, y=150)
        self.set_chord_root_entry.place(x=680, y=150)
        self.set_chord_root.place(x=770, y=150)

        self.set_start_octave = ttk.Button(self,
                                           text='Change Start Octave',
                                           command=self.change_start_octave)
        self.set_start_octave_label = ttk.Label(self, text='Start Octave')
        self.set_start_octave_entry = ttk.Entry(self, width=10)
        self.set_start_octave_entry.insert(END, self.start_octave)
        self.set_start_octave_label.place(x=600, y=250)
        self.set_start_octave_entry.place(x=680, y=250)
        self.set_start_octave.place(x=770, y=250)

        self.set_chord_intervals = ttk.Button(
            self,
            text='Change Chord Intervals',
            command=self.change_chord_intervals)
        self.set_chord_intervals_label = ttk.Label(self,
                                                   text='Chord Intervals')
        self.set_chord_intervals_entry = ttk.Entry(self, width=20)
        self.set_chord_intervals_entry.insert(
            END,
            str(self.chord_intervals) if self.chord_intervals else '')
        self.set_chord_intervals_label.place(x=600, y=300)
        self.set_chord_intervals_entry.place(x=700, y=300)
        self.set_chord_intervals.place(x=850, y=300)

        self.set_move_speed = ttk.Button(self,
                                         text='Change Move Speed',
                                         command=self.change_move_speed)
        self.set_move_speed_label = ttk.Label(self, text='Move Speed')
        self.set_move_speed_entry = ttk.Entry(self, width=10)
        self.set_move_speed_entry.insert(END, move_speed)
        self.set_move_speed_label.place(x=800, y=80)
        self.set_move_speed_entry.place(x=900, y=80)
        self.set_move_speed.place(x=1000, y=80)

        self.right_arrow_img = Image.open('resources/right.png')
        self.right_arrow_img = self.right_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.right_arrow_img = ImageTk.PhotoImage(self.right_arrow_img)

        self.left_arrow_img = Image.open('resources/left.png')
        self.left_arrow_img = self.left_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.left_arrow_img = ImageTk.PhotoImage(self.left_arrow_img)

        self.up_arrow_img = Image.open('resources/up.png')
        self.up_arrow_img = self.up_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.up_arrow_img = ImageTk.PhotoImage(self.up_arrow_img)

        self.down_arrow_img = Image.open('resources/down.png')
        self.down_arrow_img = self.down_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.down_arrow_img = ImageTk.PhotoImage(self.down_arrow_img)

        self.move_img = Image.open('resources/move.png')
        self.move_img = self.move_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.move_img = ImageTk.PhotoImage(self.move_img)

        left_button = ttk.Button(self,
                                 image=self.left_arrow_img,
                                 command=lambda: self.set_arrow('left'))
        right_button = ttk.Button(self,
                                  image=self.right_arrow_img,
                                  command=lambda: self.set_arrow('right'))
        up_button = ttk.Button(self,
                               image=self.up_arrow_img,
                               command=lambda: self.set_arrow('up'))
        down_button = ttk.Button(self,
                                 image=self.down_arrow_img,
                                 command=lambda: self.set_arrow('down'))
        left_button.place(x=950, y=200)
        right_button.place(x=1030, y=200)
        up_button.place(x=990, y=160)
        down_button.place(x=990, y=240)

        self.current_focus = 0, 0

        clear_button = ttk.Button(self,
                                  text='Clear',
                                  command=self.clear_current_block)
        clear_all_button = ttk.Button(self,
                                      text='Reset All Arrows',
                                      command=self.reset_all_blocks)
        clear_button.place(x=1080, y=200)
        clear_all_button.place(x=1080, y=250)

        self.first_set_block = 0, 0
        self.first_set = True

        start_button = ttk.Button(self, text='Start', command=self.start)
        start_button.place(x=600, y=80)

        self.start_moving = False
        self.move_speed = move_speed
        self.stop = False

        self.stop_button = ttk.Button(self,
                                      text='Stop',
                                      command=self.stop_move)
        self.stop_button.place(x=700, y=80)

        self.place_arrow = False
        self.place_arrow_button = ttk.Button(self,
                                             text='Normal Mode',
                                             command=self.change_mode)
        self.place_arrow_button.place(x=1080, y=300)

    def change_mode(self):
        if not self.place_arrow:
            self.place_arrow = True
            self.place_arrow_button.configure(text='Place Arrow Mode')
        else:
            self.place_arrow = False
            self.place_arrow_button.configure(text='Normal Mode')

    def stop_move(self):
        if self.start_moving:
            self.stop = True

    def start(self, first=True):
        if self.stop:
            self.stop = False
            self.start_moving = False
            self.reset_arrow_img(*self.current_place)
            return
        if first:

            current_block = self.blocks[self.first_set_block[0]][
                self.first_set_block[1]]
            self.msg.configure(text='')
            if current_block.direction == 'none':
                self.msg.configure(text='There are no arrows are set now')
                return
            else:
                if not self.start_moving:
                    self.start_moving = True
                else:
                    return
                self.current_place = self.first_set_block
                self.current_direction = current_block.direction
                self.blocks[self.current_place[0]][
                    self.current_place[1]].configure(image=self.move_img)
                self.play_current_note_move(*self.current_place)
                self.after(self.move_speed, lambda: self.start(False))
        else:
            self.reset_arrow_img(*self.current_place)
            if self.current_direction == 'left':
                self.current_place = self.current_place[
                    0], self.current_place[1] - 1
                if self.current_place[1] < 0:
                    self.start_moving = False
                    return
            elif self.current_direction == 'right':
                self.current_place = self.current_place[
                    0], self.current_place[1] + 1
                if self.current_place[1] >= len(self.blocks[0]):
                    self.start_moving = False
                    return
            elif self.current_direction == 'up':
                self.current_place = self.current_place[
                    0] - 1, self.current_place[1]
                if self.current_place[0] < 0:
                    self.start_moving = False
                    return
            elif self.current_direction == 'down':
                self.current_place = self.current_place[
                    0] + 1, self.current_place[1]
                if self.current_place[0] >= len(self.blocks):
                    self.start_moving = False
                    return
            self.blocks[self.current_place[0]][
                self.current_place[1]].configure(image=self.move_img)
            self.play_current_note_move(*self.current_place)
            new_direction = self.blocks[self.current_place[0]][
                self.current_place[1]].direction
            if new_direction != 'none':
                self.current_direction = new_direction
            self.after(self.move_speed, lambda: self.start(False))

    def set_arrow(self, mode):
        current_focus = self.current_focus
        current_block = self.blocks[current_focus[0]][current_focus[1]]
        if self.first_set:
            self.first_set = False
            self.first_set_block = current_focus
        if mode == 'left':
            current_block.configure(image=self.left_arrow_img)
            current_block.direction = 'left'
        elif mode == 'right':
            current_block.configure(image=self.right_arrow_img)
            current_block.direction = 'right'
        elif mode == 'up':
            current_block.configure(image=self.up_arrow_img)
            current_block.direction = 'up'
        elif mode == 'down':
            current_block.configure(image=self.down_arrow_img)
            current_block.direction = 'down'
        elif mode == 'none':
            current_block.configure(image=self.block_img)
            current_block.direction = 'none'

    def reset_arrow_img(self, i, j):
        current_block = self.blocks[i][j]
        if current_block.direction == 'left':
            current_block.configure(image=self.left_arrow_img)
        elif current_block.direction == 'right':
            current_block.configure(image=self.right_arrow_img)
        elif current_block.direction == 'up':
            current_block.configure(image=self.up_arrow_img)
        elif current_block.direction == 'down':
            current_block.configure(image=self.down_arrow_img)
        elif current_block.direction == 'none':
            current_block.configure(image=self.block_img)

    def clear_current_block(self):
        current_focus = self.current_focus
        if current_focus == self.first_set_block:
            self.first_set = True
        current_block = self.blocks[current_focus[0]][current_focus[1]]
        current_block.configure(image=self.block_img)
        current_block.direction = 'none'

    def clear_block(self, i, j):
        if (i, j) == self.first_set_block:
            self.first_set = True
        current_block = self.blocks[i][j]
        current_block.configure(image=self.block_img)
        current_block.direction = 'none'

    def reset_all_blocks(self):
        self.first_set = True
        for i in self.blocks:
            for j in i:
                j.configure(image=self.block_img)
                j.direction = 'none'

    def change_move_speed(self):
        self.move_speed = int(self.set_move_speed_entry.get())

    def change_chord_type(self):
        self.msg.configure(text='')
        current_chord_type = self.set_chord_type_entry.get()
        if current_chord_type:
            self.chord_type = current_chord_type
            self.current_chord = C(self.chord_root + self.chord_type)
            if type(self.current_chord) == str:
                if any(i.isdigit() for i in self.chord_root):
                    self.msg.configure(
                        text=
                        'Error: Chord root must be only the name of the note, not including the octave'
                    )
                else:
                    self.msg.configure(text='Error: Chord type is not found')
                return
            self.current_chord_intervals = (
                self.current_chord +
                self.current_chord[1].up(octave)).intervalof(cummulative=False)
            self.current_chord_names = self.current_chord.names()
            self.reset_note()

    def change_chord_root(self):
        self.msg.configure(text='')
        current_chord_root = self.set_chord_root_entry.get()
        if current_chord_root:
            if current_chord_root not in standard2:
                if current_chord_root not in standard_dict:
                    self.msg.configure(
                        text='Error: Chord root is not a valid note name')
                    return
                current_chord_root = standard_dict[current_chord_root]
            self.chord_root = current_chord_root
            self.current_chord = C(self.chord_root + self.chord_type)
            self.current_chord_intervals = (
                self.current_chord +
                self.current_chord[1].up(octave)).intervalof(cummulative=False)
            self.current_chord_names = self.current_chord.names()
            self.reset_note()

    def change_start_octave(self):
        current_start_octave = int(self.set_start_octave_entry.get())
        self.start_octave = current_start_octave
        self.reset_note()

    def change_chord_intervals(self):
        current_chord_intervals = self.set_chord_intervals_entry.get()
        if not current_chord_intervals:
            self.chord_intervals = None
        else:
            self.chord_intervals = literal_eval(current_chord_intervals)
        if self.chord_intervals is not None:
            self.current_chord = getchord_by_interval(self.chord_root,
                                                      self.chord_intervals,
                                                      cummulative=False)
        else:
            self.current_chord = C(chord_root + chord_type)
        self.current_chord_intervals = (
            self.current_chord +
            self.current_chord[1].up(octave)).intervalof(cummulative=False)
        self.current_chord_names = self.current_chord.names()
        self.reset_note()

    def draw_board(self):
        self.block_size = size
        self.board = ttk.LabelFrame(width=600, height=500)
        self.block_img = Image.open('resources/block.png')
        self.unit_size = unit_size
        self.block_img = self.block_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.block_img = ImageTk.PhotoImage(self.block_img)
        self.block_width = self.block_img.width
        self.blocks = []
        self.board.place(x=0, y=50)
        for i in range(self.block_size[1]):
            current_row = []
            for j in range(self.block_size[0]):
                current_block = ttk.Button(
                    self.board,
                    image=self.block_img,
                    width=self.block_width,
                    command=lambda i=i, j=j: self.play_current_note(i, j))
                current_block.direction = 'none'
                current_block.bind('<Button-3>',
                                   lambda e, i=i, j=j: self.clear_block(i, j))
                current_block.grid(row=i, column=j)
                current_row.append(current_block)
            self.blocks.append(current_row)

    def set_notes(self):
        global chord_root

        self.chord_type = chord_type
        self.chord_root = chord_root
        self.start_octave = start_octave
        self.chord_intervals = chord_intervals

        if chord_root not in standard2:
            if chord_root not in standard_dict:
                self.msg.configure(
                    text='Error: Chord root is not a valid note name')
                return
            chord_root = standard_dict[chord_root]
        self.chord_root = chord_root
        if chord_intervals is not None:
            current_chord = getchord_by_interval(chord_root,
                                                 chord_intervals,
                                                 cummulative=False)
        else:
            current_chord = C(chord_root + chord_type)

        self.current_chord = current_chord

        if type(current_chord) == str:
            if any(i.isdigit() for i in chord_root):
                self.msg.configure(
                    text=
                    'Error: Chord root must be only the name of the note, not including the octave'
                )
            else:
                self.msg.configure(text='Error: Chord type is not found')
            return
        current_chord_intervals = (current_chord +
                                   current_chord[1].up(octave)).intervalof(
                                       cummulative=False)
        current_chord_names = current_chord.names()
        self.current_chord_intervals = current_chord_intervals
        self.current_chord_names = current_chord_names

        counter = 0
        start_note = note(self.current_chord[1].name, self.start_octave)
        for i in range(self.block_size[1]):
            current_block = self.blocks[i][0]
            if i == 0:
                current_note = start_note
            else:
                current_note = current_note.up(
                    self.current_chord_intervals[counter - 1])
            current_block.configure(text=str(current_note), compound=CENTER)
            current_block.note = current_note
            counter += 1
            if counter >= len(self.current_chord_names):
                counter = 0

        for i in range(self.block_size[1]):
            start_note = self.blocks[i][0].note
            counter = self.current_chord_names.index(start_note.name)
            current_note = start_note
            for j in range(1, self.block_size[0]):
                current_block = self.blocks[i][j]
                current_note = current_note.up(
                    self.current_chord_intervals[counter])
                current_block.configure(text=str(current_note),
                                        compound=CENTER)
                current_block.note = current_note
                counter += 1
                if counter >= len(self.current_chord_names):
                    counter = 0

    def reset_note(self):
        counter = 0
        start_note = note(self.current_chord[1].name, self.start_octave)
        for i in range(self.block_size[1]):
            current_block = self.blocks[i][0]
            if i == 0:
                current_note = start_note
            else:
                current_note = current_note.up(
                    self.current_chord_intervals[counter - 1])
            current_block.configure(text=str(current_note), compound=CENTER)
            current_block.note = current_note
            counter += 1
            if counter >= len(self.current_chord_names):
                counter = 0

        for i in range(self.block_size[1]):
            start_note = self.blocks[i][0].note
            counter = self.current_chord_names.index(start_note.name)
            current_note = start_note
            for j in range(1, self.block_size[0]):
                current_block = self.blocks[i][j]
                current_note = current_note.up(
                    self.current_chord_intervals[counter])
                current_block.configure(text=str(current_note),
                                        compound=CENTER)
                current_block.note = current_note
                counter += 1
                if counter >= len(self.current_chord_names):
                    counter = 0

    def play_current_note(self, i, j):
        self.current_focus = i, j
        current_block = self.blocks[i][j]
        play_note(str(current_block.note))
        if self.place_arrow:
            if current_block.direction == 'none':
                self.set_arrow('left')
            elif current_block.direction == 'left':
                self.set_arrow('up')
            elif current_block.direction == 'up':
                self.set_arrow('right')
            elif current_block.direction == 'right':
                self.set_arrow('down')
            elif current_block.direction == 'down':
                self.set_arrow('left')

    def play_current_note_move(self, i, j):
        current_block = self.blocks[i][j]
        play_note(str(current_block.note))

    def set_size(self):
        self.block_size = int(self.set_size_width_entry.get()), int(
            self.set_size_height_entry.get())
        self.board.destroy()
        self.board = ttk.LabelFrame(width=600, height=500)
        self.blocks = []
        self.board.place(x=0, y=50)
        for i in range(self.block_size[1]):
            current_row = []
            for j in range(self.block_size[0]):
                current_block = ttk.Button(
                    self.board,
                    image=self.block_img,
                    width=self.block_width,
                    command=lambda i=i, j=j: self.play_current_note(i, j))
                current_block.direction = 'none'
                current_block.bind('<Button-3>',
                                   lambda e, i=i, j=j: self.clear_block(i, j))
                current_block.grid(row=i, column=j)
                current_row.append(current_block)
            self.blocks.append(current_row)
        self.reset_note()

    def set_block_size(self):
        self.block_img = Image.open('resources/block.png')
        self.unit_size = int(self.set_block_size_width_entry.get()), int(
            self.set_block_size_height_entry.get())
        self.block_img = self.block_img.resize(
            (self.unit_size[0], self.unit_size[1]), Image.ANTIALIAS)
        self.block_img = ImageTk.PhotoImage(self.block_img)
        self.block_width = self.block_img.width
        for i in self.blocks:
            for j in i:
                j.configure(image=self.block_img, width=self.block_width)


root = Root()
root.mainloop()