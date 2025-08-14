from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.header import SRFctHeader
from app.models.items import SRFctItems
from app.schemas.header import HeaderCreate, HeaderResponse, HeaderUpdate
from app.schemas.items import ItemResponse

# from decimal import Decimal

router = APIRouter(
    prefix="/sr",
    tags=["Service Requests"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/headers/", response_model=HeaderResponse, status_code=status.HTTP_201_CREATED
)
def create_header_with_items(header_data: HeaderCreate, db: Session = Depends(get_db)):
    """
    Create a new service request header with associated items
    """
    try:
        # Create header instance
        db_header = SRFctHeader(
            appkey=header_data.appkey,
            keyid=header_data.keyid,
            fk_sr_type_of_request_id=header_data.fk_sr_type_of_request_id,
            fk_sr_reason_of_return_id=header_data.fk_sr_reason_of_return_id,
            fk_sr_mode_of_return_id=header_data.fk_sr_mode_of_return_id,
            fk_status_id=header_data.fk_status_id,
            kunnr=header_data.kunnr,
            update_shipcode=header_data.update_shipcode,
            ship_name=header_data.ship_name,
            ship_to=header_data.ship_to,
            sdo_pao_remarks=header_data.sdo_pao_remarks,
            ssa_remarks=header_data.ssa_remarks,
            approver_remarks=header_data.approver_remarks,
            return_total=header_data.return_total,
            replacement_total=header_data.replacement_total,
            nsmemail=header_data.nsmemail,
            gsmemail=header_data.gsmemail,
            rsmemail=header_data.rsmemail,
            fspemail=header_data.fspemail,
            code=header_data.code,
            date_submitted_ssa=header_data.date_submitted_ssa,
            date_sent_approval=header_data.date_sent_approval,
            fsp=header_data.fsp,
            rsm=header_data.rsm,
            total_amount=header_data.total_amount,
            atpo_number=header_data.atpo_number,
            wrr_number=header_data.wrr_number,
            creation_tat=header_data.creation_tat,
            approver=header_data.approver,
            date_approval=header_data.date_approval,
            processing_tat=header_data.processing_tat,
            total_tat=header_data.total_tat,
            approval_tat=header_data.approval_tat,
            remarks_return=header_data.remarks_return,
            channel=header_data.channel,
        )

        db.add(db_header)
        db.flush()  # Get the header ID

        # Create associated items
        for item_data in header_data.items:
            db_item = SRFctItems(
                appkey=header_data.appkey,  # Reference to header
                keyid=item_data.keyid,
                matnr=item_data.matnr,
                fk_sr_action_of_type=item_data.fk_sr_action_of_type,
                discount=item_data.discount,
                qty=item_data.qty,
                srp=item_data.srp,
                total_amount=item_data.total_amount,
                net_price=item_data.net_price,
                net_total_amount=item_data.net_total_amount,
                fsp_remarks=item_data.fsp_remarks,
                ssa_remarks=item_data.ssa_remarks,
                dr_number=item_data.dr_number,
                dr_date=item_data.dr_date,
                code=item_data.code,
                nsmemail=item_data.nsmemail,
                gsmemail=item_data.gsmemail,
                fspemail=item_data.fspemail,
                is_sdo=item_data.is_sdo,
            )
            db.add(db_item)

        db.commit()

        # Refresh and return the created header with items
        db.refresh(db_header)
        return db_header

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create header: {str(e)}",
        )


@router.get("/headers/", response_model=List[HeaderResponse])
def get_all_headers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all service request headers with their items
    """
    # Only load items for now to avoid schema mismatch issues
    headers = (
        db.query(SRFctHeader)
        .options(joinedload(SRFctHeader.items))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return headers


@router.get("/headers/{appkey}", response_model=HeaderResponse)
def get_header_by_appkey(appkey: str, db: Session = Depends(get_db)):
    """
    Get a specific service request header by appkey
    """
    header = (
        db.query(SRFctHeader)
        .options(
            joinedload(SRFctHeader.items),
            joinedload(SRFctHeader.attachments),
            joinedload(SRFctHeader.log_remarks_header),
        )
        .filter(SRFctHeader.appkey == appkey)
        .first()
    )

    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Header with appkey {appkey} not found",
        )
    return header


@router.put("/headers/{appkey}", response_model=HeaderResponse)
def update_header(
    appkey: str, header_update: HeaderUpdate, db: Session = Depends(get_db)
):
    """
    Update a service request header
    """
    db_header = db.query(SRFctHeader).filter(SRFctHeader.appkey == appkey).first()
    if not db_header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Header with appkey {appkey} not found",
        )

    # Update only provided fields
    update_data = header_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(db_header, field):
            setattr(db_header, field, value)

    try:
        db.commit()
        db.refresh(db_header)
        return db_header
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update header: {str(e)}",
        )


@router.delete("/headers/{appkey}", status_code=status.HTTP_204_NO_CONTENT)
def delete_header(appkey: str, db: Session = Depends(get_db)):
    """
    Delete a service request header and its associated items
    """
    db_header = db.query(SRFctHeader).filter(SRFctHeader.appkey == appkey).first()
    if not db_header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Header with appkey {appkey} not found",
        )

    try:
        db.delete(db_header)  # Cascade will delete associated items
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete header: {str(e)}",
        )


@router.get("/items/", response_model=List[ItemResponse])
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all service request items
    """
    items = db.query(SRFctItems).offset(skip).limit(limit).all()
    return items


@router.get("/items/{appkey}", response_model=List[ItemResponse])
def get_items_by_appkey(appkey: str, db: Session = Depends(get_db)):
    """
    Get all items for a specific appkey
    """
    items = db.query(SRFctItems).filter(SRFctItems.appkey == appkey).all()
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No items found for appkey {appkey}",
        )
    return items
