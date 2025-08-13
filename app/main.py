from fastapi import FastAPI
from app.database import engine
from app.models.order_models import Base
from app.routers import orders

# import os
from dotenv import load_dotenv

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Management API",
    description="",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers
app.include_router(orders.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Order Management API", "status": "running", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Sample data endpoint for testing
@app.post("/sample-data")
def create_sample_data():
    from app.database import SessionLocal
    from app.models.order_models import Header, Item

    db = SessionLocal()
    try:
        # Check if sample data already exists
        existing = db.query(Header).filter(Header.appkey == "ORD-2024-001").first()
        if existing:
            return {"message": "Sample data already exists"}

        # Sample header 1
        sample_header1 = Header(
            appkey="ORD-2024-001",
            customer_name="John Doe",
            customer_email="john.doe@email.com",
            customer_phone="+1234567890",
            status="confirmed",
            total_amount=299.98,
        )
        db.add(sample_header1)
        db.flush()

        # Sample items for header 1
        sample_items1 = [
            Item(
                key_id="ORD-2024-001",
                product_name="Wireless Headphones",
                product_code="WH-001",
                quantity=2,
                unit_price=99.99,
                total_price=199.98,
            ),
            Item(
                key_id="ORD-2024-001",
                product_name="USB Cable",
                product_code="UC-002",
                quantity=1,
                unit_price=19.99,
                total_price=19.99,
            ),
            Item(
                key_id="ORD-2024-001",
                product_name="Phone Case",
                product_code="PC-003",
                quantity=1,
                unit_price=29.99,
                total_price=29.99,
            ),
        ]

        for item in sample_items1:
            db.add(item)

        # Sample header 2
        sample_header2 = Header(
            appkey="ORD-2024-002",
            customer_name="Jane Smith",
            customer_email="jane.smith@email.com",
            customer_phone="+0987654321",
            status="pending",
            total_amount=149.99,
        )
        db.add(sample_header2)
        db.flush()

        # Sample item for header 2
        sample_item2 = Item(
            key_id="ORD-2024-002",
            product_name="Bluetooth Speaker",
            product_code="BS-004",
            quantity=1,
            unit_price=149.99,
            total_price=149.99,
        )
        db.add(sample_item2)

        db.commit()
        return {"message": "Sample data created successfully"}

    except Exception as e:
        db.rollback()
        return {"error": f"Failed to create sample data: {str(e)}"}
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
