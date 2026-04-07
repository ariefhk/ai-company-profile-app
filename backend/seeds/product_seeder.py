"""Seed product categories and products."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.page import ContentStatus
from models.product import Product, ProductCategory

CATEGORIES = [
    {"name": "Software Development", "slug": "software-development"},
    {"name": "Cloud Services", "slug": "cloud-services"},
    {"name": "Consulting", "slug": "consulting"},
]

PRODUCTS = [
    {
        "category_slug": "software-development",
        "name": "Custom Web Application",
        "slug": "custom-web-application",
        "description": "Pengembangan aplikasi web kustom sesuai kebutuhan bisnis Anda.",
        "price_original": Decimal("50000000.00"),
        "price_underline": Decimal("45000000.00"),
        "status": ContentStatus.published,
    },
    {
        "category_slug": "software-development",
        "name": "Mobile App Development",
        "slug": "mobile-app-development",
        "description": "Pengembangan aplikasi mobile untuk Android dan iOS.",
        "price_original": Decimal("75000000.00"),
        "price_underline": Decimal("65000000.00"),
        "status": ContentStatus.published,
    },
    {
        "category_slug": "cloud-services",
        "name": "Cloud Migration",
        "slug": "cloud-migration",
        "description": "Migrasi infrastruktur ke cloud dengan zero downtime.",
        "price_original": Decimal("30000000.00"),
        "status": ContentStatus.published,
    },
    {
        "category_slug": "consulting",
        "name": "IT Strategy Consulting",
        "slug": "it-strategy-consulting",
        "description": "Konsultasi strategi IT untuk transformasi digital perusahaan Anda.",
        "price_original": Decimal("20000000.00"),
        "status": ContentStatus.published,
    },
]


async def run(db: AsyncSession) -> None:
    result = await db.execute(select(ProductCategory))
    if result.scalars().first() is not None:
        return

    category_map = {}
    for cat_data in CATEGORIES:
        category = ProductCategory(**cat_data)
        db.add(category)
        category_map[cat_data["slug"]] = category

    await db.flush()

    for prod_data in PRODUCTS:
        slug = prod_data.pop("category_slug")
        prod_data["category_id"] = category_map[slug].id
        db.add(Product(**prod_data))
