"""
Script para atualizar jogadores existentes no banco com os novos campos
totalGames, assists, totalTrophies, redCards
Execute este script após adicionar os novos campos ao modelo Player
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.Player import Player

# Mapeamento de dados realistas
PLAYER_STATS = {
    'NEYMAR JR': (650, 250, 25, 8),
    'MESSI': (1000, 350, 45, 3),
    'RONALDO': (1200, 250, 35, 11),
    'MBAPPE': (350, 120, 15, 2),
    'HAALAND': (250, 50, 8, 1),
    'VINI JR': (300, 100, 12, 5),
    'KANE': (600, 100, 2, 0),
    'M. SALAH': (550, 150, 10, 1),
    'BENZEMA': (750, 200, 30, 6),
    'MODRIC': (800, 150, 25, 3),
    'RODRYGO': (250, 80, 8, 2),
    'BELLINGHAM': (200, 60, 5, 1),
    'DE BRUYNE': (600, 250, 15, 4),
    'LEWANDOWSKI': (800, 150, 30, 5),
    'SUAREZ': (700, 200, 25, 12),
    'INIESTA': (750, 200, 35, 2),
    'XAVI': (800, 180, 30, 3),
    'RAMOS': (700, 50, 25, 28),
    'BALE': (550, 120, 20, 3),
    'KROOS': (700, 120, 25, 2),
    'SON': (500, 100, 1, 1),
    'MANE': (600, 120, 12, 2),
    'VAN DIJK': (500, 20, 8, 2),
    'FODEN': (250, 80, 10, 0),
    'GRIEZMANN': (650, 150, 12, 4),
    'COURTOIS': (500, 0, 20, 0),
    'PEDRI': (150, 30, 2, 0),
    'BRUNO FERNANDES': (400, 150, 3, 5),
    'RASHFORD': (350, 80, 3, 1),
    'ALISSON': (400, 0, 8, 0),
    'EDERSON': (350, 0, 12, 0),
    'CASEMIRO': (500, 30, 20, 15),
    'MARQUINHOS': (500, 20, 8, 5),
    'THIAGO SILVA': (600, 10, 15, 8),
    'FABINHO': (400, 20, 8, 3),
    'GABRIEL JESUS': (400, 100, 8, 2),
    'RICHARLISON': (350, 50, 2, 3),
    'ANTONY': (200, 50, 1, 2),
    'MARTINELLI': (200, 60, 1, 1),
    'SAKA': (250, 80, 1, 0),
    'OBLAK': (400, 0, 5, 0),
    'VARANE': (400, 5, 15, 3),
    'CARVAJAL': (500, 30, 20, 5),
    'MENDY': (300, 10, 8, 2),
    'MILITAO': (300, 5, 8, 2),
    'ALABA': (500, 40, 25, 3),
    'CAMAVINGA': (200, 20, 5, 1),
    'TCHOUAMENI': (200, 10, 5, 1),
    'VALVERDE': (300, 50, 8, 2),
    'GAVI': (150, 20, 2, 3),
    'DE JONG': (350, 50, 5, 2),
    'TER STEGEN': (500, 0, 15, 0),
    'ARAUJO': (200, 5, 2, 2),
    'KOUNDE': (250, 5, 2, 1),
    'BALDE': (150, 10, 2, 1),
    'LEAO': (300, 80, 2, 2),
    'OSIMHEN': (250, 30, 1, 1),
    'KVARATSKHELIA': (150, 50, 1, 0),
    'BARELLA': (350, 60, 3, 4),
    'LAUTARO': (350, 80, 4, 5),
    'LUKAKU': (600, 100, 3, 2),
    'DYBALA': (450, 120, 3, 2),
    'CHIESA': (300, 60, 2, 2),
    'VLAHOVIC': (250, 30, 1, 3),
    'KIMMICH': (400, 80, 15, 2),
    'MULLER': (700, 250, 30, 2),
    'NEUER': (600, 0, 25, 0),
    'GORETZKA': (400, 50, 15, 2),
    'SANÉ': (450, 120, 10, 3),
    'MUSIALA': (200, 50, 5, 1),
    'ALEXANDER-ARNOLD': (300, 80, 8, 0),
    'ROBERTSON': (400, 60, 8, 1),
    'KONATE': (200, 5, 1, 1),
    'MAC ALLISTER': (250, 40, 2, 2),
    'SZOBOSZLAI': (200, 50, 1, 1),
    'DIAZ': (200, 40, 1, 1),
    'JOTA': (300, 50, 1, 1),
    'GUNDOGAN': (500, 100, 15, 2),
    'BERNARDO SILVA': (500, 120, 15, 1),
    'WALKER': (500, 30, 15, 3),
    'STONES': (400, 10, 15, 1),
    'DIAS': (300, 5, 15, 2),
    'AKANJI': (300, 5, 15, 1),
    'GREALISH': (350, 80, 8, 2),
    'ALVAREZ': (200, 50, 8, 1),
    'DONNARUMMA': (300, 0, 3, 0),
    'HAKIMI': (400, 50, 5, 2),
    'VERRATTI': (500, 40, 10, 8),
    'IBRAHIMOVIC': (800, 200, 35, 15),
    'CAVANI': (600, 100, 15, 5),
    'DI MARIA': (700, 250, 20, 5),
    'MOUNT': (300, 60, 2, 1),
    'HAVERTZ': (350, 50, 2, 2),
    'JAMES': (500, 150, 15, 8),
    'POGBA': (450, 80, 5, 4),
    'KANTE': (500, 30, 8, 1),
    'HAZARD': (600, 150, 8, 2),
    'STERLING': (550, 120, 8, 1),
    'PULISIC': (300, 60, 2, 1),
    'ZINCHENKO': (300, 40, 8, 1),
    'RICE': (300, 20, 1, 2),
    'ODEgaard': (350, 80, 1, 1),
    'SALIBA': (200, 5, 1, 2),
    'GABRIEL': (300, 10, 1, 3),
    'PARTEY': (350, 20, 1, 3),
    'JOÃO FELIX': (300, 80, 1, 3),
    'BUSQUETS': (700, 50, 30, 8),
    'PIQUE': (600, 20, 30, 10),
    'JORDI ALBA': (500, 60, 20, 5),
    'COSTA': (600, 80, 8, 15),
}

def update_players():
    """Atualiza os jogadores existentes no banco com os novos campos"""
    app = create_app()
    
    with app.app_context():
        updated_count = 0
        default_count = 0
        
        for player in Player.query.all():
            if player.name in PLAYER_STATS:
                total_games, assists, total_trophies, red_cards = PLAYER_STATS[player.name]
                player.totalGames = total_games
                player.assists = assists
                player.totalTrophies = total_trophies
                player.redCards = red_cards
                updated_count += 1
                print(f"✅ Atualizado: {player.name}")
            else:
                # Valores padrão baseados em posição e gols
                if player.goals == 0 or player.position == 'Goleiro':
                    player.totalGames = 300
                    player.assists = 0
                    player.totalTrophies = 5
                    player.redCards = 0
                elif player.position in ['Zagueiro', 'Lateral']:
                    player.totalGames = 400
                    player.assists = 20
                    player.totalTrophies = 8
                    player.redCards = 3
                elif player.position == 'Meio-campo':
                    player.totalGames = 450
                    player.assists = 80
                    player.totalTrophies = 10
                    player.redCards = 2
                else:  # Atacante
                    player.totalGames = 500
                    player.assists = 100
                    player.totalTrophies = 8
                    player.redCards = 2
                default_count += 1
                print(f"📝 Padrão aplicado: {player.name}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print(f"✅ Atualização concluída!")
        print(f"   📊 Jogadores atualizados: {updated_count}")
        print(f"   📝 Jogadores com valores padrão: {default_count}")
        print("="*50)

if __name__ == '__main__':
    update_players()

