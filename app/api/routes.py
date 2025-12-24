from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import tempfile
import json

from app.validators.parser import parse_presentation
from app.validators.rules import RULES
from app.db.database import AsyncSessionLocal
from app.db.models import Validation, Issue

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/validate")
async def validate(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    slides = parse_presentation(path)

    validation = Validation(filename=file.filename)
    db.add(validation)
    await db.flush()

    errors = []

    for slide in slides:
        slide_number = slide.get("slide_number")
        for rule_name, rule in RULES:
            result = rule(slide)
            if result:
                # Если вернулся список ошибок — разворачиваем их
                if isinstance(result, list):
                    for item in result:
                        message_text = json.dumps(item)
                        issue = Issue(
                            validation_id=validation.id,
                            slide_number=item.get("slide", slide_number),
                            rule=item.get("rule", rule_name),
                            message=message_text
                        )
                        db.add(issue)
                        errors.append(item)
                else:
                    # Если одна ошибка — сохраняем как строку
                    message_text = str(result)
                    issue = Issue(
                        validation_id=validation.id,
                        slide_number=slide_number,
                        rule=rule_name,
                        message=message_text
                    )
                    db.add(issue)
                    errors.append({
                        "slide": slide_number,
                        "rule": rule_name,
                        "message": message_text
                    })

    await db.commit()
    return {"errors": errors}

@router.get("/validations")
async def validations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Validation))
    return result.scalars().all()

@router.get("/validations/{validation_id}")
async def validation_detail(validation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Issue).where(Issue.validation_id == validation_id)
    )
    return result.scalars().all()
