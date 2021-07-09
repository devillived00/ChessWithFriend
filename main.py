from flask import Flask, redirect, render_template, request, session, url_for, flash
import chess.svg
from flask_socketio import SocketIO, emit
from chessAPI import top_10_players
import time
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins='*')
#List of messages sent by users
chatbox = []

#Formated chessboard
board = chess.Board()

#Variable used to define player color
color = random.randint(1, 2)


def list_of_lists(given_list):
    """
    Function formats items in the chatbox to look more like messages
    """
    listv2 = []
    for item in given_list:
        x = item.split(', ')
        stringpass = ""
        for i in x:
            stringpass += i
        listv2.append(stringpass)
    return listv2


def turn_method():
    """
    Function returns string that contains information about who's turn it is
    """
    if board.turn:
        turn = "White's move"
        return turn
    elif not board.turn:
        turn = "Black's move"
        return turn


@app.route('/', methods=['GET', 'POST'])
def login_page():
    """
    Function simply creates a session for the user
    """
    if request.method == 'POST':
        if request.form['nickname'] == 'admin':
            admin = request.form['nickname']
            session["user"] = admin
            return redirect('/play')
        elif request.form['nickname'] == 'guest':
            guest = request.form['nickname']
            session["user"] = guest
            return redirect('/play')

        else:
            return redirect(url_for('login_page'))

    return render_template('login.html')


@app.route('/chat', methods=["POST", "GET"])
def chat():
    """
    Function handles chat route, and formats messages by adding time, user and some html
    """

    if request.method == "POST":
        username = session["user"]
        messages = request.form['message']
        message_time = datetime.now().strftime('%H:%M:%S')
        message = (f'<sup>{str(message_time)}</sup>' + ' ' + f'<strong>{username.upper()}</strong>' + ': '
                   + f'<b><mark>{messages}</b></mark>')
        chatbox.append(message)
        return render_template('chat.html', chat=list_of_lists(chatbox))
    return render_template('chat.html', chat=list_of_lists(chatbox))


@app.route('/play', methods=['POST', 'GET'])
def play():
    """
    This function handles gameplay.
    Assign a color to the user which determines a turn, handle movement logic.
    Logic is provided for players separately. If Admin is black and if it's white, same goes for Guest.
    It renders svg version of board for white and black player with correct perspective.
    Function ensures that the given move is legal and the game is not over. 
    """
    global color

    if color == 2:
        if session["user"] == 'admin':
            board_svg = chess.svg.board(board, orientation=chess.BLACK, size=400)
            if not board.is_game_over():
                if board.is_check():
                    board_svg = chess.svg.board(board, orientation=chess.BLACK, size=400, check=board.king(chess.BLACK))
                    return render_template('index.html', board=board_svg, turn=turn_method(),
                                           )
                else:
                    pass
                if request.method == 'POST':
                    if board.turn == chess.BLACK:
                        try:
                            board.push_san(request.form['move'])
                            if board.is_game_over():
                                flash("You have won!")
                                board.reset()
                                color = 1
                                board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                            else:
                                board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                        except:
                            pass
                    elif board.turn == chess.WHITE:
                        board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                        return render_template('index.html', board=board_svg2, turn=turn_method(),
                                               )

            return render_template('index.html', board=board_svg, turn=turn_method(),
                                   )

        elif session["user"] == 'guest':
            board_svg = chess.svg.board(board, orientation=chess.WHITE, size=400)
            if not board.is_game_over():
                if board.is_check():
                    board_svg = chess.svg.board(board, orientation=chess.WHITE, size=400, check=board.king(chess.WHITE))
                    return render_template('index.html', board=board_svg, turn=turn_method(),
                                           )
                else:
                    pass
                if request.method == 'POST':
                    if board.turn == chess.WHITE:
                        try:
                            board.push_san(request.form['move'])
                            if board.is_game_over():
                                flash("You have won!")
                                board.reset()
                                color = 1
                                board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                            else:
                                board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                        except:
                            pass
                    elif board.turn == chess.BLACK:
                        board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                        return render_template('index.html', board=board_svg2, turn=turn_method(),
                                               )

            return render_template('index.html', board=board_svg, turn=turn_method(),
                                   )

    elif color == 1:
        if session["user"] == 'guest':
            board_svg = chess.svg.board(board, orientation=chess.BLACK, size=400)
            if not board.is_game_over():
                if board.is_check():
                    board_svg = chess.svg.board(board, orientation=chess.BLACK, size=400, check=board.king(chess.BLACK))
                    return render_template('index.html', board=board_svg, turn=turn_method(),
                                           )
                else:
                    pass
                if request.method == 'POST':
                    if board.turn == chess.BLACK:
                        try:
                            board.push_san(request.form['move'])
                            if board.is_game_over():
                                flash("You have won!")
                                color = 2
                                board.reset()
                                board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                            else:
                                board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                        except:
                            pass
                    elif board.turn == chess.WHITE:
                        board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                        return render_template('index.html', board=board_svg2, turn=turn_method(),
                                               )

            return render_template('index.html', board=board_svg, turn=turn_method(),
                                   )

        elif session["user"] == 'admin':
            board_svg = chess.svg.board(board, orientation=chess.WHITE, size=400)
            if not board.is_game_over():
                if board.is_check():
                    board_svg = chess.svg.board(board, orientation=chess.WHITE, size=400, check=board.king(chess.WHITE))
                    return render_template('index.html', board=board_svg, turn=turn_method(),
                                           )
                else:
                    pass
                if request.method == 'POST':
                    if board.turn == chess.WHITE:
                        try:
                            board.push_san(request.form['move'])
                            if board.is_game_over():
                                flash("You have won!")
                                board.reset()
                                color = 2
                                board_svg2 = chess.svg.board(board, orientation=chess.BLACK, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                            else:
                                board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                                return render_template('index.html', board=board_svg2, turn=turn_method(),
                                                       )
                        except:
                            pass
                    elif board.turn == chess.BLACK:
                        board_svg2 = chess.svg.board(board, orientation=chess.WHITE, size=400)
                        return render_template('index.html', board=board_svg2, turn=turn_method(),
                                               )

            return render_template('index.html', board=board_svg, turn=turn_method(),
                                   )


@socketio.on('move', namespace='/play')
def handle_refresh(moved):
    """
    Server handles live board
    """
    print(moved)
    time.sleep(0.1)
    emit('from flask', broadcast=True)


@socketio.on('client', namespace='/chat')
def handle_chat(client):
    """
    Server handles live chat
    """
    print(client)
    time.sleep(0.1)
    emit('from client', broadcast=True)
