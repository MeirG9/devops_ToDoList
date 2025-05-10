# DevOps Matala 1 – To-Do List Service

A simple, containerized To-Do List REST API built with Flask and Redis.  
Designed to demonstrate best practices in DevOps: version control, branch protection, containerization, data persistence, and collaborative workflows.

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation & Startup](#installation--startup)  
- [API Reference](#api-reference)  
  - [Create To-Do List](#create-to-do-list)  
  - [Get All To-Do Lists](#get-all-to-do-lists)  
  - [Get Single To-Do List](#get-single-to-do-list)  
  - [Delete To-Do List](#delete-to-do-list)  
- [Architecture](#architecture)  
- [Development Workflow](#development-workflow)  
- [Branch Protection Rules](#branch-protection-rules)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

- **CRUD operations** for named To-Do lists  
- **In-memory data store** with Redis and persistence via Docker volume  
- **Containerized** using Docker and Docker Compose  
- **RESTful API** with JSON input/output  
- **Branch protection** and pull-request–based workflow

---

## Prerequisites

- [Docker](https://www.docker.com/) ≥ 20.10  
- [Docker Compose](https://docs.docker.com/compose/) ≥ 1.29  
- Git ≥ 2.25  

---

## Installation & Startup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-user/devops-matala1.git
   cd devops-matala1
   ```

2. **Start services with Docker Compose**  
   ```bash
   docker-compose up --build
   ```

3. The API will be available at `http://localhost:5000`.

---

## API Reference

All requests and responses use JSON.  
By default, the service listens on port **5000**.

### Create To-Do List

- **Endpoint:** `POST /todo`  
- **Request Body:**  
  ```json
  {
    "tasks": [
      "Buy milk",
      "Write report",
      "Call Alice"
    ]
  }
  ```
- **Responses:**  
  - `201 Created`  
    ```json
    {
      "id": 1,
      "message": "To-Do List saved successfully"
    }
    ```
  - `400 Bad Request` if `tasks` is missing or not a list.

### Get All To-Do Lists

- **Endpoint:** `GET /todos`  
- **Response:**  
  ```json
  {
    "1": ["Buy milk","Write report"],
    "2": ["Pay bills","Plan trip"]
  }
  ```

### Get Single To-Do List

- **Endpoint:** `GET /todo/{id}`  
- **Response:**  
  - `200 OK`  
    ```json
    {
      "id": "1",
      "tasks": ["Buy milk","Write report"]
    }
    ```
  - `404 Not Found` if the list does not exist.

### Delete To-Do List

- **Endpoint:** `DELETE /todo/{id}`  
- **Response:**  
  - `200 OK`  
    ```json
    {
      "message": "To-Do List deleted"
    }
    ```
  - `404 Not Found` if the list does not exist.

---

## Architecture

Client (curl/Postman)    │ ───▶ │   Flask App (app/main.py)    │ ───▶ │  Redis (cache+DB) 

- **Flask App** listens on port 5000, handles HTTP routes, serializes JSON, and communicates with Redis.  
- **Redis** stores To-Do data under `todo:{id}` keys and manages a `next_todo_id` counter.  
- **Docker Compose** defines two services (`web` and `redis`) and a named volume (`redis-data`) for data persistence.

---

## Development Workflow

1. **Create a feature branch** off `main`:
   ```bash
   git checkout -b feature/your-name
   ```
2. **Make changes**, then commit:
   ```bash
   git add .
   git commit -m "Add <short-description>"
   ```
3. **Push branch** to remote:
   ```bash
   git push -u origin feature/your-name
   ```
4. **Open a Pull Request** against `main`, request at least one review, and pass CI checks.
5. After approval and green CI, **merge** into `main`.

---

## Branch Protection Rules

- **Require pull request** before merging into `main`  
- **Require at least 1 approving review**  
- **Require status checks to pass** (e.g., CI/build)  
- **Require conversation resolution** before merge  

---

## Contributing

Contributions are welcome! Please follow the Development Workflow above and ensure all tests and linters pass before submitting a Pull Request.

---

## License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.
