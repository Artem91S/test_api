from pydantic import BaseModel


class PlanInsertResponse(BaseModel):
    message: str
