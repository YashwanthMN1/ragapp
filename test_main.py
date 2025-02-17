import pytest
from fastapi.testclient import TestClient
from main import app
import httpx

BASE_URL = "http://127.0.0.1:8000"  # Update if needed

@pytest.fixture
def client():
    """Fixture to provide an HTTP client for testing."""
    return httpx.Client(base_url=BASE_URL)


# def test_add_document(client):
#     """Test /add_document endpoint by uploading a file."""
#     file_path = "sample.text"
#     with open(file_path, "rb") as file:
#         files = {"file": (file_path, file, "application/pdf")}
#         response = client.post("/add_document", files=files)
    
#     assert response.status_code == 200
#     assert "success" in response.json() 



def test_list_doc_ids(client):
    """Test /list_doc_ids endpoint."""
    response = client.get("/list_doc_ids")
    
    assert response.status_code == 200
    # assert isinstance(response.json(), dict)  

def test_qa(client):
    """Test /ask endpoint with a query string."""
    query = "Tell me something about Karna"
    response = client.get("/ask", params={"query": query})
    
    assert response.status_code == 200
    assert isinstance(response.json(), dict) 

def test_select_document(client):
    """Test /select_document endpoint."""
    # doc_id = "example_doc_id"  
    response = client.post("/select_document", data={"selected_doc_id": "0a997ce5-2291-47ae-ac92-0646cad00015"})
    
    assert response.status_code == 200
    # assert "success" in response.json()  


if __name__ == "__main__":
    pytest.main()
