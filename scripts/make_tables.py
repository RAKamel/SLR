"""Regenerate the two LaTeX tables and check paper citations.

Run from any directory with: python -P path/to/scripts/make_tables.py
Requires openpyxl. The workbook and bibliographies are read only.
"""

from collections import Counter
from pathlib import Path
import re
import sys

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "study_type", "RQ1 orientation", "RQ1 task_stage", "RQ2 architecture",
    "RQ2 adaptation", "RQ4 code_available", "RQ4 data_available",
)
MULTILABEL = {"RQ1 task_stage", "RQ2 adaptation"}
REVIEW_NOTE = re.compile(r"\s*\(you,\s*\d{4}-\d{2}-\d{2}[^)]*\)\s*$")
BIB_HEADER = re.compile(r"@([A-Za-z]+)\s*([({])\s*([^,\s]+)\s*,")
CITATION = re.compile(
    r"\\(?:cite[A-Za-z]*|nocite)\*?\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}"
)


def text(value):
    return "" if value is None else str(value).strip()


def tex_escape(value):
    escapes = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(escapes.get(char, char) for char in text(value))


def sheet_records(sheet):
    rows = sheet.iter_rows(values_only=True)
    headers = [text(value) for value in next(rows)]
    for row in rows:
        if any(value is not None for value in row):
            yield dict(zip(headers, row))


def bib_entries(source):
    """Read entry bodies with balanced delimiters, including nested braces."""
    position = 0
    while match := BIB_HEADER.search(source, position):
        opening = match[2]
        closing = "}" if opening == "{" else ")"
        depth = 1
        quoted = False
        index = match.end()
        while index < len(source) and depth:
            char = source[index]
            if char == "\\":
                index += 2
                continue
            if char == '"':
                quoted = not quoted
            if not quoted:
                if char == opening:
                    depth += 1
                elif char == closing:
                    depth -= 1
            index += 1
        if depth:
            raise ValueError(f"Unclosed bibliography entry: {match[3]}")
        if match[1].lower() not in {"comment", "preamble", "string"}:
            yield match[3], source[match.end():index - 1]
        position = index


def bib_field(body, name):
    match = re.search(r"(?:^|,)\s*" + re.escape(name) + r"\s*=\s*", body, re.I)
    if not match:
        raise ValueError(f"Missing bibliography field: {name}")
    start = match.end()
    opening = body[start]
    if opening not in '{"':
        return body[start:].split(",", 1)[0].strip()
    closing = "}" if opening == "{" else '"'
    depth = 1
    index = start + 1
    while index < len(body):
        char = body[index]
        if char == "\\":
            index += 2
            continue
        if char == closing:
            depth -= 1
            if not depth:
                return body[start + 1:index].strip()
        elif opening == "{" and char == opening:
            depth += 1
        index += 1
    raise ValueError(f"Unclosed bibliography field: {name}")


def study_references():
    source = (ROOT / "paper/included_studies.bib").read_text(encoding="utf-8-sig")
    references = {}
    for key, body in bib_entries(source):
        match = re.match(r"^(R\d+)_", key)
        if not match:
            continue
        study_id = match[1]
        if study_id in references:
            raise ValueError(f"Multiple included bibliography keys for {study_id}")
        try:
            author = re.split(r"\s+and\s+", bib_field(body, "author"), maxsplit=1)[0]
        except ValueError as error:
            if str(error) != "Missing bibliography field: author":
                raise
            author = ""
        # These entries use BibTeX's 'family, given' name format.
        surname = author.split(",", 1)[0].strip() or "---"
        if not author:
            print(f"Missing bibliography author: {key}; first author displayed as a dash.")
        references[study_id] = (key, surname, bib_field(body, "year"))
    return references


def qa_table(included, references):
    lines = [
        r"\begin{longtable}{@{}lp{0.40\textwidth}ccccc@{}}",
        r"\hline",
        r"id & First author + year & QA1 & QA2 & QA3 & QA4 & QA\_total \\",
        r"\hline",
        r"\endfirsthead",
        r"\hline",
        r"id & First author + year & QA1 & QA2 & QA3 & QA4 & QA\_total \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\endfoot",
    ]
    for row in included:
        study_id = text(row["id"])
        if study_id not in references:
            raise ValueError(f"Missing R-id-prefixed bibliography entry for {study_id}")
        key, surname, year = references[study_id]
        values = [tex_escape(study_id), f"{surname} ({year}) \\cite{{{key}}}"]
        for field in ("QA1", "QA2", "QA3", "QA4", "QA_total"):
            value = row[field]
            if not text(value):
                raise ValueError(f"Missing {field} for {study_id}")
            if isinstance(value, (int, float)):
                value = f"{value:g}"
            values.append(tex_escape(value))
        lines.append(" & ".join(values) + r" \\")
    lines.append(r"\end{longtable}")
    return "\n".join(lines) + "\n"


def coding_label(field, value):
    # Remove only the workbook's explicit dated reviewer provenance suffix.
    value = REVIEW_NOTE.sub("", text(value)).strip()
    if field in {"RQ4 code_available", "RQ4 data_available"}:
        # Collapse attached links to the category specified in the codebook.
        if re.fullmatch(r"yes\s*\(no URL\)", value, re.I):
            return "yes (no URL)"
        if re.fullmatch(r"yes\s*\(https?://.*\)", value, re.I):
            return "yes (URL)"
    return value


def frequency_tables(rows, included_ids):
    codes = {field: {} for field in FIELDS}
    for row in rows:
        study_id, field = text(row["id"]), text(row["field"])
        if study_id not in included_ids or field not in codes:
            continue
        if study_id in codes[field]:
            raise ValueError(f"Duplicate coding row: {study_id}, {field}")
        final = row["your_final_code"]
        selected = final if text(final) else row["codex_code (AI, to verify)"]
        value = coding_label(field, selected)
        if not value:
            raise ValueError(f"Missing code: {study_id}, {field}")
        codes[field][study_id] = value

    lines = []
    denominator = len(included_ids)
    for field in FIELDS:
        missing = included_ids - codes[field].keys()
        if missing:
            raise ValueError(f"Missing {field} coding rows: {', '.join(sorted(missing))}")
        counts = Counter()
        for value in codes[field].values():
            labels = {part.strip() for part in value.split(";")} if field in MULTILABEL else {value}
            if "" in labels:
                raise ValueError(f"Empty multi-label code in {field}: {value}")
            counts.update(labels)
        lines.extend([
            r"\begin{table}[tbp]",
            r"\centering",
            f"\\caption{{Frequency of {tex_escape(field)} among the {denominator} included studies.}}",
            r"\begin{tabular}{@{}p{0.65\linewidth}rr@{}}",
            r"\hline",
            r"Category & Count & \% \\",
            r"\hline",
        ])
        for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"{tex_escape(label)} & {count} & {100 * count / denominator:.1f}\\%" + r" \\")
        lines.extend([r"\hline", r"\end{tabular}", r"\end{table}", ""])
    return "\n".join(lines)


def check_citations():
    keys = set()
    for path in sorted((ROOT / "paper").glob("*.bib")):
        keys.update(key for key, _ in bib_entries(path.read_text(encoding="utf-8-sig")))
    missing = {}
    cited = set()
    for path in sorted((ROOT / "paper").rglob("*.tex")):
        source = path.read_text(encoding="utf-8-sig")
        source = re.sub(r"(?<!\\)%[^\n]*", "", source)
        for match in CITATION.finditer(source):
            for key in match[1].split(","):
                key = key.strip()
                if key == "*":
                    continue
                cited.add(key)
                if key not in keys:
                    missing.setdefault(key, set()).add(path.relative_to(ROOT).as_posix())
    print(f"Checked {len(cited)} distinct citation keys against paper/*.bib.")
    if missing:
        for key, paths in sorted(missing.items()):
            print(f"Missing citation key: {key} ({', '.join(sorted(paths))})")
    else:
        print("Missing citation keys: none.")
    return bool(missing)


def main():
    workbook = openpyxl.load_workbook(
        ROOT / "data/extraction/extraction.xlsx", read_only=True, data_only=True
    )
    try:
        included = [
            row for row in sheet_records(workbook["fulltext_qa"])
            if text(row["ft_decision (include/exclude)"]).lower() == "include"
        ]
        included.sort(key=lambda row: text(row["id"]))
        included_ids = {text(row["id"]) for row in included}
        if len(included) != 61 or len(included_ids) != 61 or "" in included_ids:
            raise ValueError("Expected exactly 61 distinct included study IDs.")
        qa = qa_table(included, study_references())
        counts = frequency_tables(sheet_records(workbook["coding_ai"]), included_ids)
    finally:
        workbook.close()
    for relative, content in (
        ("paper/sections/appendix-qa-scores.tex", qa),
        ("paper/tables/coded_counts.tex", counts),
    ):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Generated {relative}")
    return int(check_citations())


if __name__ == "__main__":
    sys.exit(main())
