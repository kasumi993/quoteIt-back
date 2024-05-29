# QuoteTier Backend

This is the backend application for QuoteTier, a platform for managing and sharing inspirational quotes. The backend is built using Flask and PostgreSQL, and it includes functionality for adding, retrieving, liking, unliking, and deleting quotes.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Add new quotes with author, content, creator, and likes.
- Retrieve all quotes or search quotes by content or author.
- Like or unlike quotes.
- Delete quotes.

## Requirements

- Python 3.9+
- Docker

### Technologies Used: Flask, postgres

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/quotetier-backend.git
    cd quotetier-backend
    ```

2. **Build and start the project using Docker:**

    ```sh
    docker-compose up --build
    ```


## Usage

The application exposes several API endpoints for managing quotes. You can use tools like `curl`, Postman, or any other API client to interact with these endpoints.
