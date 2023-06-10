# ternaku-bangkit-Cloud-Computing
Cloud Computing Capstone Project
Dokumentasi Backend:

# Backend Documentation Ternaku

## Database Schema Ternaku

### Table: articles

| Column    | Type         | Null | Key | Default | Extra          |
|-----------|--------------|------|-----|---------|----------------|
| id        | int          | NO   | PRI | NULL    | auto_increment |
| title     | varchar(255) | NO   |     | NULL    |                |
| content   | text         | YES  |     | NULL    |                |
| img_url   | text         | YES  |     | NULL    |                |

### Table: history

| Column            | Type         | Null | Key | Default | Extra          |
|-------------------|--------------|------|-----|---------|----------------|
| id                | int          | NO   | PRI | NULL    | auto_increment |
| user_id           | int          | YES  | MUL | NULL    |                |
| animal_category   | varchar(255) | YES  |     | NULL    |                |
| prediction_result | varchar(255) | YES  |     | NULL    |                |
| image_url         | varchar(255) | YES  |     | NULL    |                |
| created_at        | datetime     | YES  |     | NULL    |                |

### Table: products

| Column      | Type         | Null | Key | Default | Extra          |
|-------------|--------------|------|-----|---------|----------------|
| id          | int          | NO   | PRI | NULL    | auto_increment |
| name        | varchar(255) | NO   |     | NULL    |                |
| price       | text         | NO   |     | NULL    |                |
| description | text         | YES  |     | NULL    |                |
| img_url     | varchar(255) | YES  |     | NULL    |                |

### Table: users

| Column    | Type         | Null | Key | Default | Extra          |
|-----------|--------------|------|-----|---------|----------------|
| user_id   | int          | NO   | PRI | NULL    | auto_increment |
| email     | varchar(255) | NO   |     | NULL    |                |
| password  | varchar(255) | NO   |     | NULL    |                |
| fullname  | varchar(255) | NO   |     | NULL    |                |



## Endpoint Documentation Ternaku

### Authentication

#### Register User
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

#### Login User
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
          "email": "user@example.com",
          "fullname": "John Doe",
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

#### Predict Sapi
- **Endpoint:** /api/predictsapi
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

#### Predict Kambing
- **Endpoint:** /api/predictkambing
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
    -

 JSON Response:
      ```json
      {
        "error": false,
        "history": [
          {
            "id": 1,
            "user_id": 1,
            "animal_category": "Sapi",
            "prediction_result": "Mata Terjangkit Penyakit Pinkeye",
            "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg",
            "created_at": "2023-06-10 12:34:56"
          },
          {
            "id": 2,
            "user_id": 1,
            "animal_category": "Kambing",
            "prediction_result": "Mata Hewan Kamu Sehat!",
            "image_url": "https://storage.googleapis.com/bucket_name/image_folder/image_filename.jpg",
            "created_at": "2023-06-11 09:12:34"
          }
        ]
      }
      ```

#### Get User Profile
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
          "email": "user@example.com",
          "fullname": "John Doe"
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
    - Response Body: `Halo! John Doe`

#### Root
- **Endpoint:** /
- **Method:** GET
- **Response:** Welcome to the Ternaku

## Conclusion

This documentation provides an overview of the backend code and the corresponding API endpoints. It includes information about user authentication, image classification, user profile, product management, and article management. Each endpoint is described with its URL, method, request body (if applicable), request headers, and response structure.

Please note that the code and documentation provided are based on the given code snippet, and additional implementation details or modifications may be required based on specific requirements or system configurations.
