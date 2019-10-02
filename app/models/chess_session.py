from sqlalchemy import Column, String, Float, Integer

from app.app import Base

TABLE_NAME = 'chess_session'
PRIMARY_KEY = 'id'
TABLE_NAME_AND_PRIMARY_KEY = TABLE_NAME+"."+PRIMARY_KEY

class ChessSession(Base):

    __tablename__ = TABLE_NAME
    id = Column(PRIMARY_KEY, Integer, primary_key=True)
    time_updated = Column(Float)
    cookie = Column(String)
    fen = Column(String)
    injected_argument_counter = Column(Integer)
    nr_of_player_moves = Column(Integer)

