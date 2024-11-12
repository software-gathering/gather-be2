from fastapi import APIRouter
from crawling.crawler import main as crawling_main
from schemas.crawling import ActivityData
from typing import List

router = APIRouter()


@router.get("/crawl", response_model=List[ActivityData])
async def get_activities():
    activities = crawling_main()

    return activities
