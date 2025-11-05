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
            # Jogadores existentes (mantidos)
            {
                'name': 'NEYMAR JR',
                'playedAt': 'Santos,Barcelona,PSG,Al-Hilal',
                'managedBy': 'Tite,Dunga',
                'playedWith': 'MESSI,SUAREZ,INIESTA',
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
                'playedWith': 'NEYMAR JR,SUAREZ,XAVI,INIESTA',
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
                'playedWith': 'BENZEMA,MODRIC,BALE',
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
                'playedWith': 'NEYMAR JR,MESSI,RAMOS',
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
                'playedWith': 'DE BRUYNE,FODEN',
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
                'playedWith': 'BENZEMA,MODRIC,RODRYGO,BELLINGHAM',
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
                'playedWith': 'SON,LEWANDOWSKI',
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
                'playedWith': 'MANE,VAN DIJK',
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
                'playedWith': 'RONALDO,MODRIC,BALE',
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
                'playedWith': 'RONALDO,BENZEMA,KROOS',
                'nationality': 'Croácia',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga,Ballon dOr',
                'leaguesPlayed': 'Premier League,La Liga',
                'position': 'Meio-campo',
                'goals': 100,
                'imageName': 'modric.jpg'
            },
            {
                'name': 'RODRYGO',
                'playedAt': 'Santos,Real Madrid',
                'managedBy': 'Carlo Ancelotti',
                'playedWith': 'VINI JR,BENZEMA,MODRIC,BELLINGHAM',
                'nationality': 'Brasil',
                'trophiesEarned': 'Champions League,La Liga',
                'leaguesPlayed': 'Brasileirão,La Liga',
                'position': 'Atacante',
                'goals': 80,
                'imageName': 'rodrygo.jpg'
            },
            {
                'name': 'BELLINGHAM',
                'playedAt': 'Birmingham,Borussia Dortmund,Real Madrid',
                'managedBy': 'Carlo Ancelotti',
                'playedWith': 'VINI JR,MODRIC,KROOS',
                'nationality': 'Inglaterra',
                'trophiesEarned': 'Champions League,La Liga',
                'leaguesPlayed': 'Premier League,Bundesliga,La Liga',
                'position': 'Meio-campo',
                'goals': 50,
                'imageName': 'bellingham.jpg'
            },
            {
                'name': 'DE BRUYNE',
                'playedAt': 'Genk,Werder Bremen,Chelsea,Wolfsburg,Manchester City',
                'managedBy': 'Pep Guardiola',
                'playedWith': 'HAALAND,FODEN',
                'nationality': 'Bélgica',
                'trophiesEarned': 'Champions League,Premier League',
                'leaguesPlayed': 'Premier League,Bundesliga',
                'position': 'Meio-campo',
                'goals': 150,
                'imageName': 'debruyne.jpg'
            },
            {
                'name': 'LEWANDOWSKI',
                'playedAt': 'Lech Poznan,Borussia Dortmund,Bayern Munich,Barcelona',
                'managedBy': 'Pep Guardiola,Hansi Flick',
                'playedWith': 'Muller,Neuer,Goretzka,Kane',
                'nationality': 'Polônia',
                'trophiesEarned': 'Champions League,Bundesliga,La Liga',
                'leaguesPlayed': 'Bundesliga,La Liga',
                'position': 'Atacante',
                'goals': 600,
                'imageName': 'lewandowski.jpg'
            },
            {
                'name': 'SUAREZ',
                'playedAt': 'Nacional,Groningen,Ajax,Liverpool,Barcelona,Atletico Madrid',
                'managedBy': 'Luis Enrique,Diego Simeone',
                'playedWith': 'MESSI,NEYMAR JR,INIESTA,GRIEZMANN',
                'nationality': 'Uruguai',
                'trophiesEarned': 'Champions League,La Liga,Premier League',
                'leaguesPlayed': 'Premier League,La Liga,Eredivisie',
                'position': 'Atacante',
                'goals': 500,
                'imageName': 'suarez.jpg'
            },
            {
                'name': 'INIESTA',
                'playedAt': 'Barcelona,Vissel Kobe',
                'managedBy': 'Pep Guardiola,Luis Enrique',
                'playedWith': 'MESSI,XAVI',
                'nationality': 'Espanha',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga',
                'leaguesPlayed': 'La Liga,J-League',
                'position': 'Meio-campo',
                'goals': 100,
                'imageName': 'iniesta.jpg'
            },
            {
                'name': 'XAVI',
                'playedAt': 'Barcelona,Al Sadd',
                'managedBy': 'Pep Guardiola',
                'playedWith': 'MESSI,INIESTA',
                'nationality': 'Espanha',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga',
                'leaguesPlayed': 'La Liga',
                'position': 'Meio-campo',
                'goals': 80,
                'imageName': 'xavi.jpg'
            },
            {
                'name': 'RAMOS',
                'playedAt': 'Sevilla,Real Madrid,PSG',
                'managedBy': 'Zidane,Carlo Ancelotti',
                'playedWith': 'RONALDO,BENZEMA,MODRIC,MBAPPE',
                'nationality': 'Espanha',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga',
                'leaguesPlayed': 'La Liga,Ligue 1',
                'position': 'Zagueiro',
                'goals': 100,
                'imageName': 'ramos.jpg'
            },
            {
                'name': 'BALE',
                'playedAt': 'Southampton,Tottenham,Real Madrid,LA Galaxy',
                'managedBy': 'Zidane,Carlo Ancelotti',
                'playedWith': 'RONALDO,BENZEMA,MODRIC',
                'nationality': 'País de Gales',
                'trophiesEarned': 'Champions League,La Liga',
                'leaguesPlayed': 'Premier League,La Liga,MLS',
                'position': 'Atacante',
                'goals': 200,
                'imageName': 'bale.jpg'
            },
            {
                'name': 'KROOS',
                'playedAt': 'Bayern Munich,Bayer Leverkusen,Real Madrid',
                'managedBy': 'Carlo Ancelotti,Zidane',
                'playedWith': 'MODRIC,BENZEMA,RONALDO',
                'nationality': 'Alemanha',
                'trophiesEarned': 'Copa do Mundo,Champions League,La Liga',
                'leaguesPlayed': 'Bundesliga,La Liga',
                'position': 'Meio-campo',
                'goals': 80,
                'imageName': 'kroos.jpg'
            },
            {
                'name': 'SON',
                'playedAt': 'Hamburger SV,Bayer Leverkusen,Tottenham',
                'managedBy': 'Mauricio Pochettino',
                'playedWith': 'KANE',
                'nationality': 'Coreia do Sul',
                'trophiesEarned': 'Premier League',
                'leaguesPlayed': 'Premier League,Bundesliga',
                'position': 'Atacante',
                'goals': 200,
                'imageName': 'son.jpg'
            },
            {
                'name': 'MANE',
                'playedAt': 'Metz,Salzburg,Southampton,Liverpool,Bayern Munich,Al Nassr',
                'managedBy': 'Jurgen Klopp',
                'playedWith': 'M. SALAH,VAN DIJK',
                'nationality': 'Senegal',
                'trophiesEarned': 'Champions League,Premier League,Bundesliga',
                'leaguesPlayed': 'Premier League,Bundesliga',
                'position': 'Atacante',
                'goals': 250,
                'imageName': 'mane.jpg'
            },
            {
                'name': 'VAN DIJK',
                'playedAt': 'Groningen,Celtic,Southampton,Liverpool',
                'managedBy': 'Jurgen Klopp',
                'playedWith': 'M. SALAH,MANE',
                'nationality': 'Holanda',
                'trophiesEarned': 'Champions League,Premier League',
                'leaguesPlayed': 'Premier League,Scottish Premiership',
                'position': 'Zagueiro',
                'goals': 50,
                'imageName': 'vandijk.jpg'
            },
            {
                'name': 'FODEN',
                'playedAt': 'Manchester City',
                'managedBy': 'Pep Guardiola',
                'playedWith': 'DE BRUYNE,HAALAND',
                'nationality': 'Inglaterra',
                'trophiesEarned': 'Champions League,Premier League',
                'leaguesPlayed': 'Premier League',
                'position': 'Meio-campo',
                'goals': 100,
                'imageName': 'foden.jpg'
            },
            {
                'name': 'GRIEZMANN',
                'playedAt': 'Real Sociedad,Atletico Madrid,Barcelona,Atletico Madrid',
                'managedBy': 'Diego Simeone,Luis Enrique',
                'playedWith': 'SUAREZ',
                'nationality': 'França',
                'trophiesEarned': 'Copa do Mundo,La Liga',
                'leaguesPlayed': 'La Liga',
                'position': 'Atacante',
                'goals': 300,
                'imageName': 'griezmann.jpg'
            },
            {
                'name': 'COURTOIS',
                'playedAt': 'Genk,Atletico Madrid,Chelsea,Real Madrid',
                'managedBy': 'Carlo Ancelotti,Zidane',
                'playedWith': 'RAMOS,MODRIC,BENZEMA',
                'nationality': 'Bélgica',
                'trophiesEarned': 'Champions League,La Liga,Premier League',
                'leaguesPlayed': 'La Liga,Premier League',
                'position': 'Goleiro',
                'goals': 0,
                'imageName': 'courtois.jpg'
            },
            {
                'name': 'PEDRI',
                'playedAt': 'Las Palmas,Barcelona',
                'managedBy': 'Xavi',
                'playedWith': 'MESSI',
                'nationality': 'Espanha',
                'trophiesEarned': 'La Liga',
                'leaguesPlayed': 'La Liga',
                'position': 'Meio-campo',
                'goals': 30,
                'imageName': 'pedri.jpg'
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

