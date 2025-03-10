from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class GitCommand(Base):
    __tablename__ = 'git_commands'

    id = Column(Integer, primary_key=True)
    command = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))

    user = relationship('UserProfile', back_populates='git_commands')
