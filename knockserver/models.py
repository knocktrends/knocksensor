from sqlalchemy import Column, BigInteger, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from knockserver.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    hashed_pass = Column(String)
    ifttt_secret = Column(String)
    salt = Column(String)
    username = Column(String)

class AccessPattern(Base):
    __tablename__ = 'accesspattern'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    active = Column(Boolean)
    expiration = Column(BigInteger)
    max_uses = Column(BigInteger)
    name = Column(String)
    pattern_pieces = relationship("patternpiece", backref="accesspattern")
    pending = Column(Boolean)
    used_count = Column(BigInteger)

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

class NotificationPreferences(Base):
    __tablename__ = 'notificationpreferences'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    expire_threshold = Column(BigInteger) # Notification sent if there is less time remaining than this threshold in minutes
    failed_attempts_threshold = Column(BigInteger) # Notification sent if failures greater than this value
    name = Column(String)
    remaining_use_threshold = Column(BigInteger) # Notification sent if uses less than this value
    send_no_earlier = Column(BigInteger) # Minutes from previous midnight (midnight = 0, 01:00 = 60)
    send_no_later = Column(BigInteger) # Minutes from previous midnight (midnight = 0, 23:00 = 1380) and must be within one day
    success_threshold = Column(BigInteger) # If used_count % this == 0 send notification
    failure_endpoint = Column(String)

class ProfileJoin(Base):
    __tablename__ = 'profilejoin'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id')) # Can be null (if null will be associated with all patterns for the user)
    pattern_id = Column(Integer, ForeignKey('accesspattern.id')) # Can be null (if null will be associated with all patterns for the user)
    perference_id = Column(Integer, ForeignKey('notificationpreferences.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

class Device(Base):
    __tablename__ = 'device'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    failure_count = Column(BigInteger)
    identifier = Column(String)
    name = Column(String)
