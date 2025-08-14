from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models.base import Base
from app.models.header import SRFctHeader
from app.models.items import SRFctItems
from app.routers import sr
from app.schemas.header import HeaderCreate
from app.schemas.items import ItemCreate
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Service Request Management API",
    description="API for managing service requests with headers and items",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers
app.include_router(sr.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "message": "Service Request Management API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/seed-sample-data")
def create_sample_data(db: Session = Depends(get_db)):
    """
    Seed the database with sample service request data
    """
    try:
        # Check if sample data already exists
        existing = (
            db.query(SRFctHeader).filter(SRFctHeader.appkey == "SR-2024-001").first()
        )
        if existing:
            return {"message": "Sample data already exists"}

        # Sample Service Request 1 - Return Request
        sample_header1 = SRFctHeader(
            appkey="SR-2024-001",
            keyid="KEY-001",
            fk_sr_type_of_request_id=1,  # Assuming 1 = Return Request
            fk_sr_reason_of_return_id=1,  # Assuming 1 = Defective
            fk_sr_mode_of_return_id=1,  # Assuming 1 = Pickup
            fk_status_id=1,  # Assuming 1 = Pending
            kunnr="CUST001",
            ship_name="ABC Electronics Store",
            ship_to="123 Main Street, Manila, Philippines",
            sdo_pao_remarks="Initial return request submitted",
            ssa_remarks="Under review by SSA team",
            return_total=Decimal("1500.00"),
            replacement_total=Decimal("0.00"),
            nsmemail="nsm@company.com",
            gsmemail="gsm@company.com",
            fspemail="fsp@company.com",
            code="RET1",
            date_submitted_ssa=datetime.now(),
            fsp="John Smith",
            rsm="Jane Doe",
            total_amount=Decimal("1500.00"),
            atpo_number=12345,
            creation_tat="24 hours",
            approver="Manager A",
            remarks_return="Customer reported defective units",
            channel=1,
        )
        db.add(sample_header1)
        db.flush()

        # Sample items for SR-2024-001
        sample_items1 = [
            SRFctItems(
                appkey="SR-2024-001",
                keyid="ITEM-001",
                matnr="MAT001",
                fk_sr_action_of_type=1,  # Assuming 1 = Return
                discount=Decimal("0.00"),
                qty=2,
                srp=Decimal("500.00"),
                total_amount=Decimal("1000.00"),
                net_price=Decimal("500.00"),
                net_total_amount=Decimal("1000.00"),
                fsp_remarks="Defective units confirmed",
                ssa_remarks="Approved for return",
                dr_number="DR-001-2024",
                dr_date=datetime.now(),
                code="ITEM001",
                nsmemail="nsm@company.com",
                gsmemail="gsm@company.com",
                fspemail="fsp@company.com",
                is_sdo=1,
            ),
            SRFctItems(
                appkey="SR-2024-001",
                keyid="ITEM-002",
                matnr="MAT002",
                fk_sr_action_of_type=1,  # Return
                discount=Decimal("0.00"),
                qty=1,
                srp=Decimal("500.00"),
                total_amount=Decimal("500.00"),
                net_price=Decimal("500.00"),
                net_total_amount=Decimal("500.00"),
                fsp_remarks="Customer complaint - not working",
                ssa_remarks="Verified defect",
                dr_number="DR-002-2024",
                dr_date=datetime.now(),
                code="ITEM002",
                nsmemail="nsm@company.com",
                gsmemail="gsm@company.com",
                fspemail="fsp@company.com",
                is_sdo=1,
            ),
        ]

        for item in sample_items1:
            db.add(item)

        # Sample Service Request 2 - Replacement Request
        sample_header2 = SRFctHeader(
            appkey="SR-2024-002",
            keyid="KEY-002",
            fk_sr_type_of_request_id=2,  # Assuming 2 = Replacement Request
            fk_sr_reason_of_return_id=2,  # Assuming 2 = Damaged in transit
            fk_sr_mode_of_return_id=2,  # Assuming 2 = Store drop-off
            fk_status_id=2,  # Assuming 2 = Approved
            kunnr="CUST002",
            ship_name="XYZ Mobile Shop",
            ship_to="456 Rizal Avenue, Quezon City, Philippines",
            sdo_pao_remarks="Replacement request processed",
            ssa_remarks="Approved by SSA",
            approver_remarks="Fast-track approved",
            return_total=Decimal("0.00"),
            replacement_total=Decimal("800.00"),
            nsmemail="nsm2@company.com",
            gsmemail="gsm2@company.com",
            rsmemail="rsm2@company.com",
            fspemail="fsp2@company.com",
            code="REP1",
            date_submitted_ssa=datetime.now(),
            date_sent_approval=datetime.now(),
            date_approval=datetime.now(),
            fsp="Alice Johnson",
            rsm="Bob Wilson",
            total_amount=Decimal("800.00"),
            atpo_number=12346,
            wrr_number=67890,
            creation_tat="12 hours",
            approver="Manager B",
            processing_tat=6,
            total_tat=18,
            approval_tat=4,
            remarks_return="Damaged during delivery",
            channel=2,
        )
        db.add(sample_header2)
        db.flush()

        # Sample item for SR-2024-002
        sample_item2 = SRFctItems(
            appkey="SR-2024-002",
            keyid="ITEM-003",
            matnr="MAT003",
            fk_sr_action_of_type=2,  # Assuming 2 = Replace
            discount=Decimal("50.00"),
            qty=1,
            srp=Decimal("850.00"),
            total_amount=Decimal("800.00"),
            net_price=Decimal("800.00"),
            net_total_amount=Decimal("800.00"),
            fsp_remarks="Replacement unit prepared",
            ssa_remarks="Ready for dispatch",
            dr_number="DR-003-2024",
            dr_date=datetime.now(),
            code="ITEM003",
            nsmemail="nsm2@company.com",
            gsmemail="gsm2@company.com",
            fspemail="fsp2@company.com",
            is_sdo=0,
        )
        db.add(sample_item2)

        # Sample Service Request 3 - Credit Note Request
        sample_header3 = SRFctHeader(
            appkey="SR-2024-003",
            keyid="KEY-003",
            fk_sr_type_of_request_id=3,  # Assuming 3 = Credit Note
            fk_sr_reason_of_return_id=3,  # Assuming 3 = Wrong item delivered
            fk_sr_mode_of_return_id=1,  # Pickup
            fk_status_id=3,  # Assuming 3 = In Progress
            kunnr="CUST003",
            ship_name="Tech Solutions Inc.",
            ship_to="789 EDSA, Makati City, Philippines",
            sdo_pao_remarks="Credit note requested",
            ssa_remarks="Processing credit memo",
            return_total=Decimal("1200.00"),
            replacement_total=Decimal("0.00"),
            nsmemail="nsm3@company.com",
            gsmemail="gsm3@company.com",
            fspemail="fsp3@company.com",
            code="CRN1",
            date_submitted_ssa=datetime.now(),
            fsp="Michael Brown",
            rsm="Sarah Davis",
            total_amount=Decimal("1200.00"),
            atpo_number=12347,
            creation_tat="36 hours",
            approver="Manager C",
            remarks_return="Wrong product delivered to customer",
            channel=1,
        )
        db.add(sample_header3)
        db.flush()

        # Sample items for SR-2024-003
        sample_items3 = [
            SRFctItems(
                appkey="SR-2024-003",
                keyid="ITEM-004",
                matnr="MAT004",
                fk_sr_action_of_type=3,  # Assuming 3 = Credit
                discount=Decimal("0.00"),
                qty=3,
                srp=Decimal("400.00"),
                total_amount=Decimal("1200.00"),
                net_price=Decimal("400.00"),
                net_total_amount=Decimal("1200.00"),
                fsp_remarks="Wrong items to be returned",
                ssa_remarks="Credit note preparation in progress",
                dr_number="DR-004-2024",
                dr_date=datetime.now(),
                code="ITEM004",
                nsmemail="nsm3@company.com",
                gsmemail="gsm3@company.com",
                fspemail="fsp3@company.com",
                is_sdo=1,
            )
        ]

        for item in sample_items3:
            db.add(item)

        db.commit()

        # Count created records
        header_count = db.query(SRFctHeader).count()
        item_count = db.query(SRFctItems).count()

        return {
            "message": "Sample data created successfully",
            "headers_created": 3,
            "items_created": 4,
            "total_headers_in_db": header_count,
            "total_items_in_db": item_count,
        }

    except Exception as e:
        db.rollback()
        return {"error": f"Failed to create sample data: {str(e)}"}


@app.delete("/clear-sample-data")
def clear_sample_data(db: Session = Depends(get_db)):
    """
    Clear all sample data from the database
    """
    try:
        # Delete all items first (due to foreign key constraints)
        items_deleted = db.query(SRFctItems).delete()

        # Delete all headers
        headers_deleted = db.query(SRFctHeader).delete()

        db.commit()

        return {
            "message": "Sample data cleared successfully",
            "headers_deleted": headers_deleted,
            "items_deleted": items_deleted,
        }
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to clear sample data: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
