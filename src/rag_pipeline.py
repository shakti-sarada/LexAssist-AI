import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer, CrossEncoder
from openai import OpenAI

from src.logger import logger

# ---------------------------
# 🔹 Load environment variables
# ---------------------------
load_dotenv()

# ---------------------------
# 🔹 Pinecone Setup
# ---------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_index(domain):
    return pc.Index(f"legal-{domain}")

# ---------------------------
# 🔹 Models
# ---------------------------
# embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

embed_model = None
reranker = None


def get_models():
    global embed_model, reranker

    if embed_model is None:
        embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    if reranker is None:
        reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    return embed_model, reranker


# ---------------------------
# 🔹 NVIDIA Setup
# ---------------------------
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# ---------------------------
# 🔹 Valid Domains
# ---------------------------
VALID_DOMAINS = {"food", "consumer", "cyber"}

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
# 🔹 Cyber Safety Filter
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
#

def retrieve_context(query, domain, final_k=3):
    index = get_index(domain)

    # ✅ 🔥 ADD THIS LINE (lazy loading)
    embed_model, reranker = get_models()

    if domain == "cyber" and not is_safe_cyber_query(query):
        return "UNSAFE_QUERY"

    expanded_query = expand_query(query, domain)

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
        return "NO_CONTEXT"

    pairs = [(expanded_query, m["metadata"]["text"]) for m in matches]
    scores = reranker.predict(pairs)

    reranked = sorted(
        [{"score": float(scores[i]), "text": m["metadata"]["text"]} for i, m in enumerate(matches)],
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(f"Top Score: {reranked[0]['score']}")

    if domain == "cyber":
        threshold = reranked[0]["score"] * 0.65
    else:
        threshold = reranked[0]["score"] * 0.75

    if reranked[0]["score"] < threshold:
        return "NO_CONTEXT"

    return "\n\n".join([r["text"] for r in reranked[:final_k]])


# ---------------------------
# 🔹 Cyber fallback
# ---------------------------
def cyber_fallback():
    return """
Cyber crimes such as online fraud, hacking, identity theft, and unauthorized transactions are generally covered under the IT Act.

What you should do:
1. Immediately inform your bank if money is involved
2. Report on https://cybercrime.gov.in
3. File a complaint at your nearest cyber police station
4. Preserve evidence (messages, transaction IDs, screenshots)

Consult a legal professional.
"""


# ---------------------------
# 🔹 Answer Generation
# ---------------------------
def generate_answer(query, context):
    prompt = f"""
You are a legal assistant for Indian laws.

STRICT RULES:
- Use ONLY the given context
- Do NOT assume anything outside the context
- If the context is NOT relevant → respond EXACTLY:
"No relevant legal information found."

- If the question is OUTSIDE the legal domain → respond EXACTLY:
"No relevant legal information found."

- Do NOT force-fit answers
- Do NOT hallucinate laws or sections

Format ONLY if relevant context exists and Format clearly using markdown:

**Explanation**
...

**What to do**
- Step 1
- Step 2
...

**Where to complain**
...

-------------------------
Context:
{context}

-------------------------
Question:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------------------------
# 🔹 MAIN RAG FUNCTION (FOR FASTAPI)
# ---------------------------
def run_rag(query: str, domain: str = "consumer"):
    logger.info(f"[API] Query: {query}")
    logger.info(f"[API] Domain: {domain}")

    if domain not in VALID_DOMAINS:
        return "Invalid domain. Choose from food, consumer, or cyber."

    # Out-of-domain check
    if is_out_of_domain(query):
        return "No relevant legal information found."

    # Retrieve context
    context = retrieve_context(query, domain)

    if context == "OUT_OF_DOMAIN":
        return "No relevant legal information found."

    elif context == "UNSAFE_QUERY":
        return "Consult a legal professional."

    elif context == "NO_CONTEXT":
        if domain == "cyber":
            return cyber_fallback()
        else:
            return "No relevant legal information found."

    # Generate answer
    answer = generate_answer(query, context)

    return answer