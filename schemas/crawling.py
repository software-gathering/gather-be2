from pydantic import BaseModel
from typing import Optional
from datetime import date


class ActivityData(BaseModel):
    ex_name: str
    ex_link: str
    ex_host: str
    ex_image: str
    ex_start: Optional[date]
    ex_end: Optional[date]  # 종료 날짜 없는 상황도 있음 (모집시 마감)
    ex_flag: int  # 대외활동 크롤링 위치 구분을 위한 플래그
