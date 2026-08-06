from fastapi.testclient import TestClient

from app.main import app

QUERIES = [
    "company policy",
    "leave application",
    "attendance policy",
    "vacation leave",
    "remote work",
    "working hours",
    "confidential information",
    "password policy",
    "payroll process",
    "overtime",
    "employee conduct",
    "harassment policy",
    "expense reimbursement",
    "termination process",
    "holiday schedule",
    "medical leave",
    "performance review",
    "security guidelines",
    "internet usage",
    "data privacy",
]


def test_retrieval_api():
    with TestClient(app) as client:

        for query in QUERIES:

            response = client.post(
                "/retrieval/search",
                json={
                    "query": query
                },
            )

            assert response.status_code == 200

            data = response.json()

            assert "result" in data
            assert isinstance(data["result"], list)
            assert len(data["result"]) > 0

            for result in data["result"]:

                assert "document_id" in result
                assert "chunk_id" in result
                assert "chunk_index" in result
                assert "department" in result
                assert "text" in result
                assert "score" in result

                assert isinstance(result["score"], float)

            print(f"✓ {query}")