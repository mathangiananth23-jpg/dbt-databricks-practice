# Azure RAG Demo

A Retrieval Augmented Generation (RAG) application built using Azure services that enables users to ask questions about uploaded documents.

The system converts documents into vector embeddings, stores them in Azure Cognitive Search, retrieves relevant context for a user query, and generates grounded responses using Azure OpenAI.

---

## Architecture

User Question → Query Embedding → Vector Search → Context Retrieval → GPT Response

Azure Services Used:

* Azure OpenAI
* Azure Cognitive Search
* Azure Blob Storage
* Streamlit UI

---

## Tech Stack

* **Azure OpenAI**

  * GPT-4o Mini (chat completion)
  * Text-Embedding-Ada-002 (vector embeddings)

* **Azure Cognitive Search**

  * Vector index
  * HNSW similarity search

* **Azure Blob Storage**

  * Document storage

* **Python**

  * RAG pipeline
  * REST-based vector retrieval

* **Streamlit**

  * Interactive chatbot interface

---

## How the System Works

1. A document is uploaded to Azure Blob Storage.
2. The ingestion pipeline extracts text and splits it into chunks.
3. Each chunk is converted into a vector embedding using Azure OpenAI.
4. The embeddings are stored in Azure Cognitive Search.
5. When a user asks a question:

   * The question is embedded
   * Azure Search retrieves the most relevant chunks
   * Retrieved context is passed to GPT-4o Mini
6. The model generates a grounded answer based on the retrieved context.

---

## Project Structure

```
config.py
01_create_index.py
02_ingest_embeddings.py
rag_query.py
ui_app.py
```

| File                    | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| config.py               | Azure credentials and configuration            |
| 01_create_index.py      | Creates vector search index                    |
| 02_ingest_embeddings.py | Processes documents and uploads embeddings     |
| rag_query.py            | Executes vector search and generates responses |
| ui_app.py               | Streamlit chatbot interface                    |

---

## Setup Instructions

1. Clone the repository

```
git clone <repo-url>
cd azure-rag-demo
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Configure Azure credentials

Copy:

```
config_sample.py → config.py
```

Then fill in:

* Azure OpenAI endpoint
* Azure OpenAI key
* Azure Search endpoint
* Azure Search key
* Blob storage connection string

4. Create the search index

```
python 01_create_index.py
```

5. Ingest documents

```
python 02_ingest_embeddings.py
```

6. Run the application

```
streamlit run ui_app.py
```

---

## Example Question

"What is the minimum attendance requirement?"

Example Answer:

"The minimum attendance requirement is 80% of the scheduled course contact hours."

---

## License

MIT License
