# WHOIS Tool 🌐

> A modern WHOIS lookup tool with an intuitive web interface, powered by FastAPI and React.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Latest-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 About

**WHOIS Tool** is a high-performance web application for performing WHOIS lookups on domain names. The tool combines the power of an asynchronous FastAPI backend with a modern and reactive React interface.

### 🎯 Key Features

- 🔍 **Instant WHOIS Lookup**: Retrieve complete domain information in real-time
- 📊 **Detailed Information**: Registrar, WHOIS servers, creation/expiration dates, status, DNS, emails
- ⚡ **Optimal Performance**: Asynchronous backend with caching for ultra-fast responses
- 🎨 **Modern Interface**: Intuitive and responsive UI built with React
- 🔄 **REST API**: Automatically documented FastAPI backend (Swagger/OpenAPI)

---

## 🚀 Installation

### Prerequisites

- **Python 3.7+** ([Download](https://www.python.org/downloads/))
- **Node.js 14+** and npm ([Download](https://nodejs.org/))

### 1️⃣ Backend Setup

```bash
# Navigate to the backend folder
cd backend

# Install Python dependencies
pip install fastapi uvicorn[standard] python-whois pydantic

# Start the FastAPI server
start.bat
# Or on Linux/Mac: uvicorn main:app --reload
```

The backend will be accessible at **http://localhost:8000**  
📚 API Documentation: **http://localhost:8000/docs**

### 2️⃣ Frontend Setup

```bash
# Navigate to the frontend folder
cd frontend

# Install Node.js dependencies
npm install

# Start the React application
npm start
```

The web interface will be accessible at **http://localhost:3000**

---

## 💻 Usage

1. Open your browser at **http://localhost:3000**
2. Enter a domain name (e.g., `example.com`)
3. Click **Search**
4. WHOIS information displays instantly

### Example Result

<img src="/img/image.png">

---

## 🛠️ REST API

The backend exposes a complete REST API:

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API home page |
| `GET` | `/whois/{domain}` | WHOIS lookup for a domain |
| `GET` | `/docs` | Interactive Swagger documentation |

### Usage Example

```bash
# With curl
curl http://localhost:8000/whois/example.com

# With httpie
http GET http://localhost:8000/whois/example.com
```

---

## 🧰 Technologies Used

### Backend
- **FastAPI**: High-performance asynchronous web framework
- **python-whois**: WHOIS query library
- **Pydantic**: Data validation and serialization
- **Uvicorn**: Lightning-fast ASGI server

### Frontend
- **React**: JavaScript library for user interfaces
- **Axios**: HTTP client for API calls
- **CSS3**: Modern and responsive styling

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it.

---

## 🙏 Acknowledgments

- Powered by [python-whois](https://pypi.org/project/python-whois/)
- Backend with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend with [React](https://reactjs.org/)

---

## 💬 Contact & Contribution

Created with ❤️ by **ch4tbl4nc**

---

<div align="center">

**Thank you for using WHOIS Tool!** 🚀

</div>