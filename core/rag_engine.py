"""
RAG Engine — using LangChain LCEL (works with LangChain 0.2 and 1.x)
Supports multi-turn conversation memory via manual history management.
"""

from typing import Dict, Any, List, Optional
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.documents import Document
from core.vector_store import VectorStoreManager


# ── Prompt Templates ──────────────────────────────────────────────────────────

SYSTEM_TEMPLATE = """You are an accurate, confidential AI document assistant.
Answer the user's question using ONLY the provided document context below.
If the answer cannot be found in the context, say clearly:
"I cannot find sufficient information in the uploaded documents to answer this question."
Do NOT fabricate information or use knowledge outside of the provided context.

---
DOCUMENT CONTEXT:
{context}
---

CONVERSATION HISTORY:
{chat_history}

CURRENT QUESTION: {question}

Provide a clear, well-structured answer based strictly on the document context above:"""


def _format_docs(docs: List[Document]) -> str:
    """Format retrieved documents into a single context string."""
    parts = []
    for i, doc in enumerate(docs, 1):
        src = doc.metadata.get("source_name", "Document")
        page = doc.metadata.get("page", "?")
        parts.append(f"[Source {i}: {src}, Page {page}]\n{doc.page_content}")
    return "\n\n".join(parts)


def _format_history(messages: List[Dict]) -> str:
    """Format chat history into a readable string for the prompt."""
    if not messages:
        return "No prior conversation."
    lines = []
    for msg in messages[-6:]:  # last 3 exchanges (6 messages)
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content'][:300]}")
    return "\n".join(lines)


class RAGEngine:
    """
    Conversational RAG engine using LangChain LCEL.
    Compatible with LangChain 0.2.x and 1.x.
    """

    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        temperature: float = 0.2,
        top_k: int = 4,
        memory_window: int = 6,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        self.memory_window = memory_window

        self.llm = Ollama(
            model=model_name,
            temperature=temperature,
            num_ctx=4096,
        )

        self.prompt = PromptTemplate(
            template=SYSTEM_TEMPLATE,
            input_variables=["context", "chat_history", "question"],
        )

    def answer_query(
        self,
        query: str,
        vector_manager: VectorStoreManager,
        chat_history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Runs the RAG pipeline and returns the answer with structured citations.

        Args:
            query:          The user's question.
            vector_manager: Active VectorStoreManager instance.
            chat_history:   Prior messages [{"role": ..., "content": ...}].

        Returns:
            {"answer": str, "citations": [...]}
        """
        vectorstore = vector_manager.get_vectorstore()
        if not vectorstore:
            raise ValueError(
                "No indexed knowledge base found. Please upload and index documents first."
            )

        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.top_k},
        )

        # Retrieve relevant documents
        source_docs = retriever.invoke(query)
        context_str = _format_docs(source_docs)
        history_str = _format_history(chat_history or [])

        # Build prompt and run LLM
        formatted_prompt = self.prompt.format(
            context=context_str,
            chat_history=history_str,
            question=query,
        )

        answer = self.llm.invoke(formatted_prompt)

        # Parse and deduplicate citations
        citations: List[Dict] = []
        seen: set = set()
        for doc in source_docs:
            src = doc.metadata.get("source_name", "Document")
            page = doc.metadata.get("page", 1)
            file_type = doc.metadata.get("file_type", "")
            preview = doc.page_content[:200].strip().replace("\n", " ") + "…"

            identifier = f"{src}_p{page}"
            if identifier not in seen:
                seen.add(identifier)
                citations.append(
                    {
                        "source": src,
                        "page": page,
                        "file_type": file_type,
                        "preview": preview,
                    }
                )

        return {"answer": answer, "citations": citations}

    def clear_memory(self) -> None:
        """No-op in LCEL approach — memory is managed externally via session state."""
        pass
