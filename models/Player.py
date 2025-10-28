from extensions import db  # Assumindo que você inicializou db em extensions.py

class Player(db.Model):
    __tablename__ = 'PLAYER'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # Campos que contêm múltiplos valores serão armazenados como strings separadas (ex: por vírgulas)
    playedAt = db.Column(db.String(150))
    managedBy = db.Column(db.String(150))
    playedWith = db.Column(db.String(200))
    nationality = db.Column(db.String(20))
    trophiesEarned = db.Column(db.String(200))
    leaguesPlayed = db.Column(db.String(200))
    position = db.Column(db.String(20))
    goals = db.Column(db.Integer)
    imageName = db.Column(db.String(80))

    def __repr__(self):
        return f'<Player {self.name}>'