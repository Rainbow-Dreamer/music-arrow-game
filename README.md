# Music Arrow Game
 
This is a project inspired by [Hagrid](https://github.com/AnkanGranero/synthgoblin), an amazing and creative grid sequencer made by [Andreas](https://www.youtube.com/channel/UCb_fE048aSG9yULuNCYUV2A), a dude that often appears in the videos of [Simon The Magpie](https://www.youtube.com/channel/UCnbfRvqQcfw3eL71HfjROOQ)'s youtube channel, [this one](https://www.youtube.com/watch?v=0WQpYU6U89k) for example.

Hagrid is an online grid sequencer where you can play here: https://hagrid-sequencer.netlify.app/

After watching Andrea's youtube video [I created a new kind of sequencer! Hagrid!](https://www.youtube.com/watch?v=c1wNKYQ2q2o) in Nov 2020,  
I was amazed by its design and ideas, so I planned to make a stand-alone software to run a game that has some similarities with Hagrid, and you can play it offline, without internet.

This game will probably not be a sequencer like Hagrid in any way, because of my lack of experience with designing sequencer, but you can load a folder of sound files (could be wav, mp3, ogg files) which has each sound file named with a pitch (e.g. C3, D5) into this game, and you can play these sounds in this game when playing with the grids. You can customize the mappings of the name of each note to the sound file in the sound path folder.

This game uses the similar logic as Hagrid, you can set arrows for each grid with four directions, and after you press `start` button, the note will start playing at the first grid you set an arrow currently, and moving around the grids following the directions you set for the grids.

You can easily set the chord's root, chord's type and the root's starting octave, moving speed in the game, and you can also set the size of the grid and how many rows and columns you want to have. You can also set the intervals of the chord, which is a list of the intervals between every two adjacent notes in the chord, for example, if you set the chord's
interval to `[4, 3, 4]`, then the chord type would be `maj7`, since a major 7th chord is built up successively with a major third (4 semitones), a minor third (3 semitones) and a major third (4 semitones). With this idea, you can even set the chord to a scale (or mode), for example, to get a major scale you can set the chord's interval to `[2, 2, 1, 2, 2, 2]`.

After you set the arrows for the grids for playing, the starting grid could be changed to any of the grids that has an arrow set by pressing the `Set As Start Grid` button while you are selecting the grid you want to set as the starting grid. All of the starting grids will be shown as an image different from other grids, which have a special background color. You can set, clear any of the grids while the music is playing through the grids, and you can also change the chord's root, chord's type, root's starting octave, chord's intervals, move speed, block size, board size during the playing, which makes this game interactive and improvising.

There are some keyboard shortcuts built in this software to make the sets of arrows to the grids and some other actions in this game more easily and quickly.  
