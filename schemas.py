"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Riceproduct(BaseModel):
    """
    Rice products collection schema
    Collection name: "riceproduct"
    """
    name: str = Field(..., description="Rice variety name")
    description: Optional[str] = Field(None, description="Short description")
    price_per_kg: float = Field(..., ge=0, description="Price per kilogram")
    origin: Optional[str] = Field(None, description="Origin region/country")
    stock_kg: float = Field(0, ge=0, description="Available stock in kg")
    image: Optional[str] = Field(None, description="Image URL")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Referenced riceproduct _id as string")
    name: str = Field(..., description="Product name snapshot")
    price_per_kg: float = Field(..., ge=0, description="Price per kg at time of order")
    quantity_kg: float = Field(..., gt=0, description="Quantity in kg")

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="Contact phone number")
    address: str = Field(..., description="Delivery address")
    notes: Optional[str] = Field(None, description="Additional notes")
    items: List[OrderItem] = Field(..., description="List of ordered items")
    total_amount: float = Field(..., ge=0, description="Computed total amount")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
