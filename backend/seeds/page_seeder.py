"""Seed pages with sections and section items."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.page import ContentStatus, Page
from models.section import RefType, Section, SectionItem, SectionType
from seeds.seo_metadata_seeder import SEO_ABOUT_PAGE_ID, SEO_HOME_PAGE_ID

HOME_PAGE_ID = uuid.UUID("c0000000-0000-0000-0000-000000000001")
ABOUT_PAGE_ID = uuid.UUID("c0000000-0000-0000-0000-000000000002")

PAGES = [
    {
        "id": HOME_PAGE_ID,
        "seo_id": SEO_HOME_PAGE_ID,
        "title": "Home",
        "slug": "home",
        "body": "Selamat datang di PT Maju Bersama.",
        "status": ContentStatus.published,
    },
    {
        "id": ABOUT_PAGE_ID,
        "seo_id": SEO_ABOUT_PAGE_ID,
        "title": "About Us",
        "slug": "about",
        "body": "Tentang perusahaan kami.",
        "status": ContentStatus.published,
    },
]

SECTIONS = [
    {
        "page_id": HOME_PAGE_ID,
        "type": SectionType.banner,
        "title": "Solusi Digital untuk Bisnis Anda",
        "subtitle": "Inovasi teknologi yang mengubah cara Anda berbisnis",
        "sort_order": 0,
        "is_visible": True,
        "settings": {"background_color": "#1a1a2e", "text_color": "#ffffff"},
    },
    {
        "page_id": HOME_PAGE_ID,
        "type": SectionType.product_list,
        "title": "Layanan Kami",
        "subtitle": "Solusi terbaik untuk kebutuhan digital Anda",
        "sort_order": 1,
        "is_visible": True,
    },
    {
        "page_id": HOME_PAGE_ID,
        "type": SectionType.client_list,
        "title": "Klien Kami",
        "subtitle": "Dipercaya oleh perusahaan terkemuka",
        "sort_order": 2,
        "is_visible": True,
    },
    {
        "page_id": HOME_PAGE_ID,
        "type": SectionType.testimonial,
        "title": "Testimoni",
        "subtitle": "Apa kata klien kami",
        "sort_order": 3,
        "is_visible": True,
    },
    {
        "page_id": ABOUT_PAGE_ID,
        "type": SectionType.about,
        "title": "Tentang Kami",
        "content": "PT Maju Bersama berdiri sejak 2010 dengan visi menjadi perusahaan teknologi terdepan.",
        "sort_order": 0,
        "is_visible": True,
    },
    {
        "page_id": ABOUT_PAGE_ID,
        "type": SectionType.contact,
        "title": "Hubungi Kami",
        "subtitle": "Kami siap membantu Anda",
        "sort_order": 1,
        "is_visible": True,
    },
]

SECTION_ITEMS = [
    {
        "section_index": 0,
        "ref_type": None,
        "label": "Mulai Sekarang",
        "url": "/contact",
        "sort_order": 0,
    },
    {
        "section_index": 0,
        "ref_type": None,
        "label": "Pelajari Lebih Lanjut",
        "url": "/about",
        "sort_order": 1,
    },
]


async def run(db: AsyncSession) -> None:
    result = await db.execute(select(Page).where(Page.id == HOME_PAGE_ID))
    if result.scalar_one_or_none() is not None:
        return

    for page_data in PAGES:
        db.add(Page(**page_data))

    sections = []
    for section_data in SECTIONS:
        section = Section(**section_data)
        db.add(section)
        sections.append(section)

    await db.flush()

    for item_data in SECTION_ITEMS:
        idx = item_data.pop("section_index")
        item_data["section_id"] = sections[idx].id
        db.add(SectionItem(**item_data))
