import json
import re
from pathlib import Path


def clean_text(text: str) -> str:
    # Remove Gazette headers
    text = re.sub(r"THE GAZETTE OF INDIA.*?\n", "", text, flags=re.IGNORECASE)

    # Remove PART headers
    text = re.sub(r"\[\s*PART.*?\]", "", text, flags=re.IGNORECASE)

    # Remove OCR junk like izdkf'kr, izkf/kdkj
    text = re.sub(r"\b[a-z]{2,}[/'`][a-z]{2,}\b", "", text)

    # Remove weird mixed symbols but keep legal punctuation
    text = re.sub(r"[^\w\s\.,;:()\-\']", " ", text)

    # Remove very short useless tokens (but keep meaningful words)
    text = re.sub(r"\b[a-z]{1,2}\b", "", text)

    # Normalize spacing
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=250, overlap=50):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += (chunk_size - overlap)

    return chunks


def is_valid_chunk(text):
    words = text.split()
    if len(words) == 0:
        return False

    valid_words = [w for w in words if w.isalpha()]

    return len(valid_words) / len(words) > 0.6


def process_json(json_path: Path, domain: str):
    data = json.loads(json_path.read_text(encoding="utf-8"))

    all_chunks = []

    for item in data:
        cleaned = clean_text(item["content"])

        if len(cleaned.split()) < 30:
            continue

        chunks = chunk_text(cleaned)

        for idx, chunk in enumerate(chunks):
            if not is_valid_chunk(chunk):
                continue

            all_chunks.append({
                "domain": domain,  # ✅ added
                "act": item["act"],
                "section": item["section"],
                "chunk_id": idx,
                "text": chunk
            })

    output_path = Path(f"data/processed_data/{domain}")  # ✅ domain path
    output_file = output_path / f"{json_path.stem}_chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4, ensure_ascii=False)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    base_path = Path("data/processed_data")

    for domain_path in base_path.iterdir():
        if domain_path.is_dir():
            domain = domain_path.name
            print(f"\n📂 Processing domain: {domain}")

            for json_file in domain_path.glob("*_sections.json"):
                print(f"Processing: {json_file.name}")
                process_json(json_file, domain)