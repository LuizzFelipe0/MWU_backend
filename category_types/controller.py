from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .repository import CategoryTypeRepository
from .schemas import CategoryTypesOutput as CategoryTypesOutScheme, CategoryTypesInput as CategoryTypeInScheme, \
    CategoryTypesUpdateInput as CategoryTypesUpdateInScheme

category_types_router = APIRouter(prefix="/category_types", tags=["Category Types"])


@cbv(category_types_router)
class CategoryTypeController:
    service: CategoryTypeRepository = Depends()

    @category_types_router.get("/all", response_model=list[CategoryTypesOutScheme])
    def get_all(self):
        return self.service.get_all_category_types()

    @category_types_router.post("/create", response_model=CategoryTypesOutScheme, status_code=201)
    def create(self, data: CategoryTypeInScheme):
        return self.service.create_category_type(data)

    @category_types_router.patch("/update/{category_id}", status_code=200)
    def update_category_type(self, category_id: UUID, data: CategoryTypesUpdateInScheme) -> CategoryTypesUpdateInScheme:
        return self.service.update_category_type(id=category_id, data=data)


"""


@category_types_router.patch("/update", status_code=200)
def update_category_type(category_type_id: UUID, data: CategoryTypesUpdateInScheme,
                         db: Session = Depends(get_db)) -> CategoryTypesUpdateInScheme:
    category_type = db.query(CategoryTypesModel).filter_by(id=category_type_id).first()

    if not category_type:
        raise HTTPException(status_code=404, detail="Category Type not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category_type, key, value)

    db.commit()

    return category_type


@category_types_router.delete("/delete", status_code=204)
def delete_category_type(category_type_id: UUID, db: Session = Depends(get_db)):
    category_type = db.query(CategoryTypesModel).filter_by(id=category_type_id).first()

    if not category_type:
        raise HTTPException(status_code=404, detail="Category Type not found")

    db.delete(category_type)
    db.commit()"""
