# PharmaGen-AI-Copilot

**AI-Assisted Document Intelligence and Investigation Support System for Pharmaceutical Manufacturing**

## 📌 Project Overview

PharmaGen AI Copilot is a proposed academic prototype that combines **Retrieval-Augmented Generation (RAG)** with **Generative AI** to assist pharmaceutical manufacturing engineers in retrieving relevant information from technical documents and supporting investigation of process or batch-related issues.

The system allows users to upload pharmaceutical manufacturing documents in PDF format, process and index their content, retrieve relevant evidence, and generate AI-assisted responses based on the retrieved document context.

The system is designed as an **investigation-support tool**. It does not replace QA/QC personnel, approved procedures, or final technical decisions.

---

## 🎯 Objectives

* Provide a centralized interface for pharmaceutical manufacturing document analysis.
* Retrieve relevant information from uploaded technical documents.
* Support investigation of batch and process deviations.
* Provide evidence-based AI-assisted responses using retrieved document content.
* Generate investigation reports in PDF format.
* Maintain investigation information during the active application session.

---

## ✨ Key Features

### 📄 Document Intelligence

* Upload PDF documents related to pharmaceutical manufacturing.
* Extract text from uploaded documents.
* Preserve document and page-level information.
* Split extracted content into smaller searchable chunks.

### 🔎 RAG-Based Retrieval

* Generate embeddings for document chunks.
* Store embeddings using a **FAISS vector store**.
* Retrieve the most relevant document sections for a user query.
* Provide source document and page information with retrieved evidence.

### 🤖 AI Copilot

* Ask questions about uploaded documents.
* Generate AI-assisted answers using retrieved context.
* Support investigation-oriented questions such as:

  * Process deviations
  * Abnormal process conditions
  * Possible contributing factors
  * Investigation gaps
  * Supporting evidence

### 📑 Investigation Reports

* Generate investigation-support reports in PDF format.
* Include the investigation question, AI-assisted answer, and source information.

### 📊 Application Dashboard

The application provides four main sections:

* **Dashboard**
* **Documents**
* **AI Copilot**
* **Reports**

---

## 🏗️ System Workflow

```text
PDF Upload
     ↓
Save PDF
     ↓
Extract Text
     ↓
Page-wise Processing
     ↓
Chunking
     ↓
Generate Embeddings
     ↓
FAISS Vector Store
     ↓
Retrieve Relevant Context
     ↓
Gemini Generative AI
     ↓
AI-Assisted Answer
     ↓
Investigation Report
```

---

## 🤖 RAG Architecture

The system follows a Retrieval-Augmented Generation approach.

```text
              ┌──────────────────┐
              │   PDF Documents  │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │  Text Extraction │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │     Chunking     │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │    Embeddings    │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │  FAISS Vector DB │
              └────────┬─────────┘
                       ↓
User Query ───────→ Retrieval
                       ↓
              Relevant Context
                       ↓
              ┌──────────────────┐
              │ Gemini Generative│
              │       AI         │
              └────────┬─────────┘
                       ↓
                 AI Response
```

---

## 🛠️ Technologies Used

| Technology            | Purpose                           |
| --------------------- | --------------------------------- |
| Python                | Core programming language         |
| Streamlit             | Web application interface         |
| LangChain             | Document and retrieval workflow   |
| FAISS                 | Vector similarity search          |
| Sentence Transformers | Text embeddings                   |
| Google Gemini         | Generative AI response generation |
| PyPDF                 | PDF text extraction               |
| fpdf2                 | PDF report generation             |
| python-dotenv         | Environment variable management   |

---

## 📂 Project Structure

```text
PharmaGen-AI-Copilot/
│
├── app/
│   ├── gemini_client.py
│   ├── pdf_processor.py
│   ├── rag_engine.py
│   └── report_generator.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Main Modules

**`app.py`**
Main Streamlit application containing the user interface and application workflow.

**`app/pdf_processor.py`**
Handles PDF processing and page-wise text extraction.

**`app/rag_engine.py`**
Handles text chunking, embeddings, FAISS vector-store creation, and relevant-context retrieval.

**`app/gemini_client.py`**
Handles communication with the Gemini Generative AI model for AI-assisted responses.

**`app/report_generator.py`**
Generates investigation-support reports in PDF format.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Prashik878/PharmaGen-AI-Copilot.git
```

### 2. Open the Project Directory

```bash
cd PharmaGen-AI-Copilot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

The application requires a Gemini API key.

Create a local `.env` file in the project root:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

**Do not upload the `.env` file or API key to GitHub.**

The API key should be stored only as an environment variable.

---

## ▶️ How to Run

After installing the dependencies and configuring the environment:

```bash
streamlit run app.py
```

The application will open in the browser through the Streamlit local server.

---

## 📱 Application Modules

### 1. Dashboard

Provides an overview of the application and document-processing status.

### 2. Documents

Allows users to upload and process pharmaceutical manufacturing PDF documents.

### 3. AI Copilot

Allows users to ask questions and retrieve AI-assisted answers based on the uploaded document evidence.

### 4. Reports

Allows users to generate investigation-support reports from the investigation information.

---

## 🔎 Example Investigation Questions

The system can be used for questions such as:

```text
What abnormalities are reported in the batch record?

What evidence supports the possible causes of the deviation?

What investigation gaps remain?

Which document and page contain evidence related to the abnormal process condition?
```

---

## 🔒 Security Considerations

* API keys are managed through environment variables.
* API keys should not be committed to the repository.
* Sensitive pharmaceutical or organizational documents should only be used according to the applicable organizational policies.
* The system is intended as an academic investigation-support prototype.

---

## ⚠️ Disclaimer

PharmaGen AI Copilot is an **academic prototype for investigation support**.

The generated responses are intended to assist users in reviewing retrieved document evidence. The system does not independently establish a confirmed root cause, replace approved pharmaceutical procedures, or make final QA/QC or manufacturing decisions.

Final conclusions and actions must be reviewed and approved by appropriately qualified personnel.

---

## 👥 Team Members

**Group:** 13
**College:** Rasiklal M. Dhariwal Institute of Technology, Chinchwad

| No. | Team Member       |
| --- | ----------------- |
| 1   | Prashik G. Wagh   |
| 2   | Siddhant S. Kadam |
| 3   | Adinath Gitte     |

---

## 🚀 Project Status

**Status:** Proposed Academic Prototype

The project demonstrates the planned integration of document processing, vector-based retrieval, and Generative AI for pharmaceutical manufacturing investigation support.
