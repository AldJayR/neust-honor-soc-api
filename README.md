# Honor Society API Documentation

A comprehensive REST API for managing honor society operations, built with Django REST Framework.

## 🚀 Getting Started

### Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

### Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```javascript
Authorization: Bearer <your-access-token>
```

## 📋 Table of Contents

- [Authentication](#authentication)
- [Campus Management](#campus-management)
- [Department Management](#department-management)
- [Course Management](#course-management)
- [Student Management](#student-management)
- [GWA Records](#gwa-records)
- [Honor Society Officers](#honor-society-officers)
- [Error Handling](#error-handling)
- [React/Next.js Examples](#reactnextjs-examples)

---

## 🔐 Authentication

### Register Officer
Register a new honor society officer (requires admin verification).

```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securePassword123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "position": "Secretary",
  "campus_id": 1
}
```

**Response (201 Created):**
```json
{
  "message": "Officer registered successfully. Please wait for admin verification before you can login.",
  "user": {
    "id": 2,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "officer": {
    "id": 2,
    "position": "Deputy Secretary",
    "is_active": true,
    "is_verified": false,
    "campus": {
      "id": 1,
      "name": "Sumacab Campus",
      "code": "SUM"
    }
  }
}
```

### Login
Authenticate and receive JWT tokens.

```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "yourPassword"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "member": {
    "id": 1,
    "position": "System Administrator",
    "is_active": true,
    "is_verified": true,
    "campus": {
      "id": 1,
      "name": "Sumacab Campus",
      "code": "SUM"
    }
  }
}
```

### User Profile
Get current user's profile information.

```http
GET /api/auth/profile/
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "member": {
    "id": 1,
    "position": "System Administrator",
    "is_active": true,
    "is_verified": true,
    "campus": {
      "id": 1,
      "name": "Sumacab Campus",
      "code": "SUM"
    }
  }
}
```

### Token Refresh
Refresh your access token using the refresh token.

```http
POST /api/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "your-refresh-token"
}
```

**Response (200 OK):**
```json
{
  "access": "new-access-token"
}
```

---

## 🏫 Campus Management

### List Campuses
Get a paginated list of all campuses.

```http
GET /api/campuses/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `search`: Search by name or code
- `ordering`: Order by field (name, code, -name, -code)
- `page`: Page number

**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Sumacab Campus",
      "code": "SUM"
    },
    {
      "id": 2,
      "name": "General Tinio Campus",
      "code": "GTC"
    }
  ]
}
```

### Create Campus
Create a new campus.

```http
POST /api/campuses/
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "General Tinio Campus",
  "code": "GTC"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "General Tinio Campus",
  "code": "GTC"
}
```

### Get Campus
Get a specific campus by ID.

```http
GET /api/campuses/{id}/
Authorization: Bearer <access-token>
```

### Update Campus
Update a campus.

```http
PUT /api/campuses/{id}/
Authorization: Bearer <access-token>
```

### Delete Campus
Delete a campus.

```http
DELETE /api/campuses/{id}/
Authorization: Bearer <access-token>
```

---

## 🏢 Department Management

### List Departments
Get a paginated list of departments (colleges/faculties).

```http
GET /api/departments/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `campus`: Filter by campus ID
- `search`: Search by name, code, or campus name
- `ordering`: Order by field

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "College of Information and Communications Technology",
      "code": "CICT",
      "campus": {
        "id": 1,
        "name": "Sumacab Campus",
        "code": "SUM"
      }
    }
  ]
}
```

### Create Department
Create a new department (college/faculty).

```http
POST /api/departments/
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "College of Engineering",
  "code": "CoE",
  "campus_id": 1
}
```

---

## 📚 Course Management

### List Courses
Get a paginated list of courses (degree programs).

```http
GET /api/courses/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `department`: Filter by department ID (college/faculty)
- `search`: Search by name, code, or department name

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Bachelor of Science in Information Technology",
      "code": "BSIT",
      "department": {
        "id": 1,
        "name": "College of Information and Communications Technology",
        "code": "CICT",
        "campus": {
          "id": 1,
          "name": "Sumacab Campus",
          "code": "SUM"
        }
      }
    },
    {
      "id": 2,
      "name": "Bachelor of Science in Data Science",
      "code": "BSDS",
      "department": {
        "id": 1,
        "name": "College of Information and Communications Technology",
        "code": "CICT",
        "campus": {
          "id": 1,
          "name": "Sumacab Campus",
          "code": "SUM"
        }
      }
    }
  ]
}
```

---

## 👨‍🎓 Student Management

### List Students
Get a paginated list of students.

```http
GET /api/students/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `campus`: Filter by campus ID
- `department`: Filter by department ID (college/faculty)
- `year_level`: Filter by year level (1, 2, 3, 4)
- `search`: Search by student number, name, campus, or department

**Response (200 OK):**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "student_number": "2024-001",
      "first_name": "Jane",
      "last_name": "Smith",
      "year_level": 2,
      "campus": {
        "id": 1,
        "name": "Sumacab Campus",
        "code": "SUM"
      },
      "department": {
        "id": 1,
        "name": "College of Information and Communications Technology",
        "code": "CICT",
        "campus": {
          "id": 1,
          "name": "Sumacab Campus",
          "code": "SUM"
        }
      }
    }
  ]
}
```

### Create Student
Create a new student.

```http
POST /api/students/
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "student_number": "2024-002",
  "first_name": "John",
  "last_name": "Doe",
  "year_level": 1,
  "campus_id": 1,
  "department_id": 1
}
```

---

## 📊 GWA Records

### List GWA Records
Get a paginated list of GWA records.

```http
GET /api/gwa-records/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `student`: Filter by student ID
- `semester`: Filter by semester
- `academic_year`: Filter by academic year
- `min_gwa`: Filter by minimum GWA
- `max_gwa`: Filter by maximum GWA
- `search`: Search by student info, semester, or academic year

**Response (200 OK):**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "semester": "1st Semester",
      "academic_year": "2024-2025",
      "gwa": "1.50",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "encoded_by": "admin",
      "student": {
        "id": 1,
        "student_number": "2024-001",
        "first_name": "Jane",
        "last_name": "Smith",
        "year_level": 2,      "campus": {
        "id": 1,
        "name": "Sumacab Campus",
        "code": "SUM"
      },
        "department": {
          "id": 1,
          "name": "College of Information and Communications Technology",
          "code": "CICT",
          "campus": {
            "id": 1,
            "name": "Sumacab Campus",
            "code": "SUM"
          }
        }
      }
    }
  ]
}
```

### Create GWA Record
Create a new GWA record.

```http
POST /api/gwa-records/
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "student_id": 1,
  "semester": "2nd Semester",
  "academic_year": "2024-2025",
  "gwa": 1.75
}
```

### Honor Eligible Students
Get students eligible for honor society (GWA ≤ 1.75).

```http
GET /api/gwa-records/honor_eligible/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `min_gwa`: Minimum GWA threshold (default: 1.75)
- `academic_year`: Filter by academic year

### GWA Statistics
Get statistical data about GWAs.

```http
GET /api/gwa-records/statistics/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `academic_year`: Filter by academic year

**Response (200 OK):**
```json
{
  "total_records": 150,
  "average_gwa": 2.25,
  "highest_gwa": 1.00,
  "lowest_gwa": 5.00,
  "honor_eligible": 45
}
```

---

## 👥 Honor Society Officers

### List Officers
Get a paginated list of honor society officers.

```http
GET /api/officers/
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `campus`: Filter by campus ID
- `is_active`: Filter by active status (true/false)
- `search`: Search by username, name, position, or campus

---

## ❌ Error Handling

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format

```json
{
  "error": "Description of the error",
  "detail": "More specific error details (optional)"
}
```

### Authentication Errors

```json
{
  "error": "Your account is pending admin verification."
}
```

```json
{
  "error": "User is not an active officer."
}
```

---

## ⚛️ React/Next.js Integration

### Basic Fetch Setup

```javascript
// Set up your base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Include JWT token in requests
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('access_token');
  
  return fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
    ...options,
  });
};
```

### Authentication Example

```javascript
// Login
const login = async (username, password) => {
  const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }
};

// Register
const register = async (userData) => {
  const response = await apiRequest('/api/auth/register/', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
  return response.json();
};
```

---

## 🔧 Environment Variables

Create a `.env.local` file in your Next.js project:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
DJANGO_API_URL=http://localhost:8000
```

---

## 📝 Notes for Frontend Developers

1. **Authentication Flow**: Users must register → wait for admin verification → login
2. **Token Management**: Store tokens securely, implement auto-refresh
3. **Error Handling**: Always handle 401/403 responses appropriately
4. **Pagination**: All list endpoints return paginated results
5. **Search & Filtering**: Most endpoints support search and filtering parameters
6. **CORS**: Configure CORS settings in Django for your frontend domain

---

## 🆘 Support

For questions about API usage or integration issues, please:
1. Check this documentation first
2. Review the API response formats
3. Test endpoints using tools like Postman or curl
4. Contact the backend development team

Happy coding! 🚀
