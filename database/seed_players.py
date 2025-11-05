"""
Script para popular a tabela Player com dados de jogadores de futebol
Execute este script após inicializar o banco de dados
"""
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.Player import Player


def seed_players():
    """
    Popula a tabela Player com dados de jogadores famosos
    """
    app = create_app()
    
    with app.app_context():
        # Verifica se já existem jogadores no banco
        existing_players = Player.query.count()
        if existing_players > 0:
            print(f"⚠️  Já existem {existing_players} jogadores no banco. Deseja continuar?")
            print("   (O script irá adicionar novos jogadores se não existirem)")
        
        # Lista de jogadores para inserir
        players_data = [
            {
                'name': 'NEYMAR JR',
                'playedAt': 'Santos,Barcelona,PSG,Al-Hilal',
                'managedBy': 'Tite,Dunga',
                'playedWith': 'Messi,Suarez,Iniesta',
                'nationality': 'Brasil',
                'trophiesEarned': 'Copa Libertadores,Champions League,Copa do Brasil',
                'leaguesPlayed': 'Brasileirão,La Liga,Ligue 1',
                'position': 'Atacante',
                'goals': 400,
                'imageName': 'neymar.jpg'
            },
            {
                'name': 'MESSI',
                'playedAt': 'Barcelona,PSG,Inter Miami',
                'managedBy': 'Pep Guardiola,Luis Enrique',
                'playedWith': 'Neymar,Suarez,Xavi,Iniesta',
                'nationality': 'Argentina',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga,Ballon dOr',
                'leaguesPlayed': 'La Liga,Ligue 1,MLS',
                'position': 'Atacante',
                'goals': 800,
                'imageName': 'messi.jpg'
            },
            {
                'name': 'RONALDO',
                'playedAt': 'Manchester United,Real Madrid,Juventus,Al Nassr',
                'managedBy': 'Sir Alex Ferguson,Zidane',
                'playedWith': 'Benzema,Modric,Bale',
                'nationality': 'Portugal',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga,Ballon dOr',
                'leaguesPlayed': 'Premier League,La Liga,Serie A',
                'position': 'Atacante',
                'goals': 850,
                'imageName': 'ronaldo.jpg'
            },
            {
                'name': 'MBAPPE',
                'playedAt': 'Monaco,PSG,Real Madrid',
                'managedBy': 'Didier Deschamps,Thomas Tuchel',
                'playedWith': 'Neymar,Messi,Ramos',
                'nationality': 'França',
                'trophiesEarned': 'Copa do Mundo,Ligue 1',
                'leaguesPlayed': 'Ligue 1,La Liga',
                'position': 'Atacante',
                'goals': 300,
                'imageName': 'mbappe.jpg'
            },
            {
                'name': 'HAALAND',
                'playedAt': 'Molde,RB Salzburg,Borussia Dortmund,Manchester City',
                'managedBy': 'Pep Guardiola,Erling Haaland Sr',
                'playedWith': 'De Bruyne,Gundogan,Foden',
                'nationality': 'Noruega',
                'trophiesEarned': 'Champions League,Premier League,Bundesliga',
                'leaguesPlayed': 'Premier League,Bundesliga',
                'position': 'Atacante',
                'goals': 250,
                'imageName': 'haaland.jpg'
            },
            {
                'name': 'VINI JR',
                'playedAt': 'Flamengo,Real Madrid',
                'managedBy': 'Carlo Ancelotti',
                'playedWith': 'Benzema,Modric,Rodrygo',
                'nationality': 'Brasil',
                'trophiesEarned': 'Champions League,La Liga,Copa do Brasil',
                'leaguesPlayed': 'Brasileirão,La Liga',
                'position': 'Atacante',
                'goals': 150,
                'imageName': 'vini.jpg'
            },
            {
                'name': 'KANE',
                'playedAt': 'Tottenham,Bayern Munich',
                'managedBy': 'Mauricio Pochettino,Thomas Tuchel',
                'playedWith': 'Son,Heung-min,Lewandowski',
                'nationality': 'Inglaterra',
                'trophiesEarned': 'Bundesliga',
                'leaguesPlayed': 'Premier League,Bundesliga',
                'position': 'Atacante',
                'goals': 400,
                'imageName': 'kane.jpg'
            },
            {
                'name': 'M. SALAH',
                'playedAt': 'Basel,Chelsea,Roma,Liverpool',
                'managedBy': 'Jurgen Klopp',
                'playedWith': 'Mane,Firmino,Van Dijk',
                'nationality': 'Egito',
                'trophiesEarned': 'Champions League,Premier League',
                'leaguesPlayed': 'Premier League,Serie A',
                'position': 'Atacante',
                'goals': 350,
                'imageName': 'salah.jpg'
            },
            {
                'name': 'BENZEMA',
                'playedAt': 'Lyon,Real Madrid,Al Ittihad',
                'managedBy': 'Carlo Ancelotti,Zidane',
                'playedWith': 'Ronaldo,Modric,Bale',
                'nationality': 'França',
                'trophiesEarned': 'Champions League,La Liga,Ballon dOr',
                'leaguesPlayed': 'La Liga,Ligue 1',
                'position': 'Atacante',
                'goals': 450,
                'imageName': 'benzema.jpg'
            },
            {
                'name': 'MODRIC',
                'playedAt': 'Dinamo Zagreb,Tottenham,Real Madrid',
                'managedBy': 'Carlo Ancelotti,Zidane',
                'playedWith': 'Ronaldo,Benzema,Kroos',
                'nationality': 'Croácia',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga,Ballon dOr',
                'leaguesPlayed': 'Premier League,La Liga',
                'position': 'Meio-campo',
                'goals': 100,
                'imageName': 'modric.jpg'
            }
        ]
        
        # Insere os jogadores no banco
        added_count = 0
        skipped_count = 0
        
        for player_data in players_data:
            # Verifica se o jogador já existe (por nome)
            existing_player = Player.query.filter_by(name=player_data['name']).first()
            
            if existing_player:
                print(f"⏭️  Jogador {player_data['name']} já existe. Pulando...")
                skipped_count += 1
                continue
            
            # Cria novo jogador
            player = Player(**player_data)
            db.session.add(player)
            added_count += 1
            print(f"✅ Adicionado: {player_data['name']}")
        
        # Salva as alterações
        db.session.commit()
        
        print("\n" + "="*50)
        print(f"✅ Seed concluído!")
        print(f"   📊 Jogadores adicionados: {added_count}")
        print(f"   ⏭️  Jogadores pulados: {skipped_count}")
        print(f"   📈 Total no banco: {Player.query.count()}")
        print("="*50)


if __name__ == '__main__':
    seed_players()

