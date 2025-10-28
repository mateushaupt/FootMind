from extensions import db

class User(db.Model):
    __tablename__ = 'USER'
    
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    # A senha deve ser armazenada como hash (ex: usando String(100) para um hash seguro)
    password = db.Column(db.String(100), nullable=False)
    
    # Relação com USER_GAMES (O usuário tem muitos registros de jogos)
    games = db.relationship('UserGame', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.nickname}>'