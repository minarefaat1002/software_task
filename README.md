# 🚀 RightsHero Software Engineer Task Assessment

Welcome to the RightsHero assessment project! This guide will walk you through setup, usage, and deployment.  
**🎬 [Video Demo Here](https://drive.google.com/file/d/1c7-t_wiHlvXZGWInPIbxrfVCQzL7m86r/view)**

---

## 📚 Table of Contents

- [📝 Project Overview](#project-overview)
- [✨ Features](#features)
- [🗄️ Database Design](#database-design)
- [🔗 API Endpoints](#api-endpoints)
- [🐳 Running the Project Locally](#running-the-project-locally)
- [🌐 Accessing the Service](#accessing-the-service)
- [☁️ AWS CloudFormation Deployment](#aws-cloudformation-deployment)
- [🛠️ Technical Stack](#technical-stack)
- [🔒 Security Considerations](#security-considerations)
- [🔮 Future Enhancements](#future-enhancements)

---

## 📝 Project Overview

A FastAPI-based web service for managing hierarchical categories with unlimited nesting, powered by PostgreSQL.  
Ready to run locally with Docker Compose and deployable to AWS using CloudFormation.

---

## ✨ Features

- 🏷️ **Unlimited Hierarchical Categories**: Organize categories and subcategories with no depth limit.
- 🔍 **RESTful API with Docs**: Swagger/OpenAPI documentation auto-generated.
- 🗄️ **Self-Referencing Table**: One simple table for all category levels.
- 🐳 **Dockerized**: Quick local setup using Docker Compose.
- ☁️ **AWS CloudFormation Ready**: One command deploy to AWS.

---

## 🗄️ Database Design

Uses a **self-referencing table** for unlimited category nesting.

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- 🔁 `parent_id` references `id` in the same table.
- 🧩 Scalable and simple for tree structures.

---

## 🔗 API Endpoints

All endpoints are documented at [http://localhost/docs](http://localhost/docs) (Swagger UI).

### ➕ Create Category

- **POST** `/categories/`
- **Body:**
  ```json
  {
    "name": "Category Name",
    "parent_id": null // or integer for subcategory
  }
  ```
- If `parent_id` is provided, the category is a child; otherwise, it's a root category.

---

### 📂 Get Categories

- **GET** `/categories/`
- **Query param:** `parent_id` (optional)
  - No `parent_id` returns root categories.
  - With `parent_id`, returns its children.
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "name": "Category B",
      "parent_id": null,
      "children": [
        {
          "id": 3,
          "name": "Sub Category B2",
          "parent_id": 1
        }
      ]
    }
  ]
  ```

---

### 🗑️ Delete Category

- **DELETE** `/categories/{category_id}`
- If the category exists, it's deleted (if the category has children, it willn't be deleted).
- Returns `204 No Content` on success, `404` if not found and `400 Bad Request` if it has children

---

## 🐳 Running the Project Locally

### Prerequisites

- Docker & Docker Compose installed

### Steps

1. **Clone the repo:**
   ```bash
   git clone https://github.com/minarefaat1002/software_task.git
   cd software_task
   ```
2. **Start services:**
   ```bash
   docker-compose up
   ```

---

## 🌐 Accessing the Service

- 🖥️ **Web Service:** [http://localhost](http://localhost)
- 📝 **API Docs:** [http://localhost/docs](http://localhost/docs)

---

## ☁️ AWS CloudFormation Deployment

Deploy the stack to AWS with the provided CloudFormation template.

### Requirements

- AWS CLI configured
- A key pair in the **eu-north-1** region

### Deploy

```bash
aws cloudformation create-stack --region eu-north-1 \
  --stack-name rightshero-ubuntu-stack \
  --template-body file://cloudformation.yml \
  --parameters ParameterKey=KeyPairName,ParameterValue=YOUR_KEY_PAIR_NAME \
  --capabilities CAPABILITY_IAM
```

- 🔑 **Replace** `YOUR_KEY_PAIR_NAME` with your AWS EC2 key pair name.
- ⚠️ **Note:**
  - The deployment **only works in eu-north-1** because the AMI is region-specific.
  - EC2 is open for SSH (22), HTTP (80), and HTTPS (443).
  - An IAM role with admin privileges will be created and attached to the instance.
  - The project is deployed automatically on the created EC2 instance.

---

## 🛠️ Technical Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Infrastructure:** Docker, AWS CloudFormation

---

## 🔒 Security Considerations

- 🛡️ Strong input validation on all endpoints
- 🚦 Proper error handling and status codes
- 🔐 IAM role is used only for assessment; scope for production!
- 🐳 Isolated Docker containers

---

## 🔮 Future Enhancements

- 🔑 Authentication/Authorization
- 🚦 Rate limiting
- 🔍 Advanced querying/filtering

---

## 📞 Contact Information

- ✉️ **Email:** mina.samaan888@gmail.com
- 💼 **LinkedIn:** [linkedin.com/in/minarefaat](https://linkedin.com/in/minarefaat)
- 📱 **Phone:** +01024271838

> 🎬 **A video demo of the project is available at:**  
> [https://drive.google.com/file/d/1c7-t_wiHlvXZGWInPIbxrfVCQzL7m86r/view](https://drive.google.com/file/d/1c7-t_wiHlvXZGWInPIbxrfVCQzL7m86r/view)
