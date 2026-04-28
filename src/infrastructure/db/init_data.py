"""
Carga de datos iniciales en la base de datos.

Crea 10 productos de ejemplo variados para probar la aplicación.
"""
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import ProductModel


def load_initial_data() -> None:
    """
    Carga productos iniciales si la base de datos está vacía.

    Crea 10 zapatos de diferentes marcas, categorías, tallas y precios
    para tener datos de prueba al iniciar la aplicación.

    No hace nada si ya existen productos en la base de datos.
    """
    db: Session = SessionLocal()

    try:
        existing_count = db.query(ProductModel).count()

        if existing_count > 0:
            return

        initial_products = [
            ProductModel(
                name="Air Zoom Pegasus 40",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.00,
                stock=15,
                description="Zapatillas de running con amortiguación Air Zoom para máxima respuesta.",
            ),
            ProductModel(
                name="Ultraboost 23",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=180.00,
                stock=8,
                description="Running shoes con tecnología Boost para retorno de energía.",
            ),
            ProductModel(
                name="Suede Classic XXI",
                brand="Puma",
                category="Casual",
                size="40",
                color="Azul",
                price=75.00,
                stock=12,
                description="Zapatillas casual icónicas con parte superior de gamuza.",
            ),
            ProductModel(
                name="Fresh Foam X 1080v13",
                brand="New Balance",
                category="Running",
                size="43",
                color="Gris",
                price=150.00,
                stock=6,
                description="Zapatillas de running con espuma Fresh Foam para máximo confort.",
            ),
            ProductModel(
                name="Classic Leather",
                brand="Reebok",
                category="Casual",
                size="42",
                color="Blanco",
                price=65.00,
                stock=20,
                description="Zapatillas clásicas de cuero para uso diario.",
            ),
            ProductModel(
                name="Chuck Taylor All Star",
                brand="Converse",
                category="Casual",
                size="39",
                color="Negro",
                price=55.00,
                stock=25,
                description="Zapatillas icónicas de lona con diseño atemporal.",
            ),
            ProductModel(
                name="Gel-Kayano 30",
                brand="Asics",
                category="Running",
                size="42",
                color="Azul/Naranja",
                price=160.00,
                stock=7,
                description="Zapatillas de running con soporte de estabilidad y gel de amortiguación.",
            ),
            ProductModel(
                name="Revolution 7",
                brand="Nike",
                category="Running",
                size="41",
                color="Gris",
                price=65.00,
                stock=10,
                description="Zapatillas de running básicas con buena amortiguación y durabilidad.",
            ),
            ProductModel(
                name="Stan Smith",
                brand="Adidas",
                category="Casual",
                size="42",
                color="Blanco/Verde",
                price=90.00,
                stock=18,
                description="Zapatillas casual clásicas de tenis con diseño minimalista.",
            ),
            ProductModel(
                name="Leadcat 2.0 Slides",
                brand="Puma",
                category="Casual",
                size="40",
                color="Negro",
                price=30.00,
                stock=0,
                description="Sandalias slide cómodas para uso casual.",
            ),
        ]

        db.add_all(initial_products)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
