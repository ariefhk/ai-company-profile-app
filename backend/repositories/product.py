from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.page import ContentStatus
from models.product import Product, ProductCategory
from repositories.base import BaseRepository


class ProductCategoryRepository(BaseRepository[ProductCategory, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductCategory, db)

    async def find_by_slug(self, slug: str) -> ProductCategory | None:
        return await self.find_one_by(ProductCategory.slug == slug)

    async def find_with_products(self, id: UUID) -> ProductCategory | None:
        return await self.find_by_id_with(id, ProductCategory.products)


class ProductRepository(BaseRepository[Product, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def find_by_slug(self, slug: str) -> Product | None:
        return await self.find_one_by(Product.slug == slug)

    async def find_by_category(
        self, category_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[Product]:
        return await self.find_many_by(
            Product.category_id == category_id, skip=skip, limit=limit
        )

    async def find_published(
        self, skip: int = 0, limit: int = 50
    ) -> list[Product]:
        return await self.find_many_by(
            Product.status == ContentStatus.published, skip=skip, limit=limit
        )

    async def find_with_relations(self, id: UUID) -> Product | None:
        return await self.find_by_id_with(
            id, Product.seo, Product.category
        )
