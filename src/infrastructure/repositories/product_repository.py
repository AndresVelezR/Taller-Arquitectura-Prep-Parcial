"""
Implementación del repositorio de productos usando SQLAlchemy.

Convierte entre entidades del dominio y modelos ORM.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.domain.repositories import IProductRepository

from ..db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación SQL del repositorio de productos.

    Usa SQLAlchemy para persistir y recuperar productos,
    convirtiendo entre entidades del dominio y modelos ORM.

    Attributes:
        db: Sesión de SQLAlchemy para interactuar con la BD.
    """

    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy activa.
        """
        self.db = db

    def get_all(self) -> List[Product]:
        """Obtiene todos los productos de la base de datos."""
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Busca un producto por su ID."""
        model = (
            self.db.query(ProductModel)
            .filter(ProductModel.id == product_id)
            .first()
        )
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """Obtiene productos de una marca específica."""
        models = (
            self.db.query(ProductModel)
            .filter(ProductModel.brand == brand)
            .all()
        )
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """Obtiene productos de una categoría específica."""
        models = (
            self.db.query(ProductModel)
            .filter(ProductModel.category == category)
            .all()
        )
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto.

        Si tiene ID, actualiza el existente. Si no tiene ID, crea uno nuevo.
        """
        if product.id:
            model = (
                self.db.query(ProductModel)
                .filter(ProductModel.id == product.id)
                .first()
            )
            if model:
                model.name = product.name
                model.brand = product.brand
                model.category = product.category
                model.size = product.size
                model.color = product.color
                model.price = product.price
                model.stock = product.stock
                model.description = product.description
            else:
                model = self._entity_to_model(product)
                self.db.add(model)
        else:
            model = self._entity_to_model(product)
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Returns:
            True si se eliminó, False si no existía.
        """
        model = (
            self.db.query(ProductModel)
            .filter(ProductModel.id == product_id)
            .first()
        )
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM a entidad de dominio.

        Args:
            model: Modelo ORM de producto.

        Returns:
            Entidad de producto del dominio.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """
        Convierte una entidad de dominio a modelo ORM.

        Args:
            entity: Entidad de producto del dominio.

        Returns:
            Modelo ORM de producto.
        """
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
