from db.database import Base
from sqlalchemy import Column, Integer, String, CheckConstraint, Text


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_number = Column(String(7))
    lesson_number = Column(Integer)
    day_week = Column(String(2), CheckConstraint("day_week IN ('пн', 'вт', 'ср', 'чт', 'пт', 'сб')"))
    type_week = Column(Integer, CheckConstraint('type_week IN (0, 1, 2)'))
    subgroup_number = Column(Integer, CheckConstraint('subgroup_number >= 0 AND subgroup_number <= 3'))
    info = Column(Text)
