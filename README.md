# WordsWithChilwell
Tile-based two-player word game inspired by 'Words with Friends'

## Rules
Each player starts with 15 randomly-selected tiles. Each
tile represents a single letter; each letter has a points value as shown in Figure 1. The tiles that a
player has are called their "hand". Each player starts with a score of 50.

| Letter  | Points letter is worth |
| :---: | :---: |
| A  | 1  |
| B  | 2  |
| C  | 2  |
| D  | 2  |
| E  | 1  |
| F  | 3  |
| G  | 2  |
| H  | 3  |
| I  | 1  |
| J  | 5  |
| K  | 3  |
| L  | 2  |
| M  | 2  |
| N  | 1  |
| O  | 1  |
| P  | 2  |
| Q  | 5  |
| R  | 1  |
| S  | 1  |
| T  | 1  |
| U  | 2  |
| V  | 3  |
| W  | 3  |
| X  | 5  |
| Y  | 3  |
| Z  | 5  |
| ▊  | 0  |

Players take turns to spell a two or more letter word using only the letter tiles in their hand. Each tile
may only be used once in the word. If on their turn they spell a valid word then the tiles used in that
word are removed from their hand and their score is increased. The amount their score increases by
depends on which tiles were used and the number of tiles used in the word. Initially the score
increases by the total points value of the tiles used. If a valid word is spelt that uses more than seven
tiles an additional 20 points are added to the player’s score. If a valid word is spelt that uses six or
seven tiles an additional five points are added to the player’s score.

The player may then choose to either get three new tiles, get a number of new tiles equal to the
number of tiles used in the word they just spelt, get a number of new tiles equal to three larger than
the number of tiles used in the word they just spelt or to get no new tiles. New tiles come from the
tile queue.

If the word they spelt is not valid then their turn is over. No tiles are removed from their hand and
they get three tiles from the tile queue.

A valid word is one in which all the tiles needed to spell the word are in their hand and it is a
correctly-spelt English word.

The tile queue contains 20 randomly-selected tiles. The tiles in the queue are shown in order, the tile
at the front of the queue will be the next tile given to a player who gets a new tile. When a tile is
removed from the front of the queue and given to a player, a new randomly-selected tile is added to
the rear of the queue. Players may look at the contents of the tile queue at any time.

The game ends when either a player has used a total of more than 50 tiles in the valid words they
have spelt or when their hand contains 20 or more tiles. If Player One uses more than 50 tiles first or
has a hand with 20 or more tiles then Player Two gets to have their turn before the game ends. At the
end of the game each player’s score is reduced by the points value of the letters on the tiles
remaining in their hand. The winner is the player with the highest score.
