# src/glitch_spreadsheet.py
import sys
import openpyxl
from core import pack_blob, unpack_blob

def encode(file_path, excel_path):
    blob = pack_blob(file_path)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "GlitchArchive"
    
    row, col = 1, 1
    for i in range(0, len(blob), 3):
        chunk = blob[i:i+3].ljust(3, b'\x00')
        hex_color = f"{chunk[0]:02x}{chunk[1]:02x}{chunk[2]:02x}"
        cell = ws.cell(row=row, column=col)
        cell.fill = openpyxl.styles.PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")
        col += 1
        if col > 256:
            col = 1
            row += 1
    wb.save(excel_path)

def decode(excel_path, output_file):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active
    blob = bytearray()
    
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=min(ws.max_column, 256)):
        for cell in row:
            if cell.fill and cell.fill.start_color and cell.fill.start_color.rgb:
                rgb_hex = str(cell.fill.start_color.rgb)
                if len(rgb_hex) >= 6:
                    if len(rgb_hex) == 8:
                        rgb_hex = rgb_hex[2:]
                    try:
                        r = int(rgb_hex[0:2], 16)
                        g = int(rgb_hex[2:4], 16)
                        b = int(rgb_hex[4:6], 16)
                        blob.extend([r, g, b])
                    except ValueError:
                        pass
            
    _, raw = unpack_blob(bytes(blob))
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if sys.argv[1] == 'enc':
            encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'dec':
            decode(sys.argv[2], sys.argv[3])