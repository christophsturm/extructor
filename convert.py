from typing import List, Optional, Union, Literal
from pydantic import BaseModel, HttpUrl


class Offer(BaseModel):
    type: Literal["Offer"] = "Offer"
    price: str
    priceCurrency: str
    availability: Optional[str] = None
    url: Optional[HttpUrl] = None
    itemCondition: Optional[str] = None
    seller: Optional[dict] = None  # This could be further typed if needed


class Product(BaseModel):
    type: Literal["Product"] = "Product"
    name: str
    description: Optional[str] = None
    image: Optional[Union[str, List[str]]] = None
    offers: Optional[Union[Offer, List[Offer]]] = None
    brand: Optional[dict] = None  # This could be further typed if needed
    manufacturer: Optional[dict] = None
    sku: Optional[str] = None
    gtin13: Optional[str] = None
    gtin14: Optional[str] = None
    mpn: Optional[str] = None


def find_products_and_offers(data: dict) -> List[Product]:
    products: List[Product] = []

    def extract_product(item: Union[dict, list]) -> None:
        if isinstance(item, dict):
            if item.get('@type') == 'Product' or item.get('type') == 'Product':
                try:
                    product = Product(**item)
                    products.append(product)
                except ValueError as e:
                    print(f"Error parsing product: {e}")

            for value in item.values():
                extract_product(value)
        elif isinstance(item, list):
            for element in item:
                extract_product(element)

    for syntax in ['json-ld', 'microdata', 'rdfa']:
        if syntax in data:
            extract_product(data[syntax])

    return products

# Example usage remains the same as in the previous response