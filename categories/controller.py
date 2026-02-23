from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from auth.utils import get_current_user
from .schemas import CategoryOutput as CategoryOutScheme, CategoryInput as CategoryInScheme, \
    CategoryUpdateInput as CategoryUpdateInScheme
from .service import CategoryService

categories_router = APIRouter(prefix="/categories", tags=["Category"])


@cbv(categories_router)
class CategoryController:
    service: CategoryService = Depends()

    @categories_router.get("/all", response_model=list[CategoryOutScheme | None])
    def get_all_categories(self, current_user = Depends(get_current_user)):
        categories = self.service.get_all_categories(user_id=current_user.id)
        return categories

    @categories_router.get("/deleted", response_model=list[CategoryOutScheme | None])
    def get_deleted_categories(self, current_user = Depends(get_current_user)):
        deleted_categories = self.service.get_deleted_categories(user_id=current_user.id)
        return deleted_categories

    @categories_router.get("/{category_id}")
    def get_category_by_id(self, category_id: UUID, current_user = Depends(get_current_user)) -> CategoryOutScheme | None:
        category = self.service.get_category_by_id(id=category_id, user_id=current_user.id)
        return category

    @categories_router.post("/create", response_model=CategoryOutScheme, status_code=201)
    def create_category(self, data: CategoryInScheme, current_user = Depends(get_current_user)) -> CategoryOutScheme:
        category = self.service.create_category(data=data, user_id=current_user.id)
        return category

    @categories_router.patch("/{category_id}/update", status_code=200)
    def update_category(self, category_id: UUID,
                        data: CategoryUpdateInScheme,
                        current_user = Depends(get_current_user)) -> CategoryOutScheme:
        category = self.service.update_category(id=category_id, data=data, user_id=current_user.id)
        return category

    @categories_router.delete("/{category_id}/delete", status_code=200)
    def delete_category(self, category_id: UUID, current_user = Depends(get_current_user)):
        category = self.service.delete_category(id=category_id, user_id=current_user.id)
        return category

    @categories_router.post("/{category_id}/restore", status_code=200)
    def restore_category(self, category_id: UUID, current_user = Depends(get_current_user)) -> CategoryOutScheme:
        category = self.service.restore_category(id=category_id, user_id=current_user.id)
        return category

    @categories_router.delete("/{category_id}/force-delete", status_code=204)
    def force_delete_category(self, category_id: UUID, current_user = Depends(get_current_user)):
        category = self.service.force_delete_category(id=category_id, user_id=current_user.id)
        return category
