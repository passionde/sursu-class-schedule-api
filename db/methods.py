import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from db.models import Schedule


def get_lesson_time(number, subject):
    answer = settings.BASE_TIMETABLE.get(number, '')
    if re.match(r".*культур\D и спорт.*", subject) is not None:
        answer = settings.PHYSICAL_TIMETABLE.get(number, '')

    return answer


def cook_data_schedule(data: list[dict]):
    result = {"numerator": {}, "denominator": {}}

    def inner(type_week: str, obj: Schedule):
        if obj.day_week not in result[type_week]:
            result[type_week][obj.day_week] = []
        result[type_week][obj.day_week].append({
            "lesson_number": obj.lesson_number,
            "subgroup_number": obj.subgroup_number,
            "info": obj.info,
            "lesson_time": get_lesson_time(str(obj.lesson_number), obj.info)
        })

    item: Schedule
    for item in data:
        if item.type_week in (0, 1):
            inner("numerator", item)
        if item.type_week in (0, 2):
            inner("denominator", item)

    return result


async def get_schedule(session: AsyncSession, group_number: str):
    result = await session.execute(
        select(Schedule)
        .filter(Schedule.group_number == group_number)
    )
    return cook_data_schedule(list(result.scalars().all()))


async def get_all_group_numbers(session: AsyncSession):
    result = await session.execute(
        select(Schedule.group_number).distinct(Schedule.group_number)
    )
    return list(result.scalars().all())