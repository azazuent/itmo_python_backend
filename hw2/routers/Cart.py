from fastapi import APIRouter

router = APIRouter(
    prefix="/cart"
)


@router.post("", response_model=dict[str])
def initialize_cart():
    ...
