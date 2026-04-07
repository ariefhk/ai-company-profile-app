"""Seed clients and testimonials."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.client import Client, ClientStatus, ClientTestimonial
from seeds.company_seeder import COMPANY_ID

CLIENTS = [
    {
        "company_id": COMPANY_ID,
        "name": "Bank Nasional Indonesia",
        "website_url": "https://bni.co.id",
        "description": "Salah satu bank terbesar di Indonesia.",
        "industry": "Perbankan",
        "status": ClientStatus.featured,
        "sort_order": 0,
    },
    {
        "company_id": COMPANY_ID,
        "name": "Telkom Indonesia",
        "website_url": "https://telkom.co.id",
        "description": "Perusahaan telekomunikasi terbesar di Indonesia.",
        "industry": "Telekomunikasi",
        "status": ClientStatus.featured,
        "sort_order": 1,
    },
    {
        "company_id": COMPANY_ID,
        "name": "Pertamina",
        "website_url": "https://pertamina.com",
        "description": "Perusahaan energi nasional.",
        "industry": "Energi",
        "status": ClientStatus.active,
        "sort_order": 2,
    },
]

TESTIMONIALS = [
    {
        "author_name": "Budi Santoso",
        "author_role": "CTO, Bank Nasional Indonesia",
        "content": "PT Maju Bersama membantu kami melakukan transformasi digital dengan sangat profesional.",
        "rating": 5,
        "is_published": True,
    },
    {
        "author_name": "Siti Rahayu",
        "author_role": "VP Engineering, Telkom Indonesia",
        "content": "Solusi yang diberikan sangat inovatif dan sesuai kebutuhan kami.",
        "rating": 5,
        "is_published": True,
    },
]


async def run(db: AsyncSession) -> None:
    result = await db.execute(
        select(Client).where(Client.company_id == COMPANY_ID)
    )
    if result.scalars().first() is not None:
        return

    clients = []
    for data in CLIENTS:
        client = Client(**data)
        db.add(client)
        clients.append(client)

    await db.flush()

    for i, testimonial_data in enumerate(TESTIMONIALS):
        if i < len(clients):
            testimonial_data["client_id"] = clients[i].id
            db.add(ClientTestimonial(**testimonial_data))
