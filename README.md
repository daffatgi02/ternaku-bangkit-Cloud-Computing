# Ternaku Backend Documentation

Welcome to the Ternaku backend application documentation. Ternaku is a livestock prediction system that utilizes machine learning models to predict the health of livestock animals based on images.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database](#database)
- [API Endpoints](#api-endpoints)
  - [Register](#register)
  - [Login](#login)
  - [Predict Cattle](#predict-cattle)
  - [Predict Goat](#predict-goat)
  - [Get History](#get-history)
  - [Get Products](#products)
  - [Get Articles](#articles)
  - [Get Profile](#profile)
  - [Homepage](#homepage)
- [Running the Application](#running-the-application)

## Prerequisites

Before running the Ternaku backend application, make sure you have the following installed:

- Python 3.6 or later
- TensorFlow
- PyMySQL
- Flask
- Flask-Cors
- Flask-JWT-Extended
- Google Cloud Storage library

## Installation

1. Clone the repository from GitHub:

   ```shell
   git clone https://github.com/Ternaku-id/ternaku-bangkit-Cloud-Computing.git
   ```

2. Change into the project directory:

   ```shell
   cd ternaku-bangkit-Cloud-Computing
   ```

3. Install the required dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, you need to configure the following settings in the `app.py` file:

- MySQL database configuration:
  - `app.config['MYSQL_HOST']`: The MySQL server host.
  - `app.config['MYSQL_USER']`: The MySQL username.
  - `app.config['MYSQL_PASSWORD']`: The MySQL password.
  - `app.config['MYSQL_DB']`: The name of the MySQL database.
- JWT secret key:
  - `app.config['JWT_SECRET_KEY']`: A secret key used for JWT token generation. You can generate a random key or provide your own.
- Google Cloud service account key:
  - `service_account_key_path`: The path to your Google Cloud service account key file.
- Model file paths:
  - `cattle_model_blob`: The path to the TFLite model file for predicting cattle.
  - `goat_model_blob`: The path to the TFLite model file for predicting goat.


## Database Schema Ternaku
### Database

This repository contains the SQL code to create and manage the database schema for a web application. The schema includes tables for users, history, products, and articles. Below is the structure and details of each table:

### Table: users

This table stores information about the users of the application.

| Column       | Data Type    | Constraints    |
| ------------ | ------------ | -------------- |
| user_id      | INT          | PRIMARY KEY, AUTO_INCREMENT |
| email        | VARCHAR(255) | NOT NULL       |
| password     | VARCHAR(255) | NOT NULL       |
| fullname     | VARCHAR(255) | NOT NULL       |

### Table: history

This table keeps track of the user's activity history, such as predictions and image uploads.

| Column             | Data Type    | Constraints                           |
| ------------------ | ------------ | ------------------------------------- |
| id                 | INT          | PRIMARY KEY, AUTO_INCREMENT           |
| user_id            | INT          |                                     |
| animal_category    | VARCHAR(255) |                                     |
| prediction_result  | VARCHAR(255) |                                     |
| image_url          | VARCHAR(255) |                                     |
| created_at         | DATETIME     |                                     |
| FOREIGN KEY        | (user_id)    | REFERENCES users(user_id)             |

### Table: products

This table stores information about the products available in the application.

| Column       | Data Type    | Constraints    |
| ------------ | ------------ | -------------- |
| id           | INT          | PRIMARY KEY, AUTO_INCREMENT |
| name         | VARCHAR(255) | NOT NULL       |
| price        | FLOAT        | NOT NULL       |
| description  | TEXT         |                |

### Table: articles

This table stores articles published in the application.

| Column          | Data Type    | Constraints    |
| --------------- | ------------ | -------------- |
| id              | INT          | PRIMARY KEY, AUTO_INCREMENT |
| headline        | VARCHAR(255) |                |
| title           | VARCHAR(255) | NOT NULL       |
| content         | TEXT         |                |
| author          | VARCHAR(100) | NOT NULL       |
| published_date  | DATE         |                |
| category        | VARCHAR(50)  |                |
| img_url         | VARCHAR(255) |                |


## API Endpoints

### Authentication

#### Register

- **Endpoint:** /api/auth/register
- **Method:** POST
- **Request Body:**
  - email (string): User's email
  - password (string): User's password
  - fullname (string): User's full name
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response: 
      ```json
      {
        "error": false,
        "message": "Berhasil Register Akun. Silahkan Login"
      }
      ```
  - If email is already taken:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": true,
        "message": "Email already taken"
      }
      ```

#### Login

- **Endpoint:** /api/auth/login
- **Method:** POST
- **Request Body:**
  - email (string): User's email
  - password (string): User's password
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": false,
        "loginResult": {
          "email": "daffatgi02@gmail.com",
          "fullname": "Daffa Fakhuddin Arrozy",
          "token": "<access_token>",
          "userid": 1
        },
        "message": "Login Success"
      }
      ```
  - If email or password is incorrect:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": true,
        "message": "Wrong Password or Account not found"
      }
      ```

### Image Classification

#### Predict Cattle

- **Endpoint:** /api/predict-cattle
- **Method:** POST
- **Request Body:**
  - image (file): Image file to classify (JPEG format)
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "class": "Mata Terjangkit Penyakit Pinkeye",
        "probability": 0.8,
        "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
      }


      ```
  - If no image uploaded:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": "No image uploaded"
      }
      ```

#### Predict Goat

- **Endpoint:** /api/predict-goat
- **Method:** POST
- **Request Body:**
  - image (file): Image file to classify (JPEG format)
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "class": "Mata Hewan Kamu Sehat!",
        "probability": 0.9,
        "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
      }
      ```
  - If no image uploaded:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": "No image uploaded"
      }
      ```

### User Profile

#### Get History

- **Endpoint:** /api/profile/history
- **Method:** GET
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
        {
          "error": false,
          "history": [
            {
              "id": 1,
              "user_id": 1,
              "animal_category": "Cattle",
              "prediction_result": "Mata Terjangkit Penyakit Pinkeye",
              "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg",
              "created_at": "2023-06-10 12:34:56"
            },
            {
              "id": 2,
              "user_id": 1,
              "animal_category": "Goat",
              "prediction_result": "Mata Hewan Kamu Sehat!",
              "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg",
              "created_at": "2023-06-11 09:12:34"
            }
          ]
        }
      ```

#### Get User Profile
### Profile
- **Endpoint:** /api/profile
- **Method:** GET
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": false,
        "profile": {
          "email": "daffatgi02@gmail.com",
          "fullname": "Daffa Fakhuddin Arrozy"
        }
      }
      ```

### Products

#### Get All Products

- **Endpoint:** /api/products
- **Method:** GET
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - JSON Response:
      ```json
      [
        {
          "id": 1,
          "name": "Product 1",
          "price": "100",
          "description": "Product 1 description",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        },
        {
          "id": 2,
          "name": "Product 2",
          "price": "200",
          "description": "Product 2 description",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        }
      ]
      ```

#### Get Product by ID

- **Endpoint:** /api/products/<product_id>
- **Method:** GET
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If product exists:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": false,
        "product": {
          "id": 1,
          "name": "Product 1",
          "price": "100",
          "description": "Product 1 description",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        }
      }
      ```
  - If product not found:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": true,
        "message": "Product not found"
      }
      ```

### Articles

#### Get All Articles

- **Endpoint:** /api/articles
- **Method:** GET
- **Response:**
  - Status Code: 200
  - JSON Response:
    ```json
    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Article 1 content",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        },
        {
          "id": 2,
          "title": "Article 2",
          "content": "Article 2 content",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        }
      ]
    }
    ```

#### Get Article by ID

- **Endpoint:** /api/articles/<article_id>
- **Method:** GET
- **Response:**
  - If article exists:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "article": {
          "id": 1,
          "title": "Article 1",
          "content": "Article 1 content",
          "img_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg"
        }
      }
      ```
  - If article not found:
    - Status Code: 200
    - JSON Response:
      ```json
      {
        "error": "Article not found"
      }
      ```

### Miscellaneous

#### Homepage

- **Endpoint:** /homepage
- **Method:** GET
- **Request Headers:**
  - Authorization: Bearer <access_token>
- **Response:**
  - If successful:
    - Status Code: 200
    - Response Body: `Halo! Daffa Fakhuddin Arrozy`

#### Root

- **Endpoint:** /
- **Method:** GET
- **Response:** Welcome to Ternaku

## Running the Application

To run the Ternaku backend application, execute the following command:

```shell
python app.py
```

The application will start running on `http://localhost:8080/`.

Make sure you have the required dependencies installed and the necessary configurations set before running the application.

That's it! You have successfully set up and documented the Ternaku backend application.
