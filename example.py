from c4game import C4Game, C4State, C4Exception

if __name__ == "__main__":
    game = C4Game()
    state = game.getState()

    def show(board):
        for row in board:
            print(row)

    while (state.result == C4State.NOT_COMPLETE):
        try:
            show(state.board)
            col = int(input('enter col for player {} : '.format(state.currentPlayer)))
            state = game.move(state.currentPlayer, col)  
        except C4Exception as e:
            print(e)
            continue
        except ValueError:
            print('Enter int')
            continue
        
    show(state.board)
    print('game complete')
    msg = ''

    if state.result != C4State.TIE:
        msg = 'player {} won'.format(state.result)
    else:
        msg = 'Tie' 
    print(msg)