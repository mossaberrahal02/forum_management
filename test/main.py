from fastapi import FastAPI, HTTPException, Depends
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# Database connection
DATABASE = "example.db"

# Create a table if it doesn't exist
def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
            """
        )
        conn.commit()

# Dependency to get the database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

# Pydantic model for request/response validation (optional but recommended)
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(Item):
    id: int

# Create an item
@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (item.name, item.description),
    )
    conn.commit()
    item_id = cursor.lastrowid
    return {**item.dict(), "id": item_id}

# Read all items
@app.get("/items/", response_model=list[ItemResponse])
def read_items(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items")
    items = cursor.fetchall()
    return [{"id": row[0], "name": row[1], "description": row[2]} for row in items]

# Read a single item by ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "description": item[2]}

# Update an item by ID
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name = ?, description = ? WHERE id = ?",
        (item.name, item.description, item_id),
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "id": item_id}

# Delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

# Run the app
if __name__ == "__main__":
    create_table()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)