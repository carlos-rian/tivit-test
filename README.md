# TIVIT Backend Challenge

This repository contains the solution for the TIVIT Backend Challenge.

The project is a REST API that provides endpoints below:

- `GET /fake/health`: Check if the API is running.
- `POST /fake/token`: Generate a JWT token. Based on the username and password provided in the query parameters.
- `GET /fake/user`: This endpoint is protected by JWT. The user must have the role `user` to access it.
- `GET /fake/admin`: This endpoint is protected by JWT. The user must have the role `admin` to access it.

The Code Coverage is 100% for the project.

- `Code`: https://github.com/carlos-rian/tivit-test
- `Code Coverage`: https://app.codecov.io/github/carlos-rian/tivit-test/tree/main


## Requirements

**Run API**:
    - [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (Containerization)

**Run Tests**:
    - [Python 3.12](https://www.python.org/) (Language used in the project)
    - [UV](https://astral.sh/blog/uv) (Python's Package Manager)

## Running the project using Docker

Enter the project directory, then, you can run the project, you need to execute the following commands:

```bash
docker-compose up --build
```

The project will be available at `http://localhost:8000`.

You can run some requests using the interface provided by Scalar at `http://localhost:8000/scalar`.


## Running the tests locally

To run the tests, you need to execute the following commands:

1. Install Python 3.12
    ```bash
    uv python install 3.12
    ```

2. Create the virtualenv and install the project dependencies
    ```bash
    uv sync --all-extras --dev
    ```

3. Create a postgres database
    ```bash
    docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres
    ```

4. Set the environment variables, the JWT_SECRET_KEY is a secret key that you can define.
    ```bash
    export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/postgres"
    export JWT_SECRET_KEY="MY_SECRET_KEY"
    ```

5. Run the tests
    ```bash
    task test
    ```

6. Generate the coverage report
    ```bash
    task coverage
    ```

7. Open the coverage report in your browser
- htmlcov/index.html