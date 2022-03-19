# 50002-1D-Team-17

## The Main Game FSM

### States:

1. `START` - more waves to begin with on the LED matrix? start game with the press of a button and switch states to `P1_TURN`

2. `P1_TURN` - have a selection on the board that starts in the middle but can be moved around with the inputs given below. when the input `confirm_selection` is turned on, lock the selected square in and change state to `P1_PLACING`
3. `P1_PLACING` - select the size of the piece to place in this state using the `up`/`down` inputs given below.

4. `P2_TURN` - same as `P1_TURN` but for p2
5. `P2_PLACING` - same as `P1_PLACING` but for p2

7. `END` - if any of the conditions given below are fulfilled, the game ends and a victor is declared.

### DFFs

Initialise:
1. `piece_count_p1[3] = {-1, 2, 2, 2}` -1, small, medium, large counts for p1
2. `piece_count_p2[3] = {-1, 2, 2, 2}` -1, small, medium, large counts for p1
3. `board_state[3][3][3] = 0` - this represents the 3x3 board for the game, the last `[3]` is just because the 3x3 array is of 3 bit wide ints.
4. `selectX[2] = 1` - selected square X coord to place the piece on
5. `selectY[2] = 1` - selected square Y coord to place the piece on

### Inputs

1. `left` - move selection left verify that the selection does not go out of bounds from the tic tac toe grid
2. `right` - move selection right verify that the selection does not go out of bounds from the tic tac toe grid
3. `up` - move selection up verify that the selection does not go out of bounds from the tic tac toe grid
4. `down` - move selection down verify that the selection does not go out of bounds from the tic tac toe grid
5. `confirm_selection` - when set to `1` this locks in the selected square for piece placement. change states to `P#_PLACING` where `up`/`down` can be used to pick the size of the piece. 
6. `confirm_size` - when set to `1` this locks in the size and places the piece for the player. deduct one from corresponding `piece_count` of the corresponding player and move to the state for next player's turn. `abs(confirm_size) > abs(board[selectY][selectX])` must be true for a valid placement (this condition will make more sense after you read the next section). These numbers represent the pieces for the players on the board:

`0: empty cell`

`1: small piece p1`

`2: medium piece p1`

`3: large piece p1`

`-1: small piece p2`

`-2: medium piece p2`

`-3: large piece p2`


### Victory Conditions

To check if a player won the game:

#### The conditions for p2 victory, all of these are OR-ed together:
 
`board[0][0] < 0 && board[0][1] < 0 && board[0][2] < 0` - first row full

`board[1][0] < 0 && board[1][1] < 0 && board[1][2] < 0` - second row full

`board[2][0] < 0 && board[2][1] < 0 && board[2][2] < 0` - thrid row full
 
`board[0][0] < 0 && board[1][0] < 0 && board[2][0] < 0` - first column full

`board[0][1] < 0 && board[1][1] < 0 && board[2][1] < 0` - second column full

`board[0][2] < 0 && board[1][2] < 0 && board[2][2] < 0` - thrid column full

`board[0][0] < 0 && board[1][1] < 0 && board[2][2] < 0` - principle diagonal full

`board[0][2] < 0 && board[1][1] < 0 && board[2][0] < 0` - reverse diagonal full


#### The conditions for p1 victory, all of these are OR-ed together:
 
`board[0][0] > 0 && board[0][1] > 0 && board[0][2] > 0` - first row full

`board[1][0] > 0 && board[1][1] > 0 && board[1][2] > 0` - second row full

`board[2][0] > 0 && board[2][1] > 0 && board[2][2] > 0` - thrid row full
 
`board[0][0] > 0 && board[1][0] > 0 && board[2][0] > 0` - first column full

`board[0][1] > 0 && board[1][1] > 0 && board[2][1] > 0` - second column full

`board[0][2] > 0 && board[1][2] > 0 && board[2][2] > 0` - thrid column full

`board[0][0] > 0 && board[1][1] > 0 && board[2][2] > 0` - principle diagonal full

`board[0][2] > 0 && board[1][1] > 0 && board[2][0] > 0` - reverse diagonal full

### Outputs

`board_state[3][3][3]`

## Display

### Inputs

`board_state[3][3][3]`

lights the corresponding pixels on the LED matrix depending on the values in `board_state`. This file is completely separate from the main game FSM, and does not interact with the other file in any way. This file will figure out all the logic needed for displaying the board on its own