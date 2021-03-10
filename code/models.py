from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, index=True)
    order_id = Column(String, index=True)
    order_number = Column(String, index=True)
    status = Column(String, index=True)
    cancel_reason_id = Column(Integer, index=True)
    created_at = Column(String, index=True)
    in_process_at = Column(String, index=True)

    order_products = relationship("OrderProducts", back_populates="own_products")
    order_analytics = relationship("OrderAnalytics", back_populates="own_analytics")
    order_findata = relationship("OrderFinData", back_populates="own_findata")


class OrderProducts(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, ForeignKey("order.posting_number"))
    sku = Column(Integer, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)
    offer_id = Column(String, index=True)
    price = Column(Float, index=True)

    own_products = relationship("Order", back_populates="order_products")


class OrderAnalytics(Base):
    __tablename__ = "order_analytics"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, ForeignKey("order.posting_number"))
    region = Column(String, index=True)
    city = Column(String, index=True)
    delivery_type = Column(String, index=True)
    is_premium = Column(Boolean, index=True)
    payment_type_group_name = Column(String, index=True)
    warehouse_id = Column(Integer, index=True)
    warehouse_name = Column(String, index=True)

    own_analytics = relationship("Order", back_populates="order_analytics")


class OrderFinData(Base):
    __tablename__ = "order_findata"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, ForeignKey("order.posting_number"))
    commission_amount = Column(Integer, index=True)
    commission_percent = Column(Integer, index=True)
    payout = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    old_price = Column(Float, index=True)
    price = Column(Float, index=True)
    total_discount_value = Column(Float, index=True)
    total_discount_percent = Column(Float, index=True)
    #actions = Column(String, index=True)
    picking = Column(String, index=True)
    quantity = Column(Integer, index=True)
    client_price = Column(String, index=True)

    own_findata = relationship("Order", back_populates="order_findata")
