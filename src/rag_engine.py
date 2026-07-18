"""RAG engine for career coach AI application."""

import os
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st


def create_documents(resume_text: str, job_description_text: str) -> List[Document]:
    """
    Create LangChain Document objects from resume and job description.
    
    Args:
        resume_text: Content of the resume
        job_description_text: Content of the job description
        
    Returns:
        List[Document]: List of Document objects
    """
    documents = [
        Document(
            page_content=resume_text,
            metadata={"source": "resume", "type": "resume"}
        ),
        Document(
            page_content=job_description_text,
            metadata={"source": "job_description", "type": "job_description"}
        )
    ]
    return documents


def split_documents(
    documents: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> List[Document]:
    """
    Split documents into smaller chunks for embedding.
    
    Args:
        documents: List of Document objects
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List[Document]: List of chunked documents
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    for doc in documents:
        split_docs = splitter.split_documents([doc])
        chunks.extend(split_docs)
    
    return chunks


def build_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Build a Chroma vector store from document chunks.
    
    Args:
        chunks: List of chunked documents
        
    Returns:
        Chroma: Vector store instance
    """
    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    return vectorstore


def run_career_coach(
    vectorstore: Chroma,
    resume_text: str,
    job_description_text: str,
    question: str
) -> Tuple[str, List[Document]]:
    """
    Run the career coach RAG pipeline.
    
    Args:
        vectorstore: Chroma vector store
        resume_text: Resume content
        job_description_text: Job description content
        question: User's question
        
    Returns:
        Tuple[str, List[Document]]: Generated answer and source documents
    """
    # Initialize LLM
    llm = ChatGroq(
        model_name="mixtral-8x7b-32768",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Retrieve relevant context
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)
    
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question", "resume", "job_description"],
        template="""You are an expert career coach. Based on the provided context from the resume and job description, answer the following question.

Resume:
{resume}

Job Description:
{job_description}

Retrieved Context:
{context}

Question: {question}

Provide a detailed, actionable answer:"""
    )
    
    # Prepare context
    context_text = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Generate answer
    answer = llm.invoke(
        prompt_template.format(
            context=context_text,
            question=question,
            resume=resume_text[:2000],
            job_description=job_description_text[:2000]
        )
    ).content
    
    return answer, relevant_docs


def generate_complete_report(
    vectorstore: Chroma,
    resume_text: str,
    job_description_text: str
) -> Tuple[str, List[Document]]:
    """
    Generate a complete career analysis report.
    
    Args:
        vectorstore: Chroma vector store
        resume_text: Resume content
        job_description_text: Job description content
        
    Returns:
        Tuple[str, List[Document]]: Generated report and source documents
    """
    # Initialize LLM
    llm = ChatGroq(
        model_name="mixtral-8x7b-32768",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Retrieve relevant context
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    relevant_docs = retriever.invoke("resume job match skills gaps recommendations")
    
    # Create prompt template for complete report
    prompt_template = PromptTemplate(
        input_variables=["context", "resume", "job_description"],
        template="""You are an expert career coach. Analyze the resume against the job description and provide a comprehensive report.

Resume:
{resume}

Job Description:
{job_description}

Retrieved Context:
{context}

Generate a detailed career analysis report including:
1. Resume-Job Match Score (1-10)
2. Key Matching Skills
3. Missing/Gap Skills
4. Resume Improvement Suggestions
5. Recommended Projects to Learn Missing Skills
6. Interview Preparation Tips
7. Overall Recommendation"""
    )
    
    # Prepare context
    context_text = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Generate report
    report = llm.invoke(
        prompt_template.format(
            context=context_text,
            resume=resume_text[:3000],
            job_description=job_description_text[:3000]
        )
    ).content
    
    return report, relevant_docs
