"""Seed company with contacts, social links, and addresses."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.company import (
    Company,
    CompanyAddress,
    CompanyContact,
    CompanySocialLink,
    ContactType,
    SocialPlatform,
)
from seeds.seo_metadata_seeder import SEO_COMPANY_ID

COMPANY_ID = uuid.UUID("b0000000-0000-0000-0000-000000000001")

COMPANY = {
    "id": COMPANY_ID,
    "seo_id": SEO_COMPANY_ID,
    "name": "PT Maju Bersama",
    "tagline": "Inovasi untuk Masa Depan",
    "vision": "Menjadi perusahaan teknologi terdepan di Asia Tenggara.",
    "mission": "Memberikan solusi teknologi terbaik untuk setiap klien kami.",
    "description": (
        "PT Maju Bersama adalah perusahaan teknologi yang berdiri sejak 2010. "
        "Kami menyediakan solusi digital untuk berbagai industri."
    ),
    "founded_year": 2010,
}

CONTACTS = [
    {
        "company_id": COMPANY_ID,
        "type": ContactType.phone,
        "label": "Kantor Pusat",
        "value": "+62-21-5551234",
        "is_primary": True,
        "sort_order": 0,
    },
    {
        "company_id": COMPANY_ID,
        "type": ContactType.email,
        "label": "General",
        "value": "info@majubersama.co.id",
        "is_primary": True,
        "sort_order": 1,
    },
    {
        "company_id": COMPANY_ID,
        "type": ContactType.whatsapp,
        "label": "Customer Service",
        "value": "+62-812-3456-7890",
        "is_primary": False,
        "sort_order": 2,
    },
]

SOCIAL_LINKS = [
    {
        "company_id": COMPANY_ID,
        "platform": SocialPlatform.instagram,
        "url": "https://instagram.com/majubersama",
        "sort_order": 0,
    },
    {
        "company_id": COMPANY_ID,
        "platform": SocialPlatform.linkedin,
        "url": "https://linkedin.com/company/majubersama",
        "sort_order": 1,
    },
    {
        "company_id": COMPANY_ID,
        "platform": SocialPlatform.youtube,
        "url": "https://youtube.com/@majubersama",
        "sort_order": 2,
    },
]

ADDRESSES = [
    {
        "company_id": COMPANY_ID,
        "label": "Kantor Pusat",
        "street": "Jl. Sudirman No. 123, Gedung Cyber Lt. 5",
        "city": "Jakarta Selatan",
        "state": "DKI Jakarta",
        "postal_code": "12190",
        "country": "Indonesia",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "is_primary": True,
    },
    {
        "company_id": COMPANY_ID,
        "label": "Kantor Cabang",
        "street": "Jl. Ahmad Yani No. 45",
        "city": "Surabaya",
        "state": "Jawa Timur",
        "postal_code": "60234",
        "country": "Indonesia",
        "latitude": -7.2575,
        "longitude": 112.7521,
        "is_primary": False,
    },
]


async def run(db: AsyncSession) -> None:
    result = await db.execute(
        select(Company).where(Company.id == COMPANY_ID)
    )
    if result.scalar_one_or_none() is not None:
        return

    db.add(Company(**COMPANY))
    for contact in CONTACTS:
        db.add(CompanyContact(**contact))
    for link in SOCIAL_LINKS:
        db.add(CompanySocialLink(**link))
    for address in ADDRESSES:
        db.add(CompanyAddress(**address))
