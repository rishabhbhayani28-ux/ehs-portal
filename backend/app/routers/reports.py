from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import io, csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .. import models
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/csv")
def download_csv(db: Session = Depends(get_db), _: models.User = Depends(get_current_admin)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Description", "Date"])
    for inc in db.query(models.Incident).all():
        writer.writerow([inc.id, inc.title, inc.description, inc.date_reported])
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=report.csv"})

@router.get("/xlsx")
def download_xlsx(db: Session = Depends(get_db), _: models.User = Depends(get_current_admin)):
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Title", "Description", "Date"])
    for inc in db.query(models.Incident).all():
        ws.append([inc.id, inc.title, inc.description, str(inc.date_reported)])
    stream = io.BytesIO()
    wb.save(stream)
    return Response(content=stream.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment; filename=report.xlsx"})

@router.get("/pdf")
def download_pdf(db: Session = Depends(get_db), _: models.User = Depends(get_current_admin)):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    c.setFont("Helvetica", 12)
    for inc in db.query(models.Incident).all():
        c.drawString(50, y, f"{inc.id}. {inc.title} - {inc.description or ''} ({inc.date_reported})")
        y -= 20
    c.showPage()
    c.save()
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
