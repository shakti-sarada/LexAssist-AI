# import os
# import logging
# from functools import lru_cache
#
# from dotenv import load_dotenv
# from pinecone import Pinecone
# from sentence_transformers import SentenceTransformer, CrossEncoder
#
# load_dotenv()
#
# # ---------------------------
# # 🔹 Logging Setup (FINAL)
# # ---------------------------
# os.makedirs("logs", exist_ok=True)
#
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
#
# # Remove old handlers
# if logger.hasHandlers():
#     logger.handlers.clear()
#
# # File handler
# file_handler = logging.FileHandler("logs/rag_system.log", mode="a")
# file_handler.setLevel(logging.INFO)
#
# file_formatter = logging.Formatter(
#     "%(asctime)s - %(levelname)s - %(message)s"
# )
# file_handler.setFormatter(file_formatter)
#
# # Console handler
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
#
# console_formatter = logging.Formatter(
#     "%(levelname)s - %(message)s"
# )
# console_handler.setFormatter(console_formatter)
#
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
#
#
# # ---------------------------
# # 🔹 Pinecone Setup
# # ---------------------------
# api_key = os.getenv("PINECONE_API_KEY")
# pc = Pinecone(api_key=api_key)
#
#
# def get_index(domain):
#     return pc.Index(f"legal-{domain}")
#
#
# # ---------------------------
# # 🔹 Models
# # ---------------------------
# embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
#
#
# # ---------------------------
# # 🔹 Cached Embedding
# # ---------------------------
# @lru_cache(maxsize=500)
# def get_embedding(text):
#     return tuple(embed_model.encode(text, normalize_embeddings=True))
#
#
# # ---------------------------
# # 🔹 Query Expansion
# # ---------------------------
# def expand_query(query, domain):
#     query = query.lower()
#
#     if domain == "consumer":
#         query += " consumer complaint refund defective product deficiency service compensation consumer court act rights"
#
#     elif domain == "cyber":
#         query += """
#         cyber crime fraud online scam hacking identity theft phishing cheating IT Act FIR cyber police complaint punishment unauthorized transaction banking fraud UPI fraud OTP fraud
#         """
#
#     elif domain == "food":
#         query += " food adulteration fssai unsafe food penalty punishment act complaint safety"
#
#     return query
#
#
# # ---------------------------
# # 🔹 Cyber safety filter
# # ---------------------------
# def is_safe_cyber_query(query):
#     keywords = [
#         "fraud", "scam", "hacking", "hack",
#         "otp", "unauthorized", "bank",
#         "payment", "cyber", "online",
#         "transaction", "account"
#     ]
#     return any(k in query.lower() for k in keywords)
#
#
# # ---------------------------
# # 🔹 Out-of-domain filter
# # ---------------------------
# def is_out_of_domain(query):
#     keywords = [
#         "complaint", "refund", "fraud", "law",
#         "court", "legal", "act", "consumer",
#         "food", "cyber", "crime", "police",
#         "service", "delivery", "product"
#     ]
#     return not any(k in query.lower() for k in keywords)
#
#
# # ---------------------------
# # 🔹 Adaptive top_k
# # ---------------------------
# def get_top_k(query):
#     length = len(query.split())
#
#     if length <= 5:
#         return 15
#     elif length <= 12:
#         return 25
#     else:
#         return 35
#
#
# # ---------------------------
# # 🔹 Retrieval + Reranking
# # ---------------------------
# def search_with_rerank(query, domain, final_k=5):
#     index = get_index(domain)
#
#     # Out-of-domain
#     if is_out_of_domain(query):
#         logger.warning("Out of domain query")
#         return "OUT_OF_DOMAIN"
#
#     # Cyber safety
#     if domain == "cyber" and not is_safe_cyber_query(query):
#         logger.warning("Unsafe cyber query")
#         return "UNSAFE_QUERY"
#
#     # Expand query
#     expanded_query = expand_query(query, domain)
#
#     # Adaptive recall
#     top_k = max(get_top_k(expanded_query), 30)
#
#     # Cached embedding
#     query_embedding = list(get_embedding(expanded_query))
#
#     results = index.query(
#         vector=query_embedding,
#         top_k=top_k,
#         include_metadata=True
#     )
#
#     matches = results.get("matches", [])
#
#     if not matches:
#         logger.warning("No matches found")
#         return "NO_CONTEXT"
#
#     # Reranking
#     pairs = [(expanded_query, m["metadata"]["text"]) for m in matches]
#     scores = reranker.predict(pairs)
#
#     reranked = [
#         {
#             "score": float(scores[i]),
#             "metadata": m["metadata"]
#         }
#         for i, m in enumerate(matches)
#     ]
#
#     reranked = sorted(reranked, key=lambda x: x["score"], reverse=True)
#
#     # Logging
#     logger.info(f"Domain: {domain}")
#     logger.info(f"Query: {query}")
#     logger.info(f"Top Score: {reranked[0]['score']}")
#     logger.info(f"Top Section: {reranked[0]['metadata']['section']}")
#
#     # Domain-based threshold
#     if domain == "cyber":
#         threshold = reranked[0]["score"] * 0.65
#     else:
#         threshold = reranked[0]["score"] * 0.75
#
#     if reranked[0]["score"] < threshold:
#         logger.warning("Low confidence retrieval")
#         return "NO_CONTEXT"
#
#     return reranked[:final_k]
#
#
# # ---------------------------
# # 🔹 Pretty Print
# # ---------------------------
# def pretty_print(results):
#     print("\n🔍 Reranked Results:\n")
#
#     if results == "OUT_OF_DOMAIN":
#         print("❌ Out of domain query")
#         return
#
#     if results == "UNSAFE_QUERY":
#         print("⚠️ Query not suitable for cyber domain")
#         return
#
#     if results == "NO_CONTEXT" or not results:
#         print("❌ No relevant context")
#         return
#
#     for i, res in enumerate(results, 1):
#         print(f"Result {i}:")
#         print(f"Rerank Score: {round(res['score'], 3)}")
#         print(f"Act: {res['metadata']['act']}")
#         print(f"Section: {res['metadata']['section']}")
#         print(f"Text: {res['metadata']['text'][:200]}...")
#         print("-" * 50)
#
#
# # ---------------------------
# # 🔹 Main
# # ---------------------------
# if __name__ == "__main__":
#     while True:
#         domain = input("\nEnter domain (food/consumer/cyber): ").strip().lower()
#         query = input("Enter query (or 'exit'): ").strip()
#
#         if query.lower() == "exit":
#             break
#
#         results = search_with_rerank(query, domain)
#         pretty_print(results)
#

import os

from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer, CrossEncoder

from logger import logger   # 🔥 IMPORT LOGGER

load_dotenv()

# ---------------------------
# 🔹 Pinecone Setup
# ---------------------------
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)


def get_index(domain):
    return pc.Index(f"legal-{domain}")


# ---------------------------
# 🔹 Models
# ---------------------------
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# ---------------------------
# 🔹 Query Expansion
# ---------------------------
def expand_query(query, domain):
    query = query.lower()

    if domain == "consumer":
        query += " consumer complaint refund defective product deficiency service compensation consumer court act rights"

    elif domain == "cyber":
        query += """
        cyber crime fraud online scam hacking identity theft phishing cheating IT Act FIR cyber police complaint punishment unauthorized transaction banking fraud UPI fraud OTP fraud
        """

    elif domain == "food":
        query += " food adulteration fssai unsafe food penalty punishment act complaint safety"

    return query


# ---------------------------
# 🔹 Cyber safety filter
# ---------------------------
def is_safe_cyber_query(query):
    keywords = [
        "fraud", "scam", "hacking", "hack",
        "otp", "unauthorized", "bank",
        "payment", "cyber", "online",
        "transaction", "account"
    ]
    return any(k in query.lower() for k in keywords)


# ---------------------------
# 🔹 Out-of-domain filter
# ---------------------------
def is_out_of_domain(query):
    keywords = [
        "complaint", "refund", "fraud", "law",
        "court", "legal", "act", "consumer",
        "food", "cyber", "crime", "police",
        "service", "delivery", "product"
    ]
    return not any(k in query.lower() for k in keywords)


# ---------------------------
# 🔹 Adaptive top_k
# ---------------------------
def get_top_k(query):
    length = len(query.split())

    if length <= 5:
        return 15
    elif length <= 12:
        return 25
    else:
        return 35


# ---------------------------
# 🔹 Retrieval + Reranking
# ---------------------------
def search_with_rerank(query, domain, final_k=5):
    index = get_index(domain)

    # Out-of-domain
    if is_out_of_domain(query):
        logger.warning("Out of domain query")
        return "OUT_OF_DOMAIN"

    # Cyber safety
    if domain == "cyber" and not is_safe_cyber_query(query):
        logger.warning("Unsafe cyber query")
        return "UNSAFE_QUERY"

    # Expand query
    expanded_query = expand_query(query, domain)

    # Adaptive recall
    top_k = max(get_top_k(expanded_query), 30)

    query_embedding = embed_model.encode(
        expanded_query,
        normalize_embeddings=True
    ).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    matches = results.get("matches", [])

    if not matches:
        logger.warning("No matches found")
        return "NO_CONTEXT"

    # Reranking
    pairs = [(expanded_query, m["metadata"]["text"]) for m in matches]
    scores = reranker.predict(pairs)

    reranked = [
        {
            "score": float(scores[i]),
            "metadata": m["metadata"]
        }
        for i, m in enumerate(matches)
    ]

    reranked = sorted(reranked, key=lambda x: x["score"], reverse=True)

    # Logging
    logger.info(f"Domain: {domain}")
    logger.info(f"Query: {query}")
    logger.info(f"Top Score: {reranked[0]['score']}")
    logger.info(f"Top Section: {reranked[0]['metadata']['section']}")

    # Domain-based threshold
    if domain == "cyber":
        threshold = reranked[0]["score"] * 0.65
    else:
        threshold = reranked[0]["score"] * 0.75

    if reranked[0]["score"] < threshold:
        logger.warning("Low confidence retrieval")
        return "NO_CONTEXT"

    return reranked[:final_k]


# ---------------------------
# 🔹 Pretty Print
# ---------------------------
def pretty_print(results):
    print("\n🔍 Reranked Results:\n")

    if results == "OUT_OF_DOMAIN":
        print("❌ Out of domain query")
        return

    if results == "UNSAFE_QUERY":
        print("⚠️ Query not suitable for cyber domain")
        return

    if results == "NO_CONTEXT" or not results:
        print("❌ No relevant context")
        return

    for i, res in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Rerank Score: {round(res['score'], 3)}")
        print(f"Act: {res['metadata']['act']}")
        print(f"Section: {res['metadata']['section']}")
        print(f"Text: {res['metadata']['text'][:200]}...")
        print("-" * 50)


# ---------------------------
# 🔹 Main
# ---------------------------
if __name__ == "__main__":
    while True:
        domain = input("\nEnter domain (food/consumer/cyber): ").strip().lower()
        query = input("Enter query (or 'exit'): ").strip()

        if query.lower() == "exit":
            break

        results = search_with_rerank(query, domain)
        pretty_print(results)