import datetime

import pytz
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.security import HeaderInitParams
from api.schemas.schedule import GetScheduleRequest
from db.database import get_async_session
import db.methods as methods

router = APIRouter(prefix="/schedule", tags=["Расписание"])
surgut_timezone = pytz.timezone('Asia/Yekaterinburg')


@router.post("/get-schedule-group")
async def get_schedule_group(
        _: HeaderInitParams,
        params: GetScheduleRequest,
        session: AsyncSession = Depends(get_async_session)
):
    g = await methods.get_schedule(session, params.group_number)
    return {"group_number": params.group_number, "schedule": g}


@router.get("/get-all-groups-numbers")
async def get_all_groups_numbers(
        _: HeaderInitParams,
        session: AsyncSession = Depends(get_async_session)
):
    groups = await methods.get_all_group_numbers(session)
    return {"total": len(groups), "groups_numbers": groups}


@router.get("/get-type-week")
async def get_type_week(_: HeaderInitParams):
    current_date = datetime.datetime.now(surgut_timezone).date()
    num_or_den = int(current_date.strftime("%V")) % 2

    if current_date.weekday() == 6:  # Если воскресенье, то следующая неделя
        num_or_den = 1 - num_or_den

    return {"type_week": 'numerator' if num_or_den else 'denominator'}
