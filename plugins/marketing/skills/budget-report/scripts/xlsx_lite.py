"""Minimal stdlib-only .xlsx reader.

Neither openpyxl nor pandas is available in this environment, and installing
packages isn't reliable across sessions. An .xlsx is just a zip of XML files,
so this reads cell values directly via zipfile + xml.etree, which is always
available. Only what this skill needs: sheet listing and grid values (shared
strings resolved, numeric/text values only — no formatting, no formulas).
"""

import zipfile
import xml.etree.ElementTree as ET

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
R_ID_ATTR = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col_letters(cell_ref):
    return "".join(ch for ch in cell_ref if ch.isalpha())


def _col_index(letters):
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch.upper()) - ord("A") + 1)
    return idx


def list_sheets(path):
    """Return [{'name': str, 'rid': str}, ...] in workbook order."""
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        return [
            {"name": s.attrib.get("name"), "rid": s.attrib.get(R_ID_ATTR)}
            for s in wb.findall(".//m:sheets/m:sheet", NS)
        ]


def _shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", NS):
        texts = si.findall(".//m:t", NS)
        out.append("".join(t.text or "" for t in texts))
    return out


def _sheet_path_for(z, sheet_name):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rid = None
    for s in wb.findall(".//m:sheets/m:sheet", NS):
        if s.attrib.get("name") == sheet_name:
            rid = s.attrib.get(R_ID_ATTR)
            break
    if rid is None:
        raise KeyError(f"Sheet '{sheet_name}' not found")
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    for rel in rels:
        if rel.attrib.get("Id") == rid:
            return "xl/" + rel.attrib.get("Target")
    raise KeyError(f"No relationship target for sheet '{sheet_name}'")


def read_sheet_rows(path, sheet_name):
    """Return {row_num: {col_letter: value}} for every non-empty cell.

    Values are returned as str (numbers included) — caller converts as needed.
    Row numbers and column letters are 1-based / as they appear in Excel (A, B, ...).
    """
    with zipfile.ZipFile(path) as z:
        shared = _shared_strings(z)
        sheet_path = _sheet_path_for(z, sheet_name)
        root = ET.fromstring(z.read(sheet_path))
        rows = {}
        for row_el in root.findall(".//m:sheetData/m:row", NS):
            row_num = int(row_el.attrib["r"])
            row_data = {}
            for c in row_el.findall("m:c", NS):
                ref = c.attrib.get("r")
                letters = _col_letters(ref)
                t = c.attrib.get("t")
                v_el = c.find("m:v", NS)
                is_el = c.find("m:is", NS)
                val = None
                if is_el is not None:
                    texts = is_el.findall(".//m:t", NS)
                    val = "".join(t2.text or "" for t2 in texts)
                elif v_el is not None:
                    raw = v_el.text
                    if t == "s":
                        try:
                            val = shared[int(raw)]
                        except (ValueError, IndexError):
                            val = raw
                    else:
                        val = raw
                if val not in (None, ""):
                    row_data[letters] = val
            if row_data:
                rows[row_num] = row_data
        return rows


def cell(rows, row_num, col_letters):
    return rows.get(row_num, {}).get(col_letters)


def as_float(v):
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
