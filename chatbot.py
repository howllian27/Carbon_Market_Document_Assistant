from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from pdf_section_mapper import get_section_mapping
import streamlit as st

# Initialize environment variables
load_dotenv()


def create_embedding_index_from_text(document_text):
    # Create text segments from the document
    segmenter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_segments = segmenter.split_text(document_text)
    
    # Generate embeddings for the text segments
    text_embeddings_generator = OpenAIEmbeddings()
    embedding_index = FAISS.from_texts(text_segments, text_embeddings_generator)
    
    return embedding_index

def interactive_pdf_qa():
    st.title("Your Carbon Market Document Assistant 🌲")
    
    uploaded_pdf = st.file_uploader('Upload your PDF Document', type='pdf')
    
    # Check if pdf is uploaded
    if uploaded_pdf:
        pdf_content_reader = PdfReader(uploaded_pdf)
        # Accumulate text content from the PDF
        accumulated_text = ""

        # Iterate over all pages in the PDF
        for page in pdf_content_reader.pages:
            accumulated_text += page.extract_text()
        
        # Build the index of embeddings from the PDF text
        pdf_embedding_index = create_embedding_index_from_text(accumulated_text)
        
        # Enter user inputs
        user_query = st.text_input('Enter your question for the PDF')
        is_cancelled = st.button('Cancel')
        
        # Check if user has cancelled
        if is_cancelled:
            st.stop()
        
        # Check if user has entered a query
        if user_query:
            # Search for similar documents
            similar_documents = pdf_embedding_index.similarity_search(user_query)
            language_model = OpenAI()
            # Load the QA chain
            qa_chain = load_qa_chain(language_model, chain_type='stuff')
            
            # Run the QA chain and track the cost
            with get_openai_callback() as cost_tracker:
                answer = qa_chain.run(input_documents=similar_documents, question=user_query)
                print(cost_tracker)
                
            st.write(answer)
            
# Entry point for the Streamlit application
if __name__ == "__main__":
    interactive_pdf_qa()