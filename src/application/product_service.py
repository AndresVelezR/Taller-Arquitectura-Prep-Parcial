"""
Servicio de aplicación para gestionar productos.

Implementa casos de uso relacionados con productos,
orquestando el repositorio del dominio.
"""
from typing import List

from src.domain.entities import Product
from src.domain.exceptions import InvalidProductDataError, ProductNotFoundError
from src.domain.repositories import IProductRepository

from .dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para operaciones con productos.

    Orquesta la lógica de negocio entre la API (capa de presentación)
    y el repositorio (capa de persistencia), aplicando el patrón
    de Dependency Injection.

    Attributes:
        product_repo: Repositorio de productos inyectado.
    """

    def __init__(self, product_repo: IProductRepository) -> None:
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repo: Implementación del repositorio de productos.
        """
        self.product_repo = product_repo

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles.

        Returns:
            Lista de DTOs con todos los productos.
        """
        products = self.product_repo.get_all()
        return [self._entity_to_dto(p) for p in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Busca un producto por su ID.

        Args:
            product_id: ID del producto a buscar.

        Returns:
            DTO del producto encontrado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return self._entity_to_dto(product)

    def get_products_by_brand(self, brand: str) -> List[ProductDTO]:
        """
        Filtra productos por marca.

        Args:
            brand: Marca a filtrar (ej: "Nike", "Adidas").

        Returns:
            Lista de DTOs de productos de esa marca.
        """
        products = self.product_repo.get_by_brand(brand)
        return [self._entity_to_dto(p) for p in products]

    def get_products_by_category(self, category: str) -> List[ProductDTO]:
        """
        Filtra productos por categoría.

        Args:
            category: Categoría a filtrar (ej: "Running", "Casual").

        Returns:
            Lista de DTOs de productos de esa categoría.
        """
        products = self.product_repo.get_by_category(category)
        return [self._entity_to_dto(p) for p in products]

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene solo productos con stock disponible.

        Returns:
            Lista de DTOs de productos con stock > 0.
        """
        all_products = self.product_repo.get_all()
        available = [p for p in all_products if p.is_available()]
        return [self._entity_to_dto(p) for p in available]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto.

        Args:
            product_dto: Datos del producto a crear.

        Returns:
            DTO del producto creado con su ID asignado.

        Raises:
            InvalidProductDataError: Si los datos son inválidos.
        """
        try:
            product = self._dto_to_entity(product_dto)
            product.id = None
            saved = self.product_repo.save(product)
            return self._entity_to_dto(saved)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza un producto existente.

        Args:
            product_id: ID del producto a actualizar.
            product_dto: Nuevos datos del producto.

        Returns:
            DTO del producto actualizado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
            InvalidProductDataError: Si los datos son inválidos.
        """
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)

        try:
            product = self._dto_to_entity(product_dto)
            product.id = product_id
            saved = self.product_repo.save(product)
            return self._entity_to_dto(saved)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto.

        Args:
            product_id: ID del producto a eliminar.

        Returns:
            True si se eliminó, False si no existía.
        """
        return self.product_repo.delete(product_id)

    def _entity_to_dto(self, product: Product) -> ProductDTO:
        """
        Convierte una entidad de dominio a DTO.

        Args:
            product: Entidad de producto.

        Returns:
            DTO correspondiente.
        """
        return ProductDTO(
            id=product.id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
            description=product.description,
        )

    def _dto_to_entity(self, dto: ProductDTO) -> Product:
        """
        Convierte un DTO a entidad de dominio.

        Args:
            dto: DTO de producto.

        Returns:
            Entidad de producto.
        """
        return Product(
            id=dto.id,
            name=dto.name,
            brand=dto.brand,
            category=dto.category,
            size=dto.size,
            color=dto.color,
            price=dto.price,
            stock=dto.stock,
            description=dto.description,
        )
