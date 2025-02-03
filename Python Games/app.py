from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run/<game_name>')
def run_game(game_name):
    try:
        # Map game names to file paths
        games = {
            "Tic-Tac-Toe": "scripts/game1.py",
            "Snake Game": "scripts/game2.py",
            "Tile Twister": "scripts/game3.py",
            "Game Fruit Catch": "scripts/game4.py",
            "Minesweeper": "scripts/game5.py",
            "Classic Snake": "scripts/game6.py",
        }

        # Check if the game exists in the mapping
        if game_name in games:
            game_path = games[game_name]
            # Run the script without showing the command prompt window
            def run_script():
                subprocess.run(['python', game_path], creationflags=subprocess.CREATE_NO_WINDOW)
                socketio.emit('game_finished', {'game_name': game_name})

            threading.Thread(target=run_script).start()
            return f"Running {game_name}."
        else:
            return f"Game {game_name} not found.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    socketio.run(app, debug=True)