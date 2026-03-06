from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

app = FastAPI(
    title="PrintAPI",
    description="A FastAPI application to manage print shop orders.",
    version="1.0.0"
)

# ─────────────────────────────────────────────
# In-memory store (no database, as per PRD)
# ─────────────────────────────────────────────
orders: dict = {}

# ─────────────────────────────────────────────
# Pricing constants (PHP)
# ─────────────────────────────────────────────
PAGE_TYPE_PRICES = {
    "black_and_white": 2.00,
    "colored": 5.00,
    "photo_paper": 20.00,
}

VALID_STATUSES = {"Queued", "Processed", "Complete"}


# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────
class OrderItem(BaseModel):
    document_name: str = Field(..., example="thesis.pdf")
    number_of_pages: int = Field(..., gt=0, example=10)
    copies_per_page: int = Field(..., gt=0, example=2)
    page_type: str = Field(
        ...,
        example="black_and_white",
        description="Accepted values: black_and_white (PHP 2.00), colored (PHP 5.00), photo_paper (PHP 20.00)"
    )


class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="Juan dela Cruz")
    items: List[OrderItem]


class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    items: List[dict]
    total_cost: float
    status: str


# ─────────────────────────────────────────────
# Helper: compute total cost for an order
# ─────────────────────────────────────────────
def compute_total_cost(items: List[OrderItem]) -> float:
    total = 0.0
    for item in items:
        price_per_page = PAGE_TYPE_PRICES[item.page_type]
        total += item.number_of_pages * item.copies_per_page * price_per_page
    return round(total, 2)


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    """Welcome endpoint for PrintAPI."""
    return {
        "message": "Welcome to PrintAPI 🖨️",
        "description": "A print shop order management system.",
        "pricing": {
            "black_and_white": "PHP 2.00 per page",
            "colored": "PHP 5.00 per page",
            "photo_paper": "PHP 20.00 per page",
        },
        "endpoints": [
            "GET  /",
            "GET  /orders",
            "GET  /orders/{order_id}",
            "POST /orders",
            "DELETE /orders",
            "PUT /orders/{order_id}/complete",
        ]
    }


@app.get("/orders", tags=["Orders"])
def get_all_orders():
    """Retrieve all print orders."""
    if not orders:
        return {"message": "No orders found.", "orders": []}
    return {"message": f"{len(orders)} order(s) found.", "orders": list(orders.values())}


@app.get("/orders/{order_id}", tags=["Orders"])
def get_order(order_id: str):
    """Retrieve a specific print order by its ID."""
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return {"message": "Order found.", "order": order}


@app.post("/orders", status_code=201, tags=["Orders"])
def create_order(order_data: OrderCreate):
    """
    Create a new print order.

    - Accepts one or more document items per order.
    - Automatically calculates the total cost.
    - Sets the initial status to **Queued**.
    """
    # Validate page types
    for item in order_data.items:
        if item.page_type not in PAGE_TYPE_PRICES:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid page_type '{item.page_type}' for document '{item.document_name}'. "
                    f"Accepted values: {list(PAGE_TYPE_PRICES.keys())}"
                )
            )

    order_id = str(uuid4())
    total_cost = compute_total_cost(order_data.items)

    order_record = {
        "order_id": order_id,
        "customer_name": order_data.customer_name,
        "items": [item.dict() for item in order_data.items],
        "total_cost": total_cost,
        "status": "Queued",
    }

    orders[order_id] = order_record

    return {
        "message": "Order successfully created.",
        "order": order_record
    }


@app.delete("/orders", tags=["Orders"])
def delete_all_orders():
    """Delete all print orders from the system."""
    if not orders:
        return {"message": "No orders to delete."}
    count = len(orders)
    orders.clear()
    return {"message": f"All {count} order(s) have been deleted successfully."}

@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: str):
    """Delete a specific print order by its ID."""
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    del orders[order_id]
    return {"message": f"Order '{order_id}' has been deleted successfully."}

@app.put("/orders/{order_id}/complete", tags=["Orders"])
def complete_order(order_id: str):
    """
    Mark a print order as **Complete**.

    - Only orders with status **Queued** or **Processed** can be completed.
    """
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    if order["status"] == "Complete":
        return {"message": f"Order '{order_id}' is already marked as Complete.", "order": order}

    order["status"] = "Complete"
    orders[order_id] = order

    return {
        "message": f"Order '{order_id}' has been marked as Complete.",
        "order": order
    }