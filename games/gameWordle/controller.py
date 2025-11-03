from flask import Blueprint, render_template, request, jsonify
import random

game_wordle_bp = Blueprint('game_wordle', __name__, template_folder='../../templates/games')

# Lista de jogadores
players = [
    "NEYMAR", "MESSI", "RONALDO", "MBAPPE", "HAALAND",
    "VINI", "KANE", "SALAH", "BENZEMA", "MODRIC"
]

current_answer = ""

@game_wordle_bp.route('/')
def home():
    global current_answer
    current_answer = random.choice(players)
    return render_template('games/game_wordle.html', word_length=len(current_answer))

@game_wordle_bp.route('/guess', methods=['POST'])
def check_guess():
    guess = request.json['guess'].upper()
    result = []
    
    if len(guess) != len(current_answer):
        return jsonify({'error': f'A palavra deve ter {len(current_answer)} letras!'})

    for i, letter in enumerate(guess):
        if letter == current_answer[i]:
            result.append({'letter': letter, 'color': 'green'})
        elif letter in current_answer:
            result.append({'letter': letter, 'color': 'yellow'})
        else:
            result.append({'letter': letter, 'color': 'gray'})
    
    won = guess == current_answer
    game_over = won or request.json['attempt'] >= 4

    return jsonify({
        'result': result,
        'won': won,
        'gameOver': game_over,
        'answer': current_answer if game_over else None
    })
