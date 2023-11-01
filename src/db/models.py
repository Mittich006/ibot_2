from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    TEXT,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from sqlalchemy.ext.mutable import MutableList, Mutable
from sqlalchemy.types import TypeDecorator, VARCHAR

from src.db.session import CompyshopDBBase


class LimitedLengthArray(TypeDecorator, Mutable):
    """
    Custom column type for PostgreSQL ARRAY with a limited length constraint.
    When updating the array, shifts values to the left and adds a new value at the end.
    """
    impl = ARRAY(VARCHAR)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        # Shift values to the left and add a new value at the end when updating the array
        if value is not None:
            value = value[-5:]  # Keep the last 5 elements
        return value

    def coerce_set(self, key, value):
        # Coerce the value to a set before setting it in the column
        # Shift values to the left and add a new value at the end
        return super(LimitedLengthArray, self).coerce_set(key, value)[-5:]


MutableList.associate_with(LimitedLengthArray)


class Users(CompyshopDBBase):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    identity_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=True
    )
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    registered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class UserStates(CompyshopDBBase):
    __tablename__ = "user_states"

    user_state_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )
    current_product_id: Mapped[int] = mapped_column(Integer, nullable=True)
    current_catalog_id: Mapped[int] = mapped_column(Integer, nullable=True)
    history: Mapped[list] = mapped_column(
        MutableList.as_mutable(LimitedLengthArray(String(254))),
        server_default="{}",
    )

    user: Mapped["Users"] = relationship(
        backref=backref("user_states", cascade="all, delete-orphan"))


class Catalogs(CompyshopDBBase):
    __tablename__ = "catalogs"

    catalog_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )


class Products(CompyshopDBBase):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    catalog_id: Mapped[str] = mapped_column(
        ForeignKey("catalogs.catalog_id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    catalog: Mapped["Catalogs"] = relationship(
        backref=backref("products", cascade="all, delete-orphan")
    )


class UserFavorites(CompyshopDBBase):
    __tablename__ = "user_favorites"

    user_favorite_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id"),
        nullable=False
    )

    user: Mapped["Users"] = relationship(
        backref=backref("user_favorites", cascade="all, delete-orphan")
    )
    product: Mapped["Products"] = relationship(
        backref=backref("user_favorites", cascade="all, delete-orphan")
    )
