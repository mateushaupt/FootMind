from extensions import db

class HistoryGame(db.Model):
    __tablename__ = 'HISTORY_GAMES'
    
    id = db.Column(db.Integer, primary_key=True)
    # TIMESTAMP ou DateTime são mais adequados, mas String (TEXT) funciona bem no SQLite para datas
    # Removido unique=True porque a combinação dateCreated + configHash deve ser única, não apenas dateCreated
    dateCreated = db.Column(db.String(50), nullable=False)
    configHash = db.Column(db.String(500), nullable=False)
    
    # Relação com USER_GAMES
    user_attempts = db.relationship('UserGame', backref='history_game', lazy=True)
    
    # Constraint única na combinação de dateCreated e configHash
    __table_args__ = (
        db.UniqueConstraint('dateCreated', 'configHash', name='uq_history_date_config'),
    )

    def __repr__(self):
        return f'<HistoryGame {self.id} - {self.dateCreated}>'