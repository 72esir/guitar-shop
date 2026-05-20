import enum
from sqlalchemy import String, Integer, Float, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class GuitarType(str, enum.Enum):
    ELECTRIC = "электрогитара"
    ACOUSTIC = "акустическая гитара"
    CLASSICAL = "классическая гитара"
    BASS = "бас гитара"

class PickupConfig(str, enum.Enum):
    SSS = "SSS"  # 3 сингла
    HH = "HH"  # 2 хамбакера
    HSS = "HSS"  # Хамбакер + 2 сингла
    HSH = "HSH"  # Хамбакер + сингл + хамбакер
    SS = "SS"  # 2 сингла
    P90 = "P90"  # Синглы P90
    PIEZO = "piezo"  # Пьезодатчик
    NONE = "none"  # Без звукоснимателей (чистая акустика)

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    # Спецификации гитары
    type: Mapped[GuitarType] = mapped_column(Enum(GuitarType), nullable=False)
    body_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    neck_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    fretboard_wood: Mapped[str] = mapped_column(String(50), nullable=False)
    fret_count: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_length: Mapped[float] = mapped_column(Float, nullable=False)

    # Конфигурация звукоснимателей
    pickup_config: Mapped[PickupConfig] = mapped_column(
        Enum(PickupConfig),
        nullable=False,
        default=PickupConfig.NONE
    )

    # Медиа
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)