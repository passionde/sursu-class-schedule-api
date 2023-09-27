import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Schedule

# расписание звонков для основных занятий
BASE_TIMETABLE = {
    '1': '08:30-09:50',
    '2': '10:00-11:20',
    '3': '11:30-12:50',
    '4': '13:20-14:40',
    '5': '14:50-16:10',
    '6': '16:20-17:40',
    '7': '18:00-19:20',
    '8': '19:30-20:50'
}

# расписание звонков для занятий по ФК
PHYSICAL_TIMETABLE = {
    '1': '09:00-10:20',
    '2': '10:30-11:50',
    '3': '12:00-13:20',
    '4': '13:30-14:50',
    '5': '15:00-16:25',
    '6': '16:30-17:50'
}


def get_lesson_time(number, subject):
    answer = BASE_TIMETABLE.get(number, '')
    if re.match(r".*культур\D и спорт.*", subject) is not None:
        answer = PHYSICAL_TIMETABLE.get(number, '')

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