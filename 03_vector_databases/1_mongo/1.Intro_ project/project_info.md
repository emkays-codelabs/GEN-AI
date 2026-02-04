


# 🚀 FastAPI MongoDB API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)
![AsyncIO](https://img.shields.io/badge/AsyncIO-supported-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-BaseModel-yellow.svg)
![dotenv](https://img.shields.io/badge/python--dotenv-green.svg)
![Deploy](https://img.shields.io/badge/Deploy-Render-purple.svg)

A **FastAPI-based REST API** that interacts with **MongoDB Atlas** using **Motor (async driver)**.  
Provides **CRUD operations** — insert, fetch, full/partial update, delete — **asynchronously** and efficiently.

The API uses **FastAPI**, **asyncio**, and **Motor** for **non-blocking, high-performance operations**, ideal for real-time apps.

---

## 🌟 Key Features

- ⚡ **FastAPI Framework** — high-performance async REST API  
- 🔄 **Async Database Access** — Motor driver for MongoDB  
- 🔐 **MongoDB Atlas** — secure & scalable cloud database  
- 📄 **Swagger UI** — interactive API docs (`/docs`)  
- ☁️ **Deployment-ready** — deploy easily on Render  
- 🗂️ Supports **CRUD operations**: Create, Read, Update (full/partial), Delete  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/emkays-codelabs/FastAPI-Guide.git
cd FastAPI-Guide
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/eurondb?retryWrites=true&w=majority
DB_NAME=eurondb
```

> 🚫 **Do not commit `.env` to GitHub.**

---

## 🖥️ Run the API Locally

```bash
uvicorn main:app --reload
```

* Open **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Check API health: `GET /`

---

## 🌐 API Endpoints

| #  | Method | Endpoint                  | Description                |
| -- | ------ | ------------------------- | -------------------------- |
| 7a | GET    | `/`                       | Health check               |
| 7b | GET    | `/get_eurondata`          | Fetch all records          |
| 7c | POST   | `/euron/insert_data`      | Insert new record          |
| 7d | PUT    | `/euron/update_data/{id}` | Full update of a record    |
| 7e | PATCH  | `/euron/patch_data/{id}`  | Partial update of a record |
| 7f | DELETE | `/euron/delete_data/{id}` | Delete a record            |

---

### Example: Insert Data

```json
POST /euron/insert_data
{
  "name": "Alice",
  "phone": 9876543210,
  "city": "Bangalore",
  "course": "AI"
}
```

**Response**

```json
{
  "status": "success",
  "message": "Record inserted successfully",
  "id": "642f1e3b8e1f1234abcd5678"
}
```

---

## 🗃️ MongoDB Collection Structure

| Field  | Type     | Description       |
| ------ | -------- | ----------------- |
| `_id`  | ObjectId | MongoDB unique ID |
| name   | string   | Name of the user  |
| phone  | int      | Phone number      |
| city   | string   | City              |
| course | string   | Course enrolled   |

> `_id` is converted to `id` in API responses.

**MongoDB Structure (ASCII)**

```
euron_coll
├─ _id: ObjectId
├─ name: string
├─ phone: int
├─ city: string
└─ course: string
```

---

## 🔄 CRUD Workflow (ASCII)

```
Client 💻
   |
FastAPI ⚡
   |
Endpoint Logic (Insert/Find/Update/Delete)
   |
MongoDB 🗄️ (euron_coll)
   |
Response JSON 📄
```

---

## ☁️ Deployment on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

**Steps:**

1. Push code to GitHub
2. Create a **Web Service** on Render
3. Connect repository
4. Set **Build Command**:

```bash
pip install -r requirements.txt
```

5. Set **Start Command**:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

6. Add Environment Variables:

```text
MONGODB_URI=<your-mongodb-uri>
DB_NAME=eurondb
```

---

## 💡 Tips & Best Practices

* Use `.env` for credentials 🌱
* Test locally before deploying 🔄
* Check **Swagger UI** for endpoint testing 🔍
* Follow CRUD order: GET → POST → PUT → PATCH → DELETE

---

## 👨‍💻 Author

<p align="center">
  <img src="https://avatars.githubusercontent.com/emkays-codelabs" width="140px" style="border-radius: 50%;" />
</p>

<h3 align="center">Emkay</h3>

<p align="center">
  <a href="https://github.com/emkays-codelabs">
    github.com/emkays-codelabs
  </a>
</p>
<p align="center">
  <img src="https://img.shields.io/github/followers/emkays-codelabs?label=Followers&style=flat&logo=github" />
  <img src="https://img.shields.io/github/stars/emkays-codelabs?label=Stars&style=flat&logo=github" />
</p>



<p align="center">
  😎 Follow me for clean code and cool projects<br/>
  ⭐ Star my repos to boost my coding superpowers 💪
</p>


<p align="center">
  <img src="https://img.shields.io/badge/Learn-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Code-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Build-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Improve-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Level up%20Together-purple?style=for-the-badge" />
</p>


<p align="center">
  <em>Stay curious. Keep coding.🔥
</em> 
</p>


---


