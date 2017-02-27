from sqlalchemy import Column, BigInteger, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from knockserver.database import Base

class ExampleObject(Base):
    __tablename__ = 'example_object'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    example_string = Column(String)

class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    hashedPass = Column(String)
    salt = Column(String)
    username = Column(String)

class AccessPattern(Base):
    __tablename__ = 'accesspattern'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    active = Column(Boolean)
    expiration = Column(BigInteger().with_variant(Integer, "sqlite"))
    maxUses = Column(BigInteger().with_variant(Integer, "sqlite"))
    name = Column(String)
    usedCount = Column(BigInteger().with_variant(Integer, "sqlite"))
    patternPieces = relationship("patternpiece", backref="accesspattern")

class PatternPiece(Base):
    __tablename__ = 'patternpiece'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    length = Column(BigInteger().with_variant(Integer, "sqlite"))
    order = Column(BigInteger().with_variant(Integer, "sqlite"))
    patternID = Column(Integer, ForeignKey('accesspattern.id'))
    pressed = Column(Boolean)
