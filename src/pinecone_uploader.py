import json
from pathlib import Path
import os
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)


def get_index(domain):
    index_name = f"legal-{domain}"

    # Create index if not exists
    if index_name not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(index_name)


def filter_existing_ids(index, vectors):
    """Check which IDs already exist and remove them"""
    ids = [v["id"] for v in vectors]

    try:
        response = index.fetch(ids=ids)
        existing_ids = set(response.vectors.keys())
    except Exception:
        existing_ids = set()

    filtered = [v for v in vectors if v["id"] not in existing_ids]

    return filtered, len(existing_ids)


def upload_batch(index, batch, retries=3):
    for attempt in range(retries):
        try:
            index.upsert(vectors=batch)
            return
        except Exception as e:
            print(f"Retry {attempt+1} failed: {e}")
            time.sleep(2)

    print("❌ Failed batch after retries.")


def upload_embeddings(file_path: Path, domain: str):
    index = get_index(domain)

    data = json.loads(file_path.read_text(encoding="utf-8"))

    vectors = [
        {
            "id": f"{item['act']}_{item['section']}_{item['chunk_id']}",
            "values": item["embedding"],
            "metadata": {
                "text": item["text"],
                "act": item["act"],
                "section": item["section"]
            }
        }
        for item in data
    ]

    print(f"\nProcessing: {file_path.name}")
    print(f"Domain: {domain}")
    print(f"Total vectors: {len(vectors)}")

    # ✅ Filter duplicates BEFORE upload
    vectors, skipped = filter_existing_ids(index, vectors)

    print(f"Skipped existing: {skipped}")
    print(f"Uploading new: {len(vectors)}")

    if not vectors:
        print("✅ All vectors already exist. Skipping file.")
        return

    batch_size = 100

    for i in tqdm(range(0, len(vectors), batch_size),
                  desc=f"{file_path.name}",
                  unit="batch"):
        batch = vectors[i:i + batch_size]
        upload_batch(index, batch)

    print(f"✅ Uploaded: {file_path.name}")


if __name__ == "__main__":
    base_path = Path("data/processed_data")

    all_files = []

    for domain_path in base_path.iterdir():
        if domain_path.is_dir():
            domain = domain_path.name

            files = list(domain_path.glob("*_embeddings.json"))

            for file in files:
                all_files.append((file, domain))

    print(f"\nTotal files: {len(all_files)}\n")

    for file, domain in tqdm(all_files, desc="Overall Progress", unit="file"):
        upload_embeddings(file, domain)

    print("\n🎉 Upload complete (multi-index, no duplicates)!")