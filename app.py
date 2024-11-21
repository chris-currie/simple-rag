import streamlit as st
import pypdf
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
import os
import chardet
import tempfile

def init_page():
    st.set_page_config(page_title="Document Chat Assistant")
    st.header("Chat with your Documents 💬")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

def detect_file_encoding(file_content):
    """Detect the encoding of the file content."""
    result = chardet.detect(file_content)
    return result['encoding'] or 'utf-8'

def process_file(file):
    """Process a single file and return text chunks."""
    # Get file extension
    file_extension = os.path.splitext(file.name)[1].lower()
    
    # Create a temporary file to handle the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file_name = tmp_file.name  # Save the file name
    try:
        if file_extension == '.pdf':
            # Handle PDF files
            loader = PyPDFLoader(tmp_file_name)
            pages = loader.load()
            text = '\n'.join(page.page_content for page in pages)
        else:
            # Handle text files with encoding detection
            content = file.getvalue()
            encoding = detect_file_encoding(content)
            text = content.decode(encoding)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        return text_splitter.split_text(text)
        
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_name)

            
def create_vectorstore(files):
    all_chunks = []
    
    # Process each file
    for file in files:
        try:
            chunks = process_file(file)
            all_chunks.extend(chunks)
        except Exception as e:
            st.error(f"Error processing file {file.name}: {str(e)}")
            continue
    
    if not all_chunks:
        raise ValueError("No valid text chunks were extracted from the files")
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(all_chunks, embeddings)
    return vector_store

def create_conversation_chain(vector_store):
    llm = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo')
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def main():
    init_page()
    
    # File upload
    with st.sidebar:
        st.subheader("Your documents")
        files = st.file_uploader(
            "Upload your files and click process",
            accept_multiple_files=True,
            type=['txt', 'pdf']  # Specify allowed file types
        )
        if st.button("Process"):
            if not files:
                st.error("Please upload at least one file first!")
            else:
                with st.spinner("Processing"):
                    try:
                        # Create vector store
                        st.session_state.vector_store = create_vectorstore(files)
                        # Create conversation chain
                        st.session_state.conversation = create_conversation_chain(
                            st.session_state.vector_store
                        )
                        st.success("Ready to chat!")
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not st.session_state.conversation:
                st.error("Please upload and process documents first!")
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Please upload and process documents first!"}
                )
            else:
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation({"question": prompt})
                    st.markdown(response['answer'])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response['answer']}
                    )

if __name__ == '__main__':
    main()