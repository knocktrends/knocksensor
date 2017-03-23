from sqlalchemy import Column, BigInteger, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from knockserver.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    hashed_pass = Column(String)
    salt = Column(String)
    username = Column(String)
    ifttt_secret = Column(String)

class AccessPattern(Base):
    __tablename__ = 'accesspattern'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    active = Column(Boolean)
    expiration = Column(BigInteger)
    max_uses = Column(BigInteger)
    name = Column(String)
    pending = Column(Boolean)
    used_count = Column(BigInteger)
    pattern_pieces = relationship("patternpiece", backref="accesspattern")

    @property
    def serialize(self):
        """Return an easily serialized version of the object."""
        return {
            "id": self.id,
            "active": self.active,
            "name": self.name,
            "pending": self.pending
        }


class PatternPiece(Base):
    __tablename__ = 'patternpiece'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    length = Column(BigInteger)
    order = Column(BigInteger)
    pattern_id = Column(Integer, ForeignKey('accesspattern.id'))
    pressed = Column(Boolean)
