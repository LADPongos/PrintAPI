# 🖨️ PrintAPI

A FastAPI application designed to handle print shop processes — accepting orders, computing costs automatically, and tracking order status.

---

## Features

- Submit print orders with multiple document items
- Auto-calculates total cost based on page type
- Tracks order status: `Queued` → `Processed` → `Complete`
- No database required — lightweight in-memory storage

---

## Pricing

| Page Type         | Price per Page |
| ----------------- | -------------- |
| `black_and_white` | PHP 2.00       |
| `colored`         | PHP 5.00       |
| `photo_paper`     | PHP 20.00      |

---

## Getting Started

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

### 3. Open the docs

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

---

## API Endpoints

| Method   | Endpoint                      | Description               |
| -------- | ----------------------------- | ------------------------- |
| `GET`    | `/`                           | Welcome page              |
| `GET`    | `/orders`                     | Get all orders            |
| `GET`    | `/orders/{order_id}`          | Get a specific order      |
| `POST`   | `/orders`                     | Create a new order        |
| `DELETE` | `/orders`                     | Delete all orders         |
| `DELETE` | `/orders/{order_id}`          | Delete a specific orders  |
| `PUT`    | `/orders/{order_id}/complete` | Mark an order as Complete |

---

## Example Request

**POST** `/orders`

```json
{
  "customer_name": "Juan dela Cruz",
  "items": [
    {
      "document_name": "thesis.pdf",
      "number_of_pages": 10,
      "copies_per_page": 2,
      "page_type": "black_and_white"
    }
  ]
}
```

**Response**

```json
{
  "message": "Order successfully created.",
  "order": {
    "order_id": "a1b2c3d4-...",
    "customer_name": "Juan dela Cruz",
    "items": [...],
    "total_cost": 40.00,
    "status": "Queued"
  }
}
```

---

## Data Model

| Field             | Type  | Description                                    |
| ----------------- | ----- | ---------------------------------------------- |
| `order_id`        | str   | Auto-generated unique order ID                 |
| `customer_name`   | str   | Name of the customer                           |
| `items`           | list  | List of document items in the order            |
| `document_name`   | str   | Name of the document                           |
| `number_of_pages` | int   | Number of pages to print                       |
| `copies_per_page` | int   | Number of copies per page                      |
| `page_type`       | str   | `black_and_white`, `colored`, or `photo_paper` |
| `total_cost`      | float | Auto-calculated total (PHP)                    |
| `status`          | str   | `Queued`, `Processed`, or `Complete`           |
