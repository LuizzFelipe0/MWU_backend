from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .service import CategoryService
from .schemas import CategoryOutput as CategoryOutScheme, CategoryInput as CategoryInScheme, \
    CategoryUpdateInput as CategoryUpdateInScheme

categories_router = APIRouter(prefix="/categories", tags=["Category"])


@cbv(categories_router)
class CategoryController:
    service: CategoryService = Depends()

    @categories_router.get("/all", response_model=list[CategoryOutScheme | None])
    def get_all_categories(self):
        categories = self.service.get_all_categories()
        return categories

    @categories_router.get("/deleted", response_model=list[CategoryOutScheme | None])
    def get_deleted_categories(self):
        deleted_categories = self.service.get_deleted_categories()
        return deleted_categories

    @categories_router.get("/{category_id}")
    def get_category_by_id(self, category_id: UUID) -> CategoryOutScheme | None:
        category = self.service.get_category_by_id(id=category_id)
        return category

    @categories_router.post("/create", response_model=CategoryOutScheme, status_code=201)
    def create_category(self, data: CategoryInScheme) -> CategoryOutScheme:
        category = self.service.create_category(data)
        return category

    @categories_router.patch("/{category_id}/update", status_code=200)
    def update_category(self, category_id: UUID, data: CategoryUpdateInScheme) -> CategoryOutScheme:
        category = self.service.update_category(id=category_id, data=data)
        return category

    @categories_router.delete("/{category_id}/delete", status_code=200)
    def delete_category(self, category_id: UUID) -> CategoryOutScheme:
        category = self.service.delete_category(id=category_id)
        return category

    @categories_router.post("{category_id}/restore", status_code=200)
    def restore_category(self, category_id: UUID) -> CategoryOutScheme:
        category = self.service.restore_category(id=category_id)
        return category
