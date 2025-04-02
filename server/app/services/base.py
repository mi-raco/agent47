from typing import Generic, TypeVar, Type, Optional, List, Any
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.models.base import BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncIOMotorDatabase):
        self.model = model
        self.db = db
        self.collection = db[model.__collection__]

    async def get(self, id: str) -> Optional[ModelType]:
        if (doc := await self.collection.find_one({"_id": id})) is not None:
            return self.model(**doc)
        return None

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100, query: dict = None
    ) -> List[ModelType]:
        cursor = self.collection.find(query or {})
        cursor = cursor.skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.model(**doc) for doc in documents]

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        result = await self.collection.insert_one(db_obj.dict(by_alias=True))
        return await self.get(str(result.inserted_id))

    async def update(
        self, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.collection.update_one(
            {"_id": db_obj.id}, {"$set": db_obj.dict(exclude={"id"})}
        )
        return await self.get(str(db_obj.id))

    async def delete(self, *, id: str) -> bool:
        result = await self.collection.delete_one({"_id": id})
        return result.deleted_count > 0

    async def exists(self, *, id: str) -> bool:
        return await self.collection.count_documents({"_id": id}) > 0 