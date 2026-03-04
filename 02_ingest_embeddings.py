# 02_ingest_embeddings.py

from pypdf import PdfReader
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from io import BytesIO
from config import *

# Azure OpenAI client
aoai = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# Azure Search client
search_client = SearchClient(
    SEARCH_ENDPOINT,
    SEARCH_INDEX_NAME,
    AzureKeyCredential(SEARCH_KEY)
)


# Chunk text into small pieces
def chunk_text(text, size=600):
    return [text[i:i + size] for i in range(0, len(text), size)]


def process_pdf(blob_name):
    # Download PDF from Blob Storage
    blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container = blob_service.get_container_client(BLOB_CONTAINER)
    blob_data = container.download_blob(blob_name).readall()

    # Correct PDF reading (wrap bytes with BytesIO)
    reader = PdfReader(BytesIO(blob_data))

    docs = []
    base_name = blob_name.split('.')[0]  # remove .pdf

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        for j, chunk in enumerate(chunk_text(text)):
            embedding = aoai.embeddings.create(
                model=OPENAI_EMBED_MODEL,
                input=chunk
            ).data[0].embedding

            doc_id = f"{base_name}-{i}-{j}"

            docs.append({
                "id": doc_id,
                "content": chunk,
                "source_file": blob_name,
                "page": i,
                "embedding": embedding
            })

    # Upload all chunks to Azure Search
    search_client.upload_documents(docs)
    print(f"Uploaded {len(docs)} chunks from {blob_name}")


if __name__ == "__main__":
    process_pdf("Mathangi_Ananthasubramanian_Resume.pdf")
