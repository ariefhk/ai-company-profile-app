"""Seed SEO metadata entries."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.seo_metadata import SeoMetadata

# Fixed UUIDs so other seeders can reference them
SEO_COMPANY_ID = uuid.UUID("a0000000-0000-0000-0000-000000000001")
SEO_HOME_PAGE_ID = uuid.UUID("a0000000-0000-0000-0000-000000000002")
SEO_ABOUT_PAGE_ID = uuid.UUID("a0000000-0000-0000-0000-000000000003")

SEO_ENTRIES = [
    {
        "id": SEO_COMPANY_ID,
        "meta_title": "PT Maju Bersama - Company Profile",
        "meta_description": "PT Maju Bersama adalah perusahaan teknologi terdepan di Indonesia.",
        "og_title": "PT Maju Bersama",
        "og_description": "Perusahaan teknologi terdepan di Indonesia.",
        "robots": "index,follow",
    },
    {
        "id": SEO_HOME_PAGE_ID,
        "meta_title": "Home - PT Maju Bersama",
        "meta_description": "Selamat datang di PT Maju Bersama.",
        "og_title": "Home - PT Maju Bersama",
        "robots": "index,follow",
    },
    {
        "id": SEO_ABOUT_PAGE_ID,
        "meta_title": "About Us - PT Maju Bersama",
        "meta_description": "Tentang PT Maju Bersama.",
        "og_title": "About Us - PT Maju Bersama",
        "robots": "index,follow",
    },
]


async def run(db: AsyncSession) -> None:
    for data in SEO_ENTRIES:
        result = await db.execute(
            select(SeoMetadata).where(SeoMetadata.id == data["id"])
        )
        if result.scalar_one_or_none() is None:
            db.add(SeoMetadata(**data))
