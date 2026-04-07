# import re
# import json
# from pathlib import Path
#
#
# def split_into_sections(text: str):
#     # Match:
#     # Section 1
#     # OR 1.
#     pattern = r"(Section\s+\d+|^\d+\.)"
#
#     parts = re.split(pattern, text, flags=re.MULTILINE)
#
#     sections = []
#
#     for i in range(1, len(parts), 2):
#         section_title = parts[i].strip()
#         content = parts[i + 1].strip() if i + 1 < len(parts) else ""
#
#         if len(content) > 50:  # filter junk
#             sections.append({
#                 "section": section_title,
#                 "content": content
#             })
#
#     return sections
#
#
# def process_file(txt_path: Path):
#     text = txt_path.read_text(encoding="utf-8")
#
#     sections = split_into_sections(text)
#
#     structured = []
#
#     for sec in sections:
#         structured.append({
#             "act": txt_path.stem,
#             "section": sec["section"],
#             "content": sec["content"]
#         })
#
#     output_path = Path("data/processed_data") / f"{txt_path.stem}.json"
#
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(structured, f, indent=4, ensure_ascii=False)
#
#     print(f"Saved: {output_path}")
#
#
# if __name__ == "__main__":
#     processed_path = Path("data/processed_data")
#
#     for txt_file in processed_path.glob("*.txt"):
#         print(f"Processing: {txt_file.name}")
#         process_file(txt_file)

import re
import json
from pathlib import Path


def split_into_sections(text: str):
    # Match:
    # Section 1
    # OR 1.
    pattern = r"(Section\s+\d+|^\d+\.)"

    parts = re.split(pattern, text, flags=re.MULTILINE)

    sections = []

    for i in range(1, len(parts), 2):
        section_title = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""

        if len(content) > 50:  # filter junk
            sections.append({
                "section": section_title,
                "content": content
            })

    return sections


def process_file(txt_path: Path, domain: str):
    text = txt_path.read_text(encoding="utf-8")

    sections = split_into_sections(text)

    structured = []

    for sec in sections:
        structured.append({
            "domain": domain,  # ✅ added
            "act": txt_path.stem,
            "section": sec["section"],
            "content": sec["content"]
        })

    output_path = Path(f"data/processed_data/{domain}")  # ✅ domain-specific
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / f"{txt_path.stem}_sections.json"  # ✅ separate file

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=4, ensure_ascii=False)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    base_path = Path("data/processed_data")

    for domain_path in base_path.iterdir():
        if domain_path.is_dir():
            domain = domain_path.name
            print(f"\n📂 Processing domain: {domain}")

            for txt_file in domain_path.glob("*.txt"):
                print(f"Processing: {txt_file.name}")
                process_file(txt_file, domain)