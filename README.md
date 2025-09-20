# JLPT Exams API

A simple Node.js Express API to serve JLPT exam data. This API allows you to retrieve full exam content or filter questions by specific skills (vocabulary, grammar, reading, listening).

## Prerequisites

- [Node.js](https://nodejs.org/) (v14 or later recommended)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)

## Installation

1.  Clone the repository or download the source code.
2.  Navigate to the project directory:
    ```bash
    cd exams-api
    ```
3.  Install the required dependencies:
    ```bash
    npm install
    ```

## Running the Server

To start the API server, run the following command from the project root:

```bash
node server.js
```

The server will start and listen on `http://localhost:3000`.

## API Authentication

All API endpoints require an API key. This project uses the `dotenv` package to manage environment variables.

1.  Create a file named `.env` in the root of the project.
2.  Add your API key to the `.env` file as follows:
    ```
    API_KEY=your_secret_key_here
    ```
3.  The server will automatically load this key. The `.gitignore` file is configured to prevent the `.env` file from being committed to Git.

When making requests, you must include the API key in the `X-API-Key` header.

**Example using cURL:**

```bash
curl -H "X-API-Key: your_secret_key_here" http://localhost:3000/exams
```

If the key is missing or invalid, the API will respond with a `401 Unauthorized` error.

## API Endpoints

The API is structured to be browsable, allowing you to discover content step-by-step.

### Browsable Endpoints

-   `GET /exams`
    -   Lists available sources (`official`, `custom`).
-   `GET /exams/:source`
    -   Lists available JLPT levels for a given source (e.g., `N1`, `N2`).
-   `GET /exams/:source/:level`
    -   Lists available test types (`jlpt_test`, `skills_test`).
-   `GET /exams/:source/:level/jlpt_test`
    -   Lists all available exam IDs for the full test.
-   `GET /exams/:source/:level/skills_test`
    -   Lists all available skills for skill-based tests (`vocabulary`, `grammar`, etc.).
-   `GET /exams/:source/:level/skills_test/:skillId`
    -   Lists all available exam IDs for a specific skill.

### Specific Content Endpoints

-   `GET /exams/:source/:level/jlpt_test/:id`
    -   Returns the full content of a specific exam.
    -   **Example:** `/exams/official/N1/jlpt_test/n1_2010_07`
-   `GET /exams/:source/:level/skills_test/:id/:skillId`
    -   Returns specific sections of an exam that correspond to a particular skill.
    -   **Example:** `/exams/official/N1/skills_test/n1_2010_07/vocabulary`

