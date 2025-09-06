from app.db.sqlite import get_connection
import pandas as pd
import os
from fastapi.responses import StreamingResponse
from openpyxl import load_workbook

EXCEL_FILE = "export.xlsx"  # fixed file instead of timestamped

def export_data():
    conn = get_connection()
    perf = pd.read_sql("SELECT * FROM index_performance", conn)
    comp = pd.read_sql("SELECT * FROM index_compositions", conn)
    conn.close()

    # ---- If file exists, update sheets ----
    if os.path.exists(EXCEL_FILE):
        book = load_workbook(EXCEL_FILE)
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            writer.book = book
            perf.to_excel(writer, sheet_name="Performance", index=False)
            comp.to_excel(writer, sheet_name="Composition", index=False)
    else:
        # ---- Create new file if it doesn't exist ----
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            perf.to_excel(writer, sheet_name="Performance", index=False)
            comp.to_excel(writer, sheet_name="Composition", index=False)

    # ---- Return updated file as download ----
    file_stream = open(EXCEL_FILE, "rb")
    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={EXCEL_FILE}"}
    )
