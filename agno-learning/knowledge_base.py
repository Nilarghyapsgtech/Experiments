from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

embedder=OpenAIEmbedder()
chunker=SemanticChunking(embedder=embedder,chunk_size=1000)

reader= PDFReader(chunking_strategy=chunker)
vectordb=ChromaDb(
    path="/Users/nilasark/experiments/agno-learning/Memory/chroma",
    collection="Knowledge",
    embedder=embedder,
    persistent_client=True
)

knowledge_base=Knowledge(
    name="knowledge_base",
    vector_db=vectordb
)
if __name__=="__main__":
    knowledge_base.add_content(path="/Users/nilasark/experiments/agno-learning/attention.pdf",reader=reader)

   