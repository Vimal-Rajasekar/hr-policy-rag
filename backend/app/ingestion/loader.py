from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

added = ["Agira Attendance Policy.pdf","Agira Buddy Refferal Policy.pdf","Agira Leave Policy.pdf","Agira Separation_Policy.pdf","Agira_Company_Code_of_Conduct__Ver1.0.pdf","Agira_Dress_Code_Policy.pdf","Agira_Variable_Pay Policy.pdf","Agira_Work From Home Policy.pdf","Agira- List of Holidays 2026.pdf","Implementation and SOP for Internal Complaints Committee V2.0 1.pdf"]

def load_pdfs(folder_path: str):
    documents = []
    for pdf_path in Path(folder_path).glob("*.pdf"):
        if pdf_path.name in added:
            print(f"Skipping already added file: {pdf_path.name}")
            continue
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        for d in docs:
            d.metadata["source_file"] = pdf_path.name
        documents.extend(docs)
    print(f"Loaded {len(documents)} documents from {folder_path}")
    print("Sample document metadata:", documents[0].metadata if documents else "No documents loaded")
    return documents
