# Minimal Chat

A simple Python-based chat application that uses **LangChain** and other libraries to enable text-based interactions. This project aims to demonstrate how to integrate various language model tools in a minimalistic setup.

---

## Table of Contents

1. [Description](#description)
2. [Technologies Used](#technologies-used)
3. [Installation Instructions](#installation-instructions)
4. [Usage Instructions](#usage-instructions)
5. [License](#license)

---

## Description

**Minimal Chat** is a Python application that leverages LangChain, a framework for building language model-powered applications. The app allows users to interact with a model to ask questions and retrieve answers based on predefined data.

---

## Technologies Used

- **Python** (version 3.6+)
- **LangChain** for question answering and chain-based language model interaction
- **Flask** or **FastAPI** (if applicable for running a web service)
- **Docker** (optional, if the app is containerized)

---

## Installation Instructions

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/chris-currie/chat-with-pdf.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd chat-with-pdf
    ```

3. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    ```

4. **Activate the virtual environment**:
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```

5. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Set up environment variables** (if needed, e.g., API keys or config files). You will need to specify your OPEN_API_KEY in your environment. If running locally then create an `.env` file with OPEN_API_KEY=your-key.

---

## Usage Instructions

After setting up the project, you can run it locally by following these steps:

1. **Run the application**:
    - If you're using a Flask app, you can run it with:
      ```bash
      python app.py
      ```
    - If using FastAPI, start the server:
      ```bash
      uvicorn app:app --reload
      ```

2. **Interact with the chat**:
    - Open your browser and navigate to the local server (typically `http://127.0.0.1::8501`).
    - Begin chatting or querying the model.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
