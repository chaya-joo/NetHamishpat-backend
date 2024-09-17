# Python Project with Flask, PyPyODBC, PyJWT, and More

## Overview
This project is a Python-based web application that uses several key libraries to provide secure and efficient functionality. It includes user authentication, file uploads, communication with databases, and external services such as email and SMS notifications. The application is built using **Flask** as the web framework, and it integrates with a relational database using **PyPyODBC**. Additionally, the project ensures security with **PyJWT** for token-based authentication and uses **Requests** for making HTTP calls to external APIs.

## Libraries Used

### 1. Flask
Flask is a lightweight web framework for Python that allows easy setup of web servers and routing. It was chosen for its simplicity and flexibility, making it ideal for small to medium web applications.

- **Usage**: Handles web routes, API requests, and responses.
- **Why Flask?**: Flask is easy to set up and allows rapid development of web applications, making it a great fit for our project's needs.

### 2. PyPyODBC
**PyPyODBC** is a Python library for connecting to ODBC-compliant databases (such as SQL Server) in a simple and consistent manner. It provides access to relational databases and allows the execution of SQL queries.

- **Usage**: Connecting to and interacting with our database to store and retrieve user data, file information, and other relevant records.
- **Why PyPyODBC?**: This library provides a lightweight and cross-platform way to connect to ODBC databases, which is important for portability and ease of use with SQL Server.

### 3. OS
**OS** is a standard Python library that provides a way to interact with the operating system. It allows us to perform actions like reading environment variables and managing file paths.

- **Usage**: Reading environment variables (e.g., API keys, database connection strings) and managing file paths for uploads and storage.
- **Why OS?**: The OS library is essential for managing environment variables and performing OS-level file operations securely and efficiently.

### 4. PyJWT
**PyJWT** is a Python library used to encode and decode JSON Web Tokens (JWT). JWTs are used for secure transmission of information between parties as JSON objects, often used in authentication systems.

- **Usage**: Used to generate and validate JWTs for secure user authentication and authorization.
- **Why PyJWT?**: JWTs are a secure way to transmit user information between client and server without exposing sensitive details. This is critical for ensuring security in authentication workflows.

### 5. Requests
**Requests** is a popular Python library for sending HTTP requests to external APIs. It simplifies making GET, POST, PUT, and DELETE requests and handling responses.

- **Usage**: Sending HTTP requests to external services (such as SMS and email providers) for notifications and verification purposes.
- **Why Requests?**: Requests is simple, intuitive, and reliable, which makes it ideal for communicating with external APIs.

### 6. Python-dotenv
**Python-dotenv** is a library that loads environment variables from a `.env` file into the Python environment. It helps manage configuration and sensitive data like API keys and database credentials in a secure way.

- **Usage**: Loads environment variables (e.g., API keys, database credentials, secret tokens) from the `.env` file.
- **Why Python-dotenv?**: Managing sensitive information securely in environment variables is a best practice. Python-dotenv simplifies this process by allowing us to store this information outside the codebase in a dedicated configuration file.

### 7. zeep
Zeep is a modern and easy-to-use SOAP client for Python. It allows for seamless interaction with SOAP-based web services by handling the complexities of the SOAP protocol and converting data between SOAP and Python objects.

- Usage: Communicating with SOAP-based web services, sending requests, and handling responses.
- Why zeep?: zeep simplifies working with SOAP services, making it easier to integrate with legacy systems and services that use the SOAP protocol.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/chaya-joo/NetHamishpat-backend.git
    cd project
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** at the root of the project and define the following variables:

    ```
    SEND_SMS_API_KEY=your_sms_api_key
    SEND_SMS_USER=your_sms_user
    SEND_SMS_PASSWORD=your_sms_password
    SEND_SMS_SENDER=your_sms_sender

    EMAIL_SENDER=your_email_sender
    EMAIL_SENDER_PASSWORD=your_email_password

    SERVER=your_server_driver
    SERVER_NAME=your_server_name
    DATABASE_NAME=your_database_name

    SECRET_KEY=your_secret_key
    TOKEN_ALGORITHM=HS256  # or your preferred algorithm
    ```

5. **Run the Flask server:**

    ```bash
    flask run
    ```

## Usage

### API Endpoints
The project exposes several API endpoints:

- **`POST /verifyUser`**: Verifies the user's identity by email or phone.
- **`POST /verifyCode`**: Verifies the user-provided code and returns an authentication token.
- **`POST /uploadFile`**: Uploads a file to the server and stores it in the database.
- **`POST /getSittings`**: Retrieves all sittings of the user by case-number from net-hamishpat.
- **`POST /getDecisions`**: Retrieves all decisions of the user by case-number from net-hamishpat.

### Authentication
- Users are authenticated using a JWT token. After a user is verified, a token is generated and returned. The token should be passed in the `Authorization` header for secure API access.

## Error Handling
The project implements consistent error handling for all routes and functions, ensuring that any unexpected behavior or failure is reported with appropriate error messages. The system catches exceptions and returns structured responses to the client.

## Conclusion
This project demonstrates how to build a Python web application using Flask, secure it with JWT tokens, interact with a relational database using PyPyODBC, and communicate with external services via HTTP requests. The use of environment variables ensures sensitive information is handled securely, and the consistent error handling throughout the project ensures reliability and maintainability.
