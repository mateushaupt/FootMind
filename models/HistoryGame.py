from extensions import db

class HistoryGame(db.Model):
    __tablename__ = 'HISTORY_GAMES'
    
    id = db.Column(db.Integer, primary_key=True)
    # TIMESTAMP ou DateTime são mais adequados, mas String (TEXT) funciona bem no SQLite para datas
    dateCreated = db.Column(db.String(50), unique=True, nullable=False)
    configHash = db.Column(db.String(200), nullable=False)
    
    # Relação com USER_GAMES
    user_attempts = db.relationship('UserGame', backref='history_game', lazy=True)

    def __repr__(self):
        return f'<HistoryGame {self.id} - {self.dateCreated}>'