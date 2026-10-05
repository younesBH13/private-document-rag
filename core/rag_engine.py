from typing import Dict, Any, List
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from core.vector_store import VectorStoreManager

DEFAULT_SYSTEM_PROMPT = """You are an accurate, confidential AI document assistant.
Answer the user's question using ONLY the provided context below.
If the answer cannot be found in the context, explicitly state "I cannot find sufficient information in the uploaded documents to answer this question." Do not make up facts.

Context:
{context}

Question:
{question}

Helpful Answer (with clear explanations):"""

class RAGEngine:
    """Handles query processing, context retrieval, and response synthesis."""
    
    def __init__(self, model_name: str = "llama3.1:8b", temperature: float = 0.2, top_k: int = 4):
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        self.llm = Ollama(model=model_name, temperature=temperature)
        
        self.prompt_template = PromptTemplate(
            template=DEFAULT_SYSTEM_PROMPT,
            input_variables=["context", "question"]
        )

    def answer_query(self, query: str, vector_manager: VectorStoreManager) -> Dict[str, Any]:
        """Runs the query through the RAG pipeline and returns answer + structured citations."""
        vectorstore = vector_manager.get_vectorstore()
        if not vectorstore:
            raise ValueError("No indexed knowledge base found. Please upload and index documents first.")
            
        retriever = vectorstore.as_retriever(search_kwargs={"k": self.top_k})
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        response = qa_chain.invoke({"query": query})
        answer = response["result"]
        source_docs = response["source_documents"]
        
        # Deduplicate and format citations
        citations = []
        seen = set()
        for doc in source_docs:
            src = doc.metadata.get("source_name", "Document")
            page = doc.metadata.get("page", 1)
            preview = doc.page_content[:180].strip().replace("\n", " ") + "..."
            
            identifier = f"{src}_p{page}"
            if identifier not in seen:
                seen.add(identifier)
                citations.append({
                    "source": src,
                    "page": page,
                    "preview": preview
                })
                
        return {
            "answer": answer,
            "citations": citations
        }
