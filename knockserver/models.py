from sqlalchemy import Column, BigInteger, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from knockserver.database import Base

class ExampleObject(Base):
    __tablename__ = 'example_objects'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    example_string = Column(String)

