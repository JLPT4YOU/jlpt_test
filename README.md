# 🎌 JLPT4YOU Exam API

> **🆕 Major Update (Oct 2025)**: Cơ sở dữ liệu đã được cập nhật với **2,023 đề thi** và **200,894 câu hỏi** được phân loại theo 4 kỹ năng chính!

A comprehensive RESTful API server for JLPT (Japanese Language Proficiency Test) exam questions with advanced part classification system.

## ✨ Features

- **🎯 Complete JLPT Database**: 2,023 đề thi across all levels (N1-N5)
- **📊 Smart Classification**: Questions classified by skills (vocabulary, grammar, reading, listening)
- **🔍 Advanced Filtering**: Filter by level, part, type, mondai, and more
- **📈 Built-in Statistics**: Detailed analytics for each exam and level
- **🚀 High Performance**: Optimized for fast data retrieval
- **🌐 CORS Enabled**: Ready for frontend integration

## 📊 Database Overview

| Level | Exams | Questions | Vocabulary | Grammar | Reading | Listening |
|-------|-------|-----------|------------|---------|---------|-----------|
| **N1** | 201 | 21,480 | 7,035 (32.8%) | 2,821 (13.1%) | 4,399 (20.5%) | 7,225 (33.6%) |
| **N2** | 382 | 40,501 | 10,286 (25.4%) | 8,392 (20.7%) | 8,967 (22.1%) | 12,856 (31.7%) |
| **N3** | 551 | 55,971 | 19,281 (34.4%) | 12,663 (22.6%) | 8,837 (15.8%) | 15,190 (27.1%) |
| **N4** | 555 | 53,351 | 18,859 (35.3%) | 13,869 (26.0%) | 5,565 (10.4%) | 15,058 (28.2%) |
| **N5** | 334 | 29,591 | 11,728 (39.6%) | 8,344 (28.2%) | 2,180 (7.4%) | 7,339 (24.8%) |

## Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher recommended)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)

## 🚀 Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/jlpt4you-api.git
    cd jlpt4you-api
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the server:**
    ```bash
    npm start
    # or for development
    npm run dev
    ```

The API will be available at `http://localhost:3001`

## 🎯 API Endpoints

### Basic Usage

```javascript
// Get all N3 exams
GET /api/exams?level=3

// Get N3 vocabulary questions only
GET /api/exams?level=3&part=vocabulary

// Get specific exam
GET /api/exams/jlpt4you_N3_1

// Get statistics
GET /api/statistics
```

### Advanced Filtering

| Parameter | Values | Description |
|-----------|--------|-------------|
| `level` | 1,2,3,4,5 | JLPT level (N1-N5) |
| `part` | vocabulary, grammar, reading, listening | Skill type |
| `type` | custom, official | Exam source |
| `mondai` | 1-19 | Specific mondai number |
| `limit` | 1-100 | Results per page |
| `offset` | 0+ | Skip results (pagination) |

### Examples

```bash
# Lấy 10 đề N2 listening đầu tiên
curl "http://localhost:3001/api/exams?level=2&part=listening&limit=10"

# Lấy đề official N1
curl "http://localhost:3001/api/exams?level=1&type=official"

# Lấy thống kê N3
curl "http://localhost:3001/api/statistics/N3"
```

## 🏗️ Part Classification System

### Mondai Mapping

| Level | Vocabulary | Grammar | Reading | Listening |
|-------|------------|---------|---------|-----------|
| **N1** | Mondai 1-5 | Mondai 6-8 | Mondai 9-13 | Mondai 14-18 |
| **N2** | Mondai 1-5 | Mondai 6-8 | Mondai 9-13 | Mondai 14-19* |
| **N3** | Mondai 1-5 | Mondai 6-8 | Mondai 9-12 | Mondai 13-17 |
| **N4** | Mondai 1-5 | Mondai 6-8 | Mondai 9-11 | Mondai 12-15 |
| **N5** | Mondai 1-4 | Mondai 5-7 | Mondai 8-10 | Mondai 11-14 |

*N2 có thể có 18 hoặc 19 mondai (Mondai 19 là listening bổ sung)

## 📚 Documentation

- **[API Usage Guide](API_USAGE_GUIDE.md)** - Comprehensive API documentation
- **[Mondai Part Mapping](MONDAI_PART_MAPPING.md)** - Detailed part classification system
- **[Statistics](exam_statistics.json)** - Generated database statistics

## 🛠️ Maintenance Scripts

```bash
# Update all exam files with correct part classification
python3 update_exam_parts.py

# Validate all exam files
python3 validate_exams.py

# Generate fresh statistics
python3 generate_statistics.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Run validation scripts
5. Submit a pull request

## 📄 License

This project is for educational purposes. JLPT is a trademark of the Japan Foundation and Japan Educational Exchanges and Services.

---

**🎯 Built for JLPT learners worldwide**

