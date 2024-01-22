from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class CommonParams(BaseModel):
    limit: Annotated[int, Query(gt=0)]
    offset: Annotated[int, Query(ge=0)]
