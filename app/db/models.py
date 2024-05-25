import enum

from sqlalchemy import MetaData, BigInteger, ForeignKey, Integer, DateTime, Date, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, date


class EventStatusEnum(str, enum.Enum):
	green = 'green'
	red = 'red'
	orange = 'orange'

class Base(DeclarativeBase):
	metadata = MetaData()

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)



class Event(Base):
	__tablename__ = 'event'
	name: Mapped[str]
	author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
	invited_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
	event_date: Mapped[datetime] = mapped_column(Date, nullable=True)
	status: Mapped[EventStatusEnum] = mapped_column(
		Enum(EventStatusEnum, native_enum=False, length=255),
	)

	author: Mapped['User'] = relationship(back_populates='my_events', foreign_keys=[author_id])
	invited: Mapped['User'] = relationship(back_populates='invited_events', foreign_keys=[invited_id])



class User(Base):
	__tablename__ = 'user'

	username: Mapped[str] = mapped_column(unique=True)
	email: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str] # hash

	my_events: Mapped[list['Event']] = relationship(back_populates='author', foreign_keys='Event.author_id')
	invited_events: Mapped[list['Event']] = relationship(back_populates='invited', foreign_keys='Event.invited_id')


class Session(Base):
	__tablename__ = 'session'

	token: Mapped[str]
	user_id: Mapped[int]
	valid_datetime: Mapped[datetime] # до какого числа токен работает