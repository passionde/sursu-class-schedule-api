from pydantic import BaseModel, Field


class GetScheduleRequest(BaseModel):
    """Модель запроса для получения расписания группы"""
    group_number: str = Field(
        ...,
        title="Номер группы",
        example="606-12",
    )
