with open('scripts/settings.py', encoding='utf-8') as f:
    exec(f.read())


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def play_note(name):
    if name in note_sounds:
        note_sounds[name].play(maxtime=note_play_last_time)


pygame.mixer.init(frequency, sound_size, channel, buffer)
pygame.mixer.set_num_channels(maxinum_channels)
note_sounds = load(notedict, sound_path, sound_format, global_volume)


class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.title("Music Arrow Game")
        self.minsize(1200, 600)

        style = ttk.Style()
        style.configure('TButton', font=(font_type, font_size))

        self.draw_board()
        self.set_notes()
        self.draw_settings_buttons()
        self.load_arrows_imgs()
        self.draw_arrows_buttons()

        self.current_focus = 0, 0

        self.draw_arrows_settings_buttons()

        self.start_moving = False
        self.move_speed = move_speed
        self.stop = False
        self.set_arrows_blocks = []
        self.set_portal = False
        self.set_portal_blocks = None
        self.current_portal_highlight = []

        self.bind_keys()
        self.current_time = time.time()

        self.direction_list = [
            'left', 'left up', 'up', 'right up', 'right', 'right down', 'down',
            'left down'
        ]

    def bind_keys(self):
        self.bind('<Up>', lambda e: self.set_arrow('up', e))
        self.bind('<Down>', lambda e: self.set_arrow('down', e))
        self.bind('<Left>', lambda e: self.set_arrow('left', e))
        self.bind('<Right>', lambda e: self.set_arrow('right', e))
        self.bind('<Left><Up>', lambda e: self.set_arrow('left up', e))
        self.bind('<Up><Left>', lambda e: self.set_arrow('left up', e))
        self.bind('<Right><Up>', lambda e: self.set_arrow('right up', e))
        self.bind('<Up><Right>', lambda e: self.set_arrow('right up', e))
        self.bind('<Left><Down>', lambda e: self.set_arrow('left down', e))
        self.bind('<Down><Left>', lambda e: self.set_arrow('left down', e))
        self.bind('<Right><Down>', lambda e: self.set_arrow('right down', e))
        self.bind('<Down><Right>', lambda e: self.set_arrow('right down', e))
        self.unbind_class('TButton', '<space>')
        self.bind("<Control-space>", lambda e: self.switch_play())
        self.bind("<Control-q>", lambda e: self.set_as_first())
        self.bind("<Tab>", lambda e: self.change_mode())
        self.bind("<Control-e>", lambda e: self.clear_current_block())
        self.bind("<Control-r>", lambda e: self.reset_all_blocks())
        self.bind("<Control-t>", lambda e: self.open_change_settings())
        self.bind('<Button-3>', lambda e: self.cancel_set_portal())

    def cancel_set_portal(self):
        if self.set_portal:
            self.set_portal = False
            if self.set_portal_blocks:
                try:
                    self.clear_block(*self.set_portal_blocks)
                except:
                    pass
                self.set_portal_blocks = None

    def draw_arrows_settings_buttons(self):
        clear_button = ttk.Button(self,
                                  text='Clear',
                                  command=self.clear_current_block)
        clear_all_button = ttk.Button(self,
                                      text='Reset All Arrows',
                                      command=self.reset_all_blocks)
        clear_button.place(x=1080, y=200)
        clear_all_button.place(x=1080, y=250)

        start_button = ttk.Button(self, text='Start', command=self.start)
        start_button.place(x=600, y=80)

        self.stop_button = ttk.Button(self,
                                      text='Stop',
                                      command=self.stop_move)
        self.stop_button.place(x=700, y=80)

        self.place_arrow = False
        self.place_arrow_button = ttk.Button(self,
                                             text='Normal Mode',
                                             command=self.change_mode)
        self.place_arrow_button.place(x=1080, y=300)

    def draw_arrows_buttons(self):
        left_button = ttk.Button(self,
                                 image=self.left_arrow_show_img,
                                 command=lambda: self.set_arrow('left'))
        right_button = ttk.Button(self,
                                  image=self.right_arrow_show_img,
                                  command=lambda: self.set_arrow('right'))
        up_button = ttk.Button(self,
                               image=self.up_arrow_show_img,
                               command=lambda: self.set_arrow('up'))
        down_button = ttk.Button(self,
                                 image=self.down_arrow_show_img,
                                 command=lambda: self.set_arrow('down'))
        left_up_button = ttk.Button(self,
                                    image=self.left_up_arrow_show_img,
                                    command=lambda: self.set_arrow('left up'))
        right_up_button = ttk.Button(
            self,
            image=self.right_up_arrow_show_img,
            command=lambda: self.set_arrow('right up'))
        left_down_button = ttk.Button(
            self,
            image=self.left_down_arrow_show_img,
            command=lambda: self.set_arrow('left down'))
        right_down_button = ttk.Button(
            self,
            image=self.right_down_arrow_show_img,
            command=lambda: self.set_arrow('right down'))
        portal_button = ttk.Button(self,
                                   image=self.portal_in_show_img,
                                   command=lambda: self.set_portal_func())
        left_button.place(x=950, y=200)
        right_button.place(x=1030, y=200)
        up_button.place(x=990, y=160)
        down_button.place(x=990, y=240)
        left_up_button.place(x=950, y=160)
        right_up_button.place(x=1030, y=160)
        left_down_button.place(x=950, y=240)
        right_down_button.place(x=1030, y=240)
        portal_button.place(x=990, y=280)
        self.set_as_first_button = ttk.Button(self,
                                              text='Set As Start Grid',
                                              command=self.set_as_first)
        self.set_as_first_button.place(x=1080, y=350)

    def load_arrows_imgs(self):
        self.right_arrow_img = PIL_Image.open('resources/right.png')
        self.right_arrow_img = self.right_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_arrow_show_img = ImageTk.PhotoImage(
            self.right_arrow_img.copy())
        self.right_arrow_img = ImageTk.PhotoImage(self.right_arrow_img)
        self.right_arrow_first_img = PIL_Image.open(
            'resources/right_first.png')
        self.right_arrow_first_img = self.right_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_arrow_first_img = ImageTk.PhotoImage(
            self.right_arrow_first_img)

        self.left_arrow_img = PIL_Image.open('resources/left.png')
        self.left_arrow_img = self.left_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_arrow_show_img = ImageTk.PhotoImage(
            self.left_arrow_img.copy())
        self.left_arrow_img = ImageTk.PhotoImage(self.left_arrow_img)
        self.left_arrow_first_img = PIL_Image.open('resources/left_first.png')
        self.left_arrow_first_img = self.left_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_arrow_first_img = ImageTk.PhotoImage(
            self.left_arrow_first_img)

        self.up_arrow_img = PIL_Image.open('resources/up.png')
        self.up_arrow_img = self.up_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.up_arrow_show_img = ImageTk.PhotoImage(self.up_arrow_img.copy())
        self.up_arrow_img = ImageTk.PhotoImage(self.up_arrow_img)
        self.up_arrow_first_img = PIL_Image.open('resources/up_first.png')
        self.up_arrow_first_img = self.up_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.up_arrow_first_img = ImageTk.PhotoImage(self.up_arrow_first_img)

        self.down_arrow_img = PIL_Image.open('resources/down.png')
        self.down_arrow_img = self.down_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.down_arrow_show_img = ImageTk.PhotoImage(
            self.down_arrow_img.copy())
        self.down_arrow_img = ImageTk.PhotoImage(self.down_arrow_img)
        self.down_arrow_first_img = PIL_Image.open('resources/down_first.png')
        self.down_arrow_first_img = self.down_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.down_arrow_first_img = ImageTk.PhotoImage(
            self.down_arrow_first_img)

        self.left_up_arrow_img = PIL_Image.open('resources/left_up.png')
        self.left_up_arrow_img = self.left_up_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_up_arrow_show_img = ImageTk.PhotoImage(
            self.left_up_arrow_img.copy())
        self.left_up_arrow_img = ImageTk.PhotoImage(self.left_up_arrow_img)
        self.left_up_first_arrow_img = PIL_Image.open(
            'resources/left_up_first.png')
        self.left_up_first_arrow_img = self.left_up_first_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_up_first_arrow_img = ImageTk.PhotoImage(
            self.left_up_first_arrow_img)

        self.right_up_arrow_img = PIL_Image.open('resources/right_up.png')
        self.right_up_arrow_img = self.right_up_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_up_arrow_show_img = ImageTk.PhotoImage(
            self.right_up_arrow_img.copy())
        self.right_up_arrow_img = ImageTk.PhotoImage(self.right_up_arrow_img)
        self.right_up_first_arrow_img = PIL_Image.open(
            'resources/right_up_first.png')
        self.right_up_first_arrow_img = self.right_up_first_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_up_first_arrow_img = ImageTk.PhotoImage(
            self.right_up_first_arrow_img)

        self.left_down_arrow_img = PIL_Image.open('resources/left_down.png')
        self.left_down_arrow_img = self.left_down_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_down_arrow_show_img = ImageTk.PhotoImage(
            self.left_down_arrow_img.copy())
        self.left_down_arrow_img = ImageTk.PhotoImage(self.left_down_arrow_img)
        self.left_down_first_arrow_img = PIL_Image.open(
            'resources/left_down_first.png')
        self.left_down_first_arrow_img = self.left_down_first_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_down_first_arrow_img = ImageTk.PhotoImage(
            self.left_down_first_arrow_img)

        self.right_down_arrow_img = PIL_Image.open('resources/right_down.png')
        self.right_down_arrow_img = self.right_down_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_down_arrow_show_img = ImageTk.PhotoImage(
            self.right_down_arrow_img.copy())
        self.right_down_arrow_img = ImageTk.PhotoImage(
            self.right_down_arrow_img)
        self.right_down_first_arrow_img = PIL_Image.open(
            'resources/right_down_first.png')
        self.right_down_first_arrow_img = self.right_down_first_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_down_first_arrow_img = ImageTk.PhotoImage(
            self.right_down_first_arrow_img)

        self.move_img = PIL_Image.open('resources/move.png')
        self.move_img = self.move_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.move_img = ImageTk.PhotoImage(self.move_img)

        self.portal_in_img = PIL_Image.open('resources/portal_in.png')
        self.portal_in_img = self.portal_in_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_in_show_img = ImageTk.PhotoImage(self.portal_in_img.copy())
        self.portal_in_img = ImageTk.PhotoImage(self.portal_in_img)

        self.portal_in_highlight_img = PIL_Image.open(
            'resources/portal_in_highlight.png')
        self.portal_in_highlight_img = self.portal_in_highlight_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_in_highlight_img = ImageTk.PhotoImage(
            self.portal_in_highlight_img)

        self.portal_out_img = PIL_Image.open('resources/portal_out.png')
        self.portal_out_img = self.portal_out_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_out_img = ImageTk.PhotoImage(self.portal_out_img)

        self.portal_out_highlight_img = PIL_Image.open(
            'resources/portal_out_highlight.png')
        self.portal_out_highlight_img = self.portal_out_highlight_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_out_highlight_img = ImageTk.PhotoImage(
            self.portal_out_highlight_img)

    def draw_settings_buttons(self):
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

        self.slider = StringVar()
        self.speed_interval = [speed_interval[0], speed_interval[1]]
        self.speed_length = self.speed_interval[0] - self.speed_interval[1]
        current_speed_percentage = round(
            ((self.speed_interval[0] - move_speed) * 100 / self.speed_length) *
            2) / 2
        self.slider.set(f'{current_speed_percentage}%')
        self.slider_label = ttk.Label(self, textvariable=self.slider)
        self.slider_label.place(x=730, y=110)
        self.set_move_speed_bar = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            length=200,
            value=current_speed_percentage,
            command=lambda e: self.change_move_speed_bar(e))
        self.set_move_speed_bar.place(x=800, y=110)

        self.change_settings_button = ttk.Button(
            self, text='Change Settings', command=self.open_change_settings)
        self.change_settings_button.place(x=850, y=10)
        self.open_settings = False

        self.set_as_notes = ttk.Button(self,
                                       text='Set Notes',
                                       command=self.change_notes)
        self.set_as_notes_label = ttk.Label(self, text='Notes')
        self.set_as_notes_entry = ttk.Entry(self, width=20)
        self.set_as_notes_entry.insert(END, '')
        self.set_as_notes_label.place(x=600, y=350)
        self.set_as_notes_entry.place(x=680, y=350)
        self.set_as_notes.place(x=850, y=350)

        self.set_scale = ttk.Button(self,
                                    text='Set Scale / Mode',
                                    command=self.change_scale)
        self.set_scale_label = ttk.Label(self, text='Scale / Mode')
        self.set_scale_entry = ttk.Entry(self, width=20)
        self.set_scale_entry.insert(END, '')
        self.set_scale_label.place(x=600, y=400)
        self.set_scale_entry.place(x=690, y=400)
        self.set_scale.place(x=850, y=400)

        self.set_chord_name = ttk.Button(self,
                                         text='Set Chord Name',
                                         command=self.change_chord_name)
        self.set_chord_name_label = ttk.Label(self, text='Chord Name')
        self.set_chord_name_entry = ttk.Entry(self, width=20)
        self.set_chord_name_entry.insert(END, '')
        self.set_chord_name_label.place(x=600, y=450)
        self.set_chord_name_entry.place(x=690, y=450)
        self.set_chord_name.place(x=850, y=450)

    def change_chord_name(self):
        self.msg.configure(text='')
        current_chord_name = self.set_chord_name_entry.get()
        current_notes = C(current_chord_name, self.start_octave)
        if type(current_notes) != chord:
            self.msg.configure(text='Error: Invalid chord name')
            return
        for i in current_notes:
            if i.name not in database.standard2:
                i.name = standard_dict[i.name]
        self.current_chord = current_notes
        self.current_chord_intervals = (
            self.current_chord +
            self.current_chord[0].up(database.octave)).intervalof(
                cummulative=False)
        self.current_chord_names = self.current_chord.names()
        self.reset_note()

    def change_scale(self):
        self.msg.configure(text='')
        current_scale = self.set_scale_entry.get().lower()
        current_scale = database.scaleTypes[current_scale]
        if current_scale == 'not found':
            self.msg.configure(text='Error: This scale/mode is not found')
            return
        current_scale = current_scale[:-1]
        self.set_chord_intervals_entry.delete(0, END)
        self.set_chord_intervals_entry.insert(END, str(current_scale))
        self.change_chord_intervals()

    def change_notes(self):
        self.msg.configure(text='')
        current_notes = self.set_as_notes_entry.get()
        if ',' in current_notes:
            current_notes = current_notes.replace(' ', '').split(',')
        else:
            current_notes = current_notes.replace('  ', ' ').split(' ')
        try:
            current_notes = chord(current_notes)
        except:
            self.msg.configure(text='Error: Some of the notes is invalid')
            return
        self.current_chord = current_notes
        self.current_chord_intervals = (
            self.current_chord +
            self.current_chord[0].up(database.octave)).intervalof(
                cummulative=False)
        self.current_chord_names = self.current_chord.names()
        self.start_octave = current_notes[1].num
        self.set_start_octave_entry.delete(0, END)
        self.set_start_octave_entry.insert(END, self.start_octave)
        self.reset_note()

    def change_move_speed_bar(self, e):
        current_percentage = round(float(e) * 2) / 2
        self.slider.set(f'{current_percentage}%')
        self.set_move_speed_entry.delete(0, END)
        self.set_move_speed_entry.insert(
            END,
            round(self.speed_interval[0] -
                  self.speed_length * current_percentage / 100))
        self.change_move_speed()

    def switch_play(self):
        if self.start_moving:
            self.stop_move()
        else:
            self.start()

    def set_as_first(self):
        current_focus = self.current_focus
        if list(current_focus) in self.set_arrows_blocks:
            if self.set_arrows_blocks[0] != list(current_focus):
                first_block = self.set_arrows_blocks[0]
                self.set_arrows_blocks.insert(
                    0,
                    self.set_arrows_blocks.pop(
                        self.set_arrows_blocks.index(list(current_focus))))
                self.reset_arrow_img(*current_focus)
                self.reset_arrow_img(*first_block)

    def open_change_settings(self):
        if not self.open_settings:
            self.open_settings = True
        else:
            return
        os.chdir('scripts')
        with open('change_settings.pyw') as f:
            exec(f.read(), globals(), globals())

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
            self.msg.configure(text='')
            if not self.set_arrows_blocks:
                self.msg.configure(
                    text='There are no arrows for any grids now')
                return
            else:
                if not self.start_moving:
                    self.start_moving = True
                else:
                    return
                first_block = self.set_arrows_blocks[0]
                current_block = self.blocks[first_block[0]][first_block[1]]
                self.current_place = first_block
                self.current_direction = current_block.direction
                self.blocks[self.current_place[0]][
                    self.current_place[1]].configure(image=self.move_img)
                self.play_current_note_move(*self.current_place)
                self.after(self.move_speed, lambda: self.start(False))

        else:
            self.reset_arrow_img(*self.current_place)
            current_block = self.blocks[self.current_place[0]][
                self.current_place[1]]
            if current_block.direction == 'portal' and current_block.portal_direction == 'in':
                try:
                    self.current_place = list(current_block.portal_block)
                    if current_block.change_direction != 'keep':
                        self.current_direction = current_block.change_direction
                except:
                    pass
            elif self.current_direction == 'left':
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
            elif self.current_direction == 'left up':
                self.current_place = self.current_place[
                    0] - 1, self.current_place[1] - 1
                if self.current_place[1] < 0 or self.current_place[0] < 0:
                    self.start_moving = False
                    return
            elif self.current_direction == 'right up':
                self.current_place = self.current_place[
                    0] - 1, self.current_place[1] + 1
                if self.current_place[1] >= len(
                        self.blocks[0]) or self.current_place[0] < 0:
                    self.start_moving = False
                    return
            elif self.current_direction == 'left down':
                self.current_place = self.current_place[
                    0] + 1, self.current_place[1] - 1
                if self.current_place[0] >= len(
                        self.blocks) or self.current_place[1] < 0:
                    self.start_moving = False
                    return
            elif self.current_direction == 'right down':
                self.current_place = self.current_place[
                    0] + 1, self.current_place[1] + 1
                if self.current_place[0] >= len(
                        self.blocks) or self.current_place[1] >= len(
                            self.blocks[0]):
                    self.start_moving = False
                    return
            self.blocks[self.current_place[0]][
                self.current_place[1]].configure(image=self.move_img)
            self.play_current_note_move(*self.current_place)
            new_direction = self.blocks[self.current_place[0]][
                self.current_place[1]].direction
            if new_direction not in ['none', 'portal']:
                self.current_direction = new_direction
            self.after(self.move_speed, lambda: self.start(False))

    def set_arrow(self, mode, e=None):
        if self.set_portal:
            self.portal_direction = mode
            return
        current_focus = self.current_focus
        current_block = self.blocks[current_focus[0]][current_focus[1]]
        if current_block.direction == 'portal':
            return
        if e:
            current_time = time.time()
            current_interval = current_time - self.current_time
            self.current_time = current_time
            if current_interval >= 0.02:
                mode = e.keysym.lower()
        current_first = False
        if (not self.set_arrows_blocks) or (self.set_arrows_blocks
                                            and list(current_focus)
                                            == self.set_arrows_blocks[0]):
            current_first = True
        if list(current_focus) not in self.set_arrows_blocks:
            self.set_arrows_blocks.append(list(current_focus))
        if mode == 'left':
            current_block.configure(
                image=self.left_arrow_img if not current_first else self.
                left_arrow_first_img)
            current_block.direction_num = 0
            current_block.direction = 'left'
        elif mode == 'right':
            current_block.configure(
                image=self.right_arrow_img if not current_first else self.
                right_arrow_first_img)
            current_block.direction = 'right'
            current_block.direction_num = 4
        elif mode == 'up':
            current_block.configure(
                image=self.up_arrow_img if not current_first else self.
                up_arrow_first_img)
            current_block.direction = 'up'
            current_block.direction_num = 2
        elif mode == 'down':
            current_block.configure(
                image=self.down_arrow_img if not current_first else self.
                down_arrow_first_img)
            current_block.direction = 'down'
            current_block.direction_num = 6
        elif mode == 'left up':
            current_block.configure(
                image=self.left_up_arrow_img if not current_first else self.
                left_up_first_arrow_img)
            current_block.direction = 'left up'
            current_block.direction_num = 1
        elif mode == 'right up':
            current_block.configure(
                image=self.right_up_arrow_img if not current_first else self.
                right_up_first_arrow_img)
            current_block.direction = 'right up'
            current_block.direction_num = 3
        elif mode == 'left down':
            current_block.configure(
                image=self.left_down_arrow_img if not current_first else self.
                left_down_first_arrow_img)
            current_block.direction = 'left down'
            current_block.direction_num = 7
        elif mode == 'right down':
            current_block.configure(
                image=self.right_down_arrow_img if not current_first else self.
                right_down_first_arrow_img)
            current_block.direction = 'right down'
            current_block.direction_num = 5
        elif mode == 'none':
            current_block.configure(image=self.block_img)
            current_block.direction = 'none'
            current_block.direction_num = -1

    def set_portal_func(self):
        if not self.set_portal:
            self.set_portal = 'portal in'
            self.portal_direction = 'keep'

    def reset_arrow_img(self, i=0, j=0, current_block=None):
        current_first = False

        if current_block is None:
            current_block = self.blocks[i][j]
            if self.set_arrows_blocks:
                if [i, j] == self.set_arrows_blocks[0]:
                    current_first = True
        else:
            if self.set_arrows_blocks:
                first_block = self.set_arrows_blocks[0]
                if self.blocks[first_block[0]][
                        first_block[1]] == current_block:
                    current_first = True
        if current_block.direction == 'left':
            current_block.configure(
                image=self.left_arrow_img if not current_first else self.
                left_arrow_first_img)
        elif current_block.direction == 'right':
            current_block.configure(
                image=self.right_arrow_img if not current_first else self.
                right_arrow_first_img)
        elif current_block.direction == 'up':
            current_block.configure(
                image=self.up_arrow_img if not current_first else self.
                up_arrow_first_img)
        elif current_block.direction == 'down':
            current_block.configure(
                image=self.down_arrow_img if not current_first else self.
                down_arrow_first_img)
        elif current_block.direction == 'left up':
            current_block.configure(
                image=self.left_up_arrow_img if not current_first else self.
                left_up_first_arrow_img)
        elif current_block.direction == 'right up':
            current_block.configure(
                image=self.right_up_arrow_img if not current_first else self.
                right_up_first_arrow_img)
        elif current_block.direction == 'left down':
            current_block.configure(
                image=self.left_down_arrow_img if not current_first else self.
                left_down_first_arrow_img)
        elif current_block.direction == 'right down':
            current_block.configure(
                image=self.right_down_arrow_img if not current_first else self.
                right_down_first_arrow_img)
        elif current_block.direction == 'none':
            current_block.configure(image=self.block_img)
        elif current_block.direction == 'portal':
            current_block.configure(
                image=self.portal_in_img if current_block.portal_direction ==
                'in' else self.portal_out_img)

    def clear_current_block(self):
        current_focus = self.current_focus
        current_block = self.blocks[current_focus[0]][current_focus[1]]
        if current_block.direction == 'portal':
            current_block.configure(image=self.block_img)
            current_block.direction = 'none'
            self.blocks[current_block.portal_block[0]][
                current_block.portal_block[1]].configure(image=self.block_img)
            self.blocks[current_block.portal_block[0]][
                current_block.portal_block[1]].direction = 'none'
            return
        current_first = False
        if self.set_arrows_blocks and list(
                current_focus) == self.set_arrows_blocks[0]:
            current_first = True
        if list(current_focus) in self.set_arrows_blocks:
            self.set_arrows_blocks.remove(list(current_focus))
        if self.set_arrows_blocks and current_first:
            self.reset_arrow_img(*self.set_arrows_blocks[0])
        current_block.configure(image=self.block_img)
        current_block.direction = 'none'

    def clear_block(self, i, j):
        current_block = self.blocks[i][j]
        if current_block.direction == 'portal':
            current_block.configure(image=self.block_img)
            current_block.direction = 'none'
            self.blocks[current_block.portal_block[0]][
                current_block.portal_block[1]].configure(image=self.block_img)
            self.blocks[current_block.portal_block[0]][
                current_block.portal_block[1]].direction = 'none'
            return
        current_first = False
        if self.set_arrows_blocks and [i, j] == self.set_arrows_blocks[0]:
            current_first = True
        if [i, j] in self.set_arrows_blocks:
            self.set_arrows_blocks.remove([i, j])
        if self.set_arrows_blocks and current_first:
            self.reset_arrow_img(*self.set_arrows_blocks[0])
        current_block.configure(image=self.block_img)
        current_block.direction = 'none'

    def reset_all_blocks(self):
        for i in self.blocks:
            for j in i:
                j.configure(image=self.block_img)
                j.direction = 'none'
        self.set_arrows_blocks.clear()

    def change_move_speed(self):
        self.move_speed = int(self.set_move_speed_entry.get())

    def change_chord_type(self):
        self.msg.configure(text='')
        current_chord_type = self.set_chord_type_entry.get()
        self.chord_type = current_chord_type
        self.current_chord = C(self.chord_root + self.chord_type)
        if type(self.current_chord) == str or self.current_chord is None:
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
            self.current_chord[0].up(database.octave)).intervalof(
                cummulative=False)
        self.current_chord_names = self.current_chord.names()
        self.reset_note()

    def change_chord_root(self):
        self.msg.configure(text='')
        current_chord_root = self.set_chord_root_entry.get()
        if current_chord_root:
            if current_chord_root not in database.standard2:
                if current_chord_root not in standard_dict:
                    self.msg.configure(
                        text='Error: Chord root is not a valid note name')
                    return
                current_chord_root = standard_dict[current_chord_root]
            self.chord_root = current_chord_root
            self.current_chord = C(self.chord_root + self.chord_type)
            self.current_chord_intervals = (
                self.current_chord +
                self.current_chord[0].up(database.octave)).intervalof(
                    cummulative=False)
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
            try:
                self.chord_intervals = literal_eval(current_chord_intervals)
                self.current_chord = get_chord_by_interval(
                    self.chord_root, self.chord_intervals, cummulative=False)
            except:
                self.msg.configure(text='Error: Chord interval is invalid')
                return
        self.current_chord_intervals = (
            self.current_chord +
            self.current_chord[0].up(database.octave)).intervalof(
                cummulative=False)
        self.current_chord_names = self.current_chord.names()
        self.reset_note()

    def draw_board(self):
        self.block_size = size
        self.board = ttk.LabelFrame(width=600, height=500)
        self.block_img = PIL_Image.open('resources/block.png')
        self.unit_size = unit_size
        self.block_img = self.block_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
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
        self.msg = ttk.Label(self, text='')
        self.msg.place(x=600, y=500)

    def set_notes(self):
        global chord_root

        self.chord_type = chord_type
        self.chord_root = chord_root
        self.start_octave = start_octave
        self.chord_intervals = chord_intervals

        if chord_root not in database.standard2:
            if chord_root not in standard_dict:
                self.msg.configure(
                    text='Error: Chord root is not a valid note name')
                return
            chord_root = standard_dict[chord_root]
        self.chord_root = chord_root
        if chord_intervals is not None:
            current_chord = get_chord_by_interval(chord_root,
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
        current_chord_intervals = (
            current_chord +
            current_chord[0].up(database.octave)).intervalof(cummulative=False)
        current_chord_names = current_chord.names()
        self.current_chord_intervals = current_chord_intervals
        self.current_chord_names = current_chord_names

        counter = 0
        start_note = note(self.current_chord[0].name, self.start_octave)
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
        start_note = note(self.current_chord[0].name, self.start_octave)
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
            if current_block.direction != 'portal':
                if current_block.direction == 'none':
                    current_block.direction_num = 0
                else:
                    current_block.direction_num += 1
                    if current_block.direction_num >= 8:
                        current_block.direction_num = 0
                self.set_arrow(
                    self.direction_list[current_block.direction_num])
        if self.set_portal:
            if self.set_portal == 'portal in':
                self.set_portal = 'portal out'
                current_block.configure(image=self.portal_in_img)
                current_block.direction = 'portal'
                current_block.portal_direction = 'in'
                current_block.change_direction = self.portal_direction
                self.set_portal_blocks = i, j
            elif self.set_portal == 'portal out':
                self.set_portal = False
                current_block.configure(image=self.portal_out_img)
                current_block.direction = 'portal'
                current_block.portal_direction = 'out'
                current_block.portal_block = self.set_portal_blocks
                self.blocks[self.set_portal_blocks[0]][
                    self.set_portal_blocks[1]].portal_block = i, j
                self.set_portal_blocks = None
        else:
            if current_block.direction == 'portal':
                if current_block.portal_direction == 'in':
                    current_portal_highlight = [(i, j),
                                                current_block.portal_block]
                else:
                    current_portal_highlight = [
                        current_block.portal_block, (i, j)
                    ]
                if self.current_portal_highlight:
                    for each in self.current_portal_highlight:
                        self.reset_arrow_img(*each)
                    if current_portal_highlight == self.current_portal_highlight:
                        self.current_portal_highlight.clear()
                    else:
                        self.current_portal_highlight = current_portal_highlight
                        portal_in, portal_out = self.current_portal_highlight
                        self.blocks[portal_in[0]][portal_in[1]].configure(
                            image=self.portal_in_highlight_img)
                        self.blocks[portal_out[0]][portal_out[1]].configure(
                            image=self.portal_out_highlight_img)
                else:
                    self.current_portal_highlight = current_portal_highlight
                    portal_in, portal_out = self.current_portal_highlight
                    self.blocks[portal_in[0]][portal_in[1]].configure(
                        image=self.portal_in_highlight_img)
                    self.blocks[portal_out[0]][portal_out[1]].configure(
                        image=self.portal_out_highlight_img)

    def play_current_note_move(self, i, j):
        current_block = self.blocks[i][j]
        play_note(str(current_block.note))

    def set_size(self):
        current_arrows_blocks = [[
            each, self.blocks[each[0]][each[1]].direction
        ] for each in self.set_arrows_blocks]
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
        for each in current_arrows_blocks:
            try:
                current_block = self.blocks[each[0][0]][each[0][1]]
                current_block.direction = each[1]
                self.reset_arrow_img(current_block=current_block)
            except:
                self.set_arrows_blocks.remove(each[0])

    def set_block_size(self):
        self.block_img = PIL_Image.open('resources/block.png')
        self.unit_size = int(self.set_block_size_width_entry.get()), int(
            self.set_block_size_height_entry.get())
        self.block_img = self.block_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.block_img = ImageTk.PhotoImage(self.block_img)
        self.block_width = self.block_img.width
        self.right_arrow_img = PIL_Image.open('resources/right.png')
        self.right_arrow_img = self.right_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_arrow_img = ImageTk.PhotoImage(self.right_arrow_img)
        self.right_arrow_first_img = PIL_Image.open(
            'resources/right_first.png')
        self.right_arrow_first_img = self.right_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.right_arrow_first_img = ImageTk.PhotoImage(
            self.right_arrow_first_img)

        self.left_arrow_img = PIL_Image.open('resources/left.png')
        self.left_arrow_img = self.left_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_arrow_img = ImageTk.PhotoImage(self.left_arrow_img)
        self.left_arrow_first_img = PIL_Image.open('resources/left_first.png')
        self.left_arrow_first_img = self.left_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.left_arrow_first_img = ImageTk.PhotoImage(
            self.left_arrow_first_img)

        self.up_arrow_img = PIL_Image.open('resources/up.png')
        self.up_arrow_img = self.up_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.up_arrow_img = ImageTk.PhotoImage(self.up_arrow_img)
        self.up_arrow_first_img = PIL_Image.open('resources/up_first.png')
        self.up_arrow_first_img = self.up_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.up_arrow_first_img = ImageTk.PhotoImage(self.up_arrow_first_img)

        self.down_arrow_img = PIL_Image.open('resources/down.png')
        self.down_arrow_img = self.down_arrow_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.down_arrow_img = ImageTk.PhotoImage(self.down_arrow_img)
        self.down_arrow_first_img = PIL_Image.open('resources/down_first.png')
        self.down_arrow_first_img = self.down_arrow_first_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.down_arrow_first_img = ImageTk.PhotoImage(
            self.down_arrow_first_img)

        self.move_img = PIL_Image.open('resources/move.png')
        self.move_img = self.move_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.move_img = ImageTk.PhotoImage(self.move_img)

        self.portal_in_img = PIL_Image.open('resources/portal_in.png')
        self.portal_in_img = self.portal_in_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_in_img = ImageTk.PhotoImage(self.portal_in_img)

        self.portal_in_highlight_img = PIL_Image.open(
            'resources/portal_in_highlight.png')
        self.portal_in_highlight_img = self.portal_in_highlight_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_in_highlight_img = ImageTk.PhotoImage(
            self.portal_in_highlight_img)

        self.portal_out_img = PIL_Image.open('resources/portal_out.png')
        self.portal_out_img = self.portal_out_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_out_img = ImageTk.PhotoImage(self.portal_out_img)

        self.portal_out_highlight_img = PIL_Image.open(
            'resources/portal_out_highlight.png')
        self.portal_out_highlight_img = self.portal_out_highlight_img.resize(
            (self.unit_size[0], self.unit_size[1]), PIL_Image.ANTIALIAS)
        self.portal_out_highlight_img = ImageTk.PhotoImage(
            self.portal_out_highlight_img)

        for i in self.blocks:
            for j in i:
                j.configure(image=self.block_img, width=self.block_width)
                self.reset_arrow_img(current_block=j)

        if self.current_portal_highlight:
            portal_in, portal_out = self.current_portal_highlight
            self.blocks[portal_in[0]][portal_in[1]].configure(
                image=self.portal_in_highlight_img)
            self.blocks[portal_out[0]][portal_out[1]].configure(
                image=self.portal_out_highlight_img)


root = Root()
root.mainloop()