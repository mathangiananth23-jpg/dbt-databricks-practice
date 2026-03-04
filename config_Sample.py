# ===============================
# Azure OpenAI Configuration
# ===============================

AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-openai-key>"

# Deployed model names in Azure OpenAI
OPENAI_CHAT_MODEL = "gpt-4o-mini"
OPENAI_EMBED_MODEL = "text-embedding-ada-002"


# ===============================
# Azure Cognitive Search
# ===============================

SEARCH_ENDPOINT = "https://<your-search-service>.search.windows.net"
SEARCH_KEY = "<your-search-admin-key>"

# Name of the vector index you created
SEARCH_INDEX_NAME = "student-policy-index"


# ===============================
# Azure Blob Storage
# ===============================

BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=<your-account>;AccountKey=<your-key>;EndpointSuffix=core.windows.net"

# Container where PDFs are uploaded
BLOB_CONTAINER = "student-handbook"