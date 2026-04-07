import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def process_all_domains():
    base_path = Path("data/raw_data")

    for domain_path in base_path.iterdir():
        if domain_path.is_dir():
            domain = domain_path.name

            print(f"\n📂 Processing domain: {domain}")

            output_path = Path(f"data/processed_data/{domain}")
            output_path.mkdir(parents=True, exist_ok=True)

            for pdf_file in domain_path.glob("*.pdf"):
                print(f"Processing: {pdf_file.name}")

                text = extract_text_from_pdf(str(pdf_file))

                # ✅ Save as TXT per domain
                txt_file = output_path / f"{pdf_file.stem}.txt"
                txt_file.write_text(text, encoding="utf-8")

                print(f"Saved: {txt_file}")


if __name__ == "__main__":
    process_all_domains()