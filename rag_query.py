import json
import requests
from openai import AzureOpenAI
from config import *

# Initialize Azure OpenAI client (same as before)
aoai = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


# Helper: perform vector search by calling the Azure Search REST API directly
def vector_search_rest(query_embedding, top_k=3):
    # Build endpoint URL (use preview API version which supports vector search)
    # If your Search service requires a different api-version, replace it accordingly.
    api_version = "2023-07-01-preview"
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version={api_version}"

    body = {
        "vector": {
            "value": query_embedding,
            "k": top_k,
            "fields": "embedding"
        },
        # return the fields we need
        "select": "content,source_file,page"
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))
    resp.raise_for_status()
    rj = resp.json()

    # 'value' contains hits
    hits = rj.get("value", [])
    # Each hit's document fields are under 'content', 'source_file', 'page'
    return hits


def answer_question(question):
    # 1) create embedding for the query (Azure OpenAI)
    q_embed = aoai.embeddings.create(
        model=OPENAI_EMBED_MODEL,
        input=question
    ).data[0].embedding

    # 2) call REST vector search (returns top chunks)
    hits = vector_search_rest(q_embed, top_k=3)

    # 3) build context from search hits
    context_parts = []
    for h in hits:
        # depending on index, the fields may be directly top-level in hit
        # some responses use "document" or just field keys — handle both
        doc = h.get("document") if "document" in h else h
        content = doc.get("content") or doc.get("content", "")
        source = doc.get("source_file", "")
        page = doc.get("page", "")
        context_parts.append(f"Source: {source}, Page: {page}\n{content}")

    context = "\n\n---\n\n".join(context_parts) if context_parts else ""

    # 4) create a safe system prompt and call chat completion
    prompt = f"""
You answer ONLY from the context below. If the answer is not in the context, say "Not in document".
CONTEXT:
{context}

QUESTION: {question}
"""

    completion = aoai.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    q = "what are the certifications mentioned by mathangi?"
    print(answer_question(q))
