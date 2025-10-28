from extensions import db
# Importar classes para definir as chaves estrangeiras
from .User import User 
from .HistoryGame import HistoryGame 

class UserGame(db.Model):
    __tablename__ = 'USER_GAMES'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Chaves Estrangeiras (Foreign Keys)
    userId = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False)
    gameId = db.Column(db.Integer, db.ForeignKey('HISTORY_GAMES.id'), nullable=False)
    
    # TINYINT mapeado para Integer (0 = Derrota, 1 = Vitória)
    result = db.Column(db.Integer) 

    def __repr__(self):
        return f'<UserGame UserID:{self.userId} GameID:{self.gameId} Result:{self.result}>'