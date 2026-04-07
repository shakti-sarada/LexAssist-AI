import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


# Load model (good balance of speed + quality)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def generate_embeddings(input_path: Path, domain: str):
    data = json.loads(input_path.read_text(encoding="utf-8"))

    embedded_data = []

    for item in tqdm(data, desc="Embedding"):
        embedding = model.encode(item["text"]).tolist()

        embedded_data.append({
            "domain": domain,  # ✅ added
            "act": item["act"],
            "section": item["section"],
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "embedding": embedding
        })

    output_path = Path(f"data/processed_data/{domain}")  # ✅ domain path
    output_file = output_path / f"{input_path.stem}_embeddings.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(embedded_data, f, indent=4)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    base_path = Path("data/processed_data")

    for domain_path in base_path.iterdir():
        if domain_path.is_dir():
            domain = domain_path.name
            print(f"\n📂 Processing domain: {domain}")

            for file in domain_path.glob("*_chunks.json"):
                print(f"Processing: {file.name}")
                generate_embeddings(file, domain)