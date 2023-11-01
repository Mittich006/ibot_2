from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    TEXT,
    DECIMAL,
    ARRAY
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.mutable import MutableList

from src.db.session import CompyshopDBBase


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
    history: Mapped[list] = mapped_column(MutableList.as_mutable(
        ARRAY(String(length=254))),
        server_default="{}",
    )

    user: Mapped["Users"] = relationship()


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

    catalog: Mapped["Catalogs"] = relationship()