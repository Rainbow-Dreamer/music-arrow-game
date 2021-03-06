# Music Arrow Game
 
This is a project inspired by [Hagrid](https://github.com/AnkanGranero/synthgoblin), an amazing and creative grid sequencer made by [Andreas](https://www.youtube.com/channel/UCb_fE048aSG9yULuNCYUV2A), a dude that often appears in the videos of [Simon The Magpie](https://www.youtube.com/channel/UCnbfRvqQcfw3eL71HfjROOQ)'s youtube channel, [this one](https://www.youtube.com/watch?v=0WQpYU6U89k) for example.

Hagrid is an online grid sequencer where you can play here: https://hagrid-sequencer.netlify.app/

After watching Andrea's youtube video [I created a new kind of sequencer! Hagrid!](https://www.youtube.com/watch?v=c1wNKYQ2q2o) in Nov 2020,  
I was amazed by its design and ideas, so I planned to make a stand-alone software to run a game that has some similarities with Hagrid, and you can play it offline, without internet.

This game will probably not be a sequencer like Hagrid in any way, because of my lack of experience with designing sequencer, but you can load a folder of sound files (could be wav, mp3, ogg files) which has each sound file named with a pitch (e.g. C3, D5) into this game, and you can play these sounds in this game when playing with the grids. You can customize the mappings of the name of each note to the sound file in the sound path folder.

This game uses the similar logic as Hagrid, you can set arrows for each grid with one of four directions (left, right, up, down) and extra four diagonal directions (left up, left down, right up, right down). After you press `start` button, the note will start playing at the first grid you set an arrow currently, and moving around the grids following the directions you set for the grids.

You can easily set the chord's root, chord's type and the root's starting octave, moving speed in the game, and you can also set the size of the grid and how many rows and columns you want to have. You can also set the intervals of the chord, which is a list of the intervals between every two adjacent notes in the chord, for example, if you set the chord's interval to `[4, 3, 4]`, then the chord type would be `maj7`, since a major 7th chord is built up successively with a major third (4 semitones), a minor third (3 semitones) and a major third (4 semitones). With this idea, you can even set the chord to a scale (or mode), for example, to get a major scale you can set the chord's interval to `[2, 2, 1, 2, 2, 2]`. The chord's intervals could also be a tuple, which means you can even omit the brackets, for example, `2, 2, 1, 2, 2, 2`.

After you set the arrows for the grids for playing, the starting grid could be changed to any of the grids that has an arrow set by pressing the `Set As Start Grid` button while you are selecting the grid you want to set as the starting grid. All of the starting grids will be shown as an image different from the other grids, which have a special background color. You can set, clear any of the grids while the music is playing through the grids, and you can also change the chord's root, chord's type, root's starting octave, chord's intervals, move speed, block size, board size and so on during the playing, which makes this game interactive and improvising.

There are some keyboard shortcuts and mouse shortcuts built in this software to make the sets and clearances of arrows to the grids and some other actions in this game more easily and quickly.  
* After you click on one of the grids, you can use the arrow keys on the keyboard to set the grid with an arrow with the direction that the key corresponds to, for diagonal directions, just use combinations of the arrow keys (press at the same time) to set the arrow.
* To clear the arrow of a grid, right click the mouse on the grid. Or you can click on the grid and press `Ctrl + E` on the keyboard to clear the arrow. The button `Clear` will also do the trick for you.
* To clear all of the arrows that are currently set, you can press `Ctrl + R` on the keyboard, or you can press the button `Reset All Arrows`
* There is a `Place Arrow Mode` built in this software, which could help you use mouse to quickly set the arrows for the grids. Normally, you can set the arrows for the grids by clicking on a grid and then click on the arrows button with the desired direction on the right side of the screen in the software, but this will be kind of slow and inconvenient. You can press the button `Normal Mode` or press `Tab` on the keyboard to switch between Normal Mode and Place Arrow Mode. When you are in Place Arrow Mode, you can click on a grid and then firstly set the grid to left direction with an arrow. You can click the grid again to set it to up direction, and then right up direction, and then right direction, etc., which changes in a clockwise direction, the directions you can set will loop again when it goes back to the up direction. To clear the arrow, it is the same as usual, right click the mouse or use `Ctrl + E` on the keyboard.
* You can press `Ctrl + space` on the keyboard to start playing with current grids, and press `Ctrl + space` again to stop current playing. You can also press the `Start` and `Stop` button to start and stop playing with current grids.
* press `Ctrl + Q` on the keyboard or click the `Set As Start Grid` button to set the grid you are currently clicked on as the starting grid (there must be an arrow in this grid)
* press `Ctrl + T` on the keyboard or click the `Change Settings` button to open the change settings window

The note names with octaves will appear on each grid as the note that each grid currently corresponds to, and when you click on the grid, it will play the sound file that the note of this grid corresponds to, in other words, when you click on a grid, it will play the note for you.

The move speed is the time interval of each move in milliseconds (ms), the smaller it is, the faster the playing moves through the grids.

There are some advanced options in this game.

You can set a portal in the board, and when the moving go through the portal, it will go out from the another side of the portal. Click the circle button under the arrows buttons and click on a grid to set an in portal, and click on another grid to set an out portal. You can click the right button of mouse to cancel setting a portal. Note that in default the portal doesn't change the current direction of moving, but this game supports direction change through a portal. After you click on the portal button, you can then click one of the arrows buttons to make the portal has its own direction change function like the arrows. Then you can set a portal which can change direction while also being as a portal. If you click on any of the portals, the portal and the another portal associated with this portal will be highlighted, and you can click again to unhighlight them. To clear a pair of portals, it is the same as clearing an arrow, when you right click the mouse on a portal, the portal and its paired portal will both be cleared.

You can directly set the notes of the chord by entering the name of the notes (could be with or without octaves), separated with `,` or ` `.

If you want to set a scale/mode, you can enter the name of the scale/mode, the valid scale/mode name can be looked at `scaleTypes` in the file database.py in musicpy folder.

Here is a screenshot of this software:  
![image](https://github.com/Rainbow-Dreamer/music-arrow-game/blob/main/previews/1.jpg)
