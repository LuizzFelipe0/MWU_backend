from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .service import CategoryTypeService
from .schemas import CategoryTypesOutput as CategoryTypesOutScheme, CategoryTypesInput as CategoryTypeInScheme, \
    CategoryTypesUpdateInput as CategoryTypesUpdateInScheme

category_types_router = APIRouter(prefix="/category_types", tags=["Category Types"])


@cbv(category_types_router)
class CategoryTypeController:
    service: CategoryTypeService = Depends()

    @category_types_router.get("/all", response_model=list[CategoryTypesOutScheme])
    def get_all_category_types(self):
        category_types = self.service.get_all_category_types()
        return category_types

    @category_types_router.post("/create", response_model=CategoryTypesOutScheme, status_code=201)
    def create_category_type(self, data: CategoryTypeInScheme):
        category_type = self.service.create_category_type(data)
        return category_type

    @category_types_router.patch("/{category_id}/update", status_code=200)
    def update_category_type(self, category_id: UUID, data: CategoryTypesUpdateInScheme) -> CategoryTypesUpdateInScheme:
        category_type = self.service.update_category_type(id=category_id, data=data)
        return category_type

    @category_types_router.delete("/{category_id}/delete", status_code=204)
    def delete_category_type(self, category_id: UUID):
        category_type = self.service.delete_category_type(id=category_id)
        return category_type
