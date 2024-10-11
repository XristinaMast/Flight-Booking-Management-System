# Flight Booking Management System

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [How to Run the System](#how-to-run-the-system)
7. [API Endpoints](#api-endpoints)
8. [How to Use the System (Examples)](#how-to-use-the-system-examples)


## Introduction

The **Flight Booking Management System** is a web-based application designed to manage flight bookings, cancellations, and flight details for users and administrators. It allows users to search for available flights, book tickets, and cancel reservations. Administrators have access to additional features such as managing flight details and user data.

This project is implemented using **Flask** as the web framework, **MongoDB** for data storage, and **Docker** for containerizing the application.

## Features

### User Features:
- User registration and login
- Search for available flights
- Book flights by specifying the desired date and time
- View and manage booked flights
- Cancel flight bookings

### Admin Features:
- Admin login with predefined credentials
- Manage flight schedules (add, update, delete flights)
- View and manage all user bookings

### Other Features:
- Secure password encryption
- Session management using cookies
- Persistent data storage using MongoDB

## Technologies Used

- **Flask**: A micro web framework for Python.
- **MongoDB**: NoSQL database for storing user and flight data.
- **Flask-PyMongo**: To integrate Flask with MongoDB.
- **Docker**: For containerizing the application for easy deployment.
- **Python 3.x**: Programming language for the backend logic.
- **Werkzeug**: To handle password encryption and security.

## Project Structure

```
Flight-Booking-Management-System/
│
├── app.py                 # Main application file with API routes
├── Dockerfile             # Instructions for building Docker image
├── docker-compose.yml     # Docker Compose configuration file
├── requirements.txt       # Project dependencies
├── static/                # Static files (CSS, images)
├── templates/             # HTML templates for rendering web pages
├── config.py              # Configuration file for database and app settings
└── README.md              # This readme file
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Docker**
- **Docker Compose**

### Python Libraries:

If you are not using Docker, install the required Python libraries:

```bash
pip install -r requirements.txt
```

### Docker:

Ensure that Docker and Docker Compose are installed on your machine. You can download them from [Docker's official website](https://www.docker.com/).

## How to Run the System

### Clone the Repository

```bash
git clone https://github.com/XristinaMast/Flight-Booking-Management-System.git
cd Flight-Booking-Management-System
```

### Running with Docker

1. Build and start the containers:

```bash
docker-compose up --build
```

2. Open your browser and navigate to:

```bash
http://localhost:5000
```

3. To stop the containers, press `Ctrl + C` in your terminal and then run:

```bash
docker-compose down
```

### Running without Docker

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Run the Flask app:

```bash
python app.py
```

3. Access the app by visiting:

```bash
http://localhost:5000
```

## API Endpoints

### User Endpoints

- **Register User**:  
  - `POST /register`
  - Example request:
    ```bash
    curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "user1", "password": "pass123"}'
    ```

- **Login User**:  
  - `POST /login`
  - Example request:
    ```bash
    curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "pass123"}'
    ```

- **Search Flights**:  
  - `GET /flights/search?origin=<origin>&destination=<destination>&date=<date>`
  - Example request:
    ```bash
    curl -X GET "http://localhost:5000/flights/search?origin=NYC&destination=LAX&date=2024-12-20"
    ```

- **Book a Flight**:  
  - `POST /flights/book`
  - Example request:
    ```bash
    curl -X POST http://localhost:5000/flights/book -H "Content-Type: application/json" -d '{"flight_id": "12345", "user_id": "56789"}'
    ```

- **Cancel a Booking**:  
  - `DELETE /flights/cancel/<booking_id>`
  - Example request:
    ```bash
    curl -X DELETE http://localhost:5000/flights/cancel/67890
    ```

### Admin Endpoints

- **Add a Flight**:  
  - `POST /flights/add`
  - Example request:
    ```bash
    curl -X POST http://localhost:5000/flights/add -H "Content-Type: application/json" -d '{"flight_number": "AA123", "origin": "NYC", "destination": "LAX", "date": "2024-12-20", "time": "10:00"}'
    ```

- **Update a Flight**:  
  - `PUT /flights/update/<flight_id>`
  - Example request:
    ```bash
    curl -X PUT http://localhost:5000/flights/update/12345 -H "Content-Type: application/json" -d '{"flight_number": "AA123", "origin": "NYC", "destination": "LAX", "date": "2024-12-21", "time": "12:00"}'
    ```

- **Delete a Flight**:  
  - `DELETE /flights/delete/<flight_id>`
  - Example request:
    ```bash
    curl -X DELETE http://localhost:5000/flights/delete/12345
    ```

## How to Use the System (Examples)

### 1. **User Registration and Login**
   - **Register**: A new user can sign up by sending a `POST` request to `/register`. Once registered, they can log in using the `/login` endpoint to receive a session cookie.

### 2. **Search for Flights**
   - **Search**: Users can search for available flights based on origin, destination, and date. The results include flight number, date, time, and availability.

### 3. **Booking and Canceling Flights**
   - **Book**: Users can select a flight and book it using the `POST /flights/book` endpoint.
   - **Cancel**: Booked flights can be canceled by sending a `DELETE` request to `/flights/cancel/<booking_id>`.

### 4. **Admin Flight Management**
   - **Add**: Admins can add new flights by sending a `POST` request to `/flights/add`.
   - **Update**: Admins can update flight details such as time, date, and flight number.
   - **Delete**: Admins can remove a flight from the system using a `DELETE` request.
