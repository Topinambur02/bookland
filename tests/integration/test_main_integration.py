class TestAPI:
    def test_read_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Добро пожаловать в систему управления библиотекой!"}

    def test_get_nonexistent_book(self, client):
        response = client.get("/books/999")
        assert response.status_code == 404
        assert "message" in response.json()

    def test_create_branch(self, client, sample_branch_data: dict):
        response = client.post("/branches/", json=sample_branch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_branch_data["name"]
        assert "id" in data

    def test_create_faculty(self, client, sample_faculty_data: dict):
        response = client.post("/faculties/", json=sample_faculty_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_faculty_data["name"]
        assert "id" in data

    def test_get_books_empty(self, client):
        response = client.get("/books/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_branches_empty(self, client):
        response = client.get("/branches/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_faculties_empty(self, client):
        response = client.get("/faculties/")
        assert response.status_code == 200
        assert response.json() == []