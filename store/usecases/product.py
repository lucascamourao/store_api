from datetime import datetime
from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import DuplicateEntryException, NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        # Check if a product with the same name but a different price exists
        existing_product = await self.collection.find_one(
            {"name": body.name, "price": {"$ne": body.price}}
        )
        if existing_product:
            raise DuplicateEntryException(
                "Product with the same name but different price already exists"
            )

        product_model = ProductModel(**body.model_dump())
        # Create: Map an exception in case an insertion error occurs and capture it in the controller
        try:
            await self.collection.insert_one(product_model.model_dump())
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateEntryException("Product already exists! ")

        return ProductOut(**product_model.model_dump())

    """
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        # Create: Map an exception in case an insertion error occurs and capture it in the controller
        try:
            await self.collection.insert_one(product_model.model_dump())
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateEntryException("Product already exists! ")

        return ProductOut(**product_model.model_dump())
    """

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(
        self, min_price: float = None, max_price: float = None
    ) -> List[ProductOut]:
        filter_query = {}

        if min_price is not None and max_price is not None:
            filter_query["price"] = {"$gt": min_price, "$lt": max_price}

        # Fetch products matching the filter criteria
        cursor = self.collection.find(filter_query)
        products = [
            ProductOut(**product) async for product in await cursor.to_list(length=None)
        ]

        return products

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        body_dict = body.model_dump(exclude_none=True)
        body_dict["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body_dict},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
