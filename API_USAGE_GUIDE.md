# 🎌 JLPT4YOU API Usage Guide

## 📊 Database Overview

Cơ sở dữ liệu chứa **2,023 đề thi JLPT** với tổng cộng **200,894 câu hỏi** được phân loại theo 4 kỹ năng chính:

| Level | Đề thi | Câu hỏi | Vocabulary | Grammar | Reading | Listening |
|-------|--------|---------|------------|---------|---------|-----------|
| **N1** | 201 | 21,480 | 7,035 (32.8%) | 2,821 (13.1%) | 4,399 (20.5%) | 7,225 (33.6%) |
| **N2** | 382 | 40,501 | 10,286 (25.4%) | 8,392 (20.7%) | 8,967 (22.1%) | 12,856 (31.7%) |
| **N3** | 551 | 55,971 | 19,281 (34.4%) | 12,663 (22.6%) | 8,837 (15.8%) | 15,190 (27.1%) |
| **N4** | 555 | 53,351 | 18,859 (35.3%) | 13,869 (26.0%) | 5,565 (10.4%) | 15,058 (28.2%) |
| **N5** | 334 | 29,591 | 11,728 (39.6%) | 8,344 (28.2%) | 2,180 (7.4%) | 7,339 (24.8%) |

## 🎯 API Endpoints

### 1. Lấy danh sách đề thi theo level và part

```javascript
// Lấy tất cả đề N3
GET /api/exams?level=3

// Lấy đề N3 có phần vocabulary
GET /api/exams?level=3&part=vocabulary

// Lấy đề N2 có phần listening
GET /api/exams?level=2&part=listening

// Lấy đề custom N4
GET /api/exams?level=4&type=custom
```

### 2. Lấy chi tiết một đề thi

```javascript
// Lấy đề thi cụ thể
GET /api/exams/jlpt4you_N3_1

// Response example:
{
  "id": "jlpt4you_N3_1",
  "title": "JLPT4YOU N3 (1)",
  "level": 3,
  "type": "custom",
  "duration": 139,
  "sections": [
    {
      "mondai": 1,
      "part": "vocabulary",
      "title": "Chuyển Kanji sang Hira",
      "questions": [...]
    }
  ],
  "statistics": {
    "total_questions": 102,
    "total_sections": 17,
    "by_part": {
      "vocabulary": 35,
      "grammar": 18,
      "reading": 21,
      "listening": 28
    }
  }
}
```

### 3. Lấy câu hỏi theo kỹ năng

```javascript
// Lấy chỉ phần vocabulary của đề N3
GET /api/exams/jlpt4you_N3_1/vocabulary

// Lấy chỉ phần listening của đề N2
GET /api/exams/jlpt4you_N2_1/listening

// Lấy câu hỏi của mondai cụ thể
GET /api/exams/jlpt4you_N3_1/mondai/1
```

## 🏗️ Cấu trúc dữ liệu

### Part Classification (Phân loại theo kỹ năng)

| Level | Vocabulary | Grammar | Reading | Listening |
|-------|------------|---------|---------|-----------|
| **N1** | Mondai 1-5 | Mondai 6-8 | Mondai 9-13 | Mondai 14-18 |
| **N2** | Mondai 1-5 | Mondai 6-8 | Mondai 9-13 | Mondai 14-19* |
| **N3** | Mondai 1-5 | Mondai 6-8 | Mondai 9-12 | Mondai 13-17 |
| **N4** | Mondai 1-5 | Mondai 6-8 | Mondai 9-11 | Mondai 12-15 |
| **N5** | Mondai 1-4 | Mondai 5-7 | Mondai 8-10 | Mondai 11-14 |

*Lưu ý: N2 có thể có 18 hoặc 19 mondai (Mondai 19 là listening bổ sung)

### Question Structure

```javascript
{
  "number": 1,
  "text": "Question text with <u>underlined</u> parts",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "answer": 0, // Index của đáp án đúng
  "passage": "Reading passage (nếu có)",
  "audioURL": "Link to audio file (cho listening)"
}
```

## 🔍 Tìm kiếm và lọc

### Query Parameters

- `level`: 1, 2, 3, 4, 5 (N1-N5)
- `part`: vocabulary, grammar, reading, listening
- `type`: custom, official
- `mondai`: 1-19 (tùy level)
- `limit`: Số lượng kết quả (default: 50)
- `offset`: Bỏ qua số kết quả (cho pagination)

### Examples

```javascript
// Lấy 10 đề N3 đầu tiên có phần vocabulary
GET /api/exams?level=3&part=vocabulary&limit=10

// Lấy đề official N1 từ vị trí 20
GET /api/exams?level=1&type=official&offset=20

// Tìm tất cả đề có mondai 15 (listening)
GET /api/exams?mondai=15
```

## 📈 Statistics API

```javascript
// Lấy thống kê tổng quan
GET /api/statistics

// Lấy thống kê theo level
GET /api/statistics/N3

// Response example:
{
  "total_exams": 551,
  "total_questions": 55971,
  "by_part": {
    "vocabulary": 19281,
    "grammar": 12663,
    "reading": 8837,
    "listening": 15190
  },
  "average_questions_per_exam": 101.6
}
```

## 🎮 Frontend Usage Examples

### React Hook

```javascript
import { useState, useEffect } from 'react';

const useJLPTExams = (level, part) => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchExams = async () => {
      const response = await fetch(`/api/exams?level=${level}&part=${part}`);
      const data = await response.json();
      setExams(data);
      setLoading(false);
    };
    
    fetchExams();
  }, [level, part]);

  return { exams, loading };
};
```

### Vue Composition API

```javascript
import { ref, onMounted } from 'vue';

export function useJLPTExams(level, part) {
  const exams = ref([]);
  const loading = ref(true);

  const fetchExams = async () => {
    try {
      const response = await fetch(`/api/exams?level=${level}&part=${part}`);
      exams.value = await response.json();
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchExams);
  
  return { exams, loading, fetchExams };
}
```

## 🛠️ Maintenance Scripts

### Update Parts Classification

```bash
# Cập nhật phân loại part cho tất cả file
python3 update_exam_parts.py

# Validate tất cả file
python3 validate_exams.py

# Tạo thống kê mới
python3 generate_statistics.py
```

## 📝 Notes

1. **Part Classification**: Tất cả đề thi đã được phân loại theo 4 kỹ năng chính
2. **Statistics**: Mỗi file có thống kê chi tiết về số câu hỏi theo part
3. **Validation**: 100% file đã được validate và đúng cấu trúc
4. **Audio Files**: Listening questions có link đến file audio
5. **Reading Passages**: Reading questions có đoạn văn kèm theo

## 🚀 Performance Tips

- Sử dụng pagination cho danh sách lớn
- Cache kết quả thống kê
- Load audio files lazy (khi cần)
- Sử dụng compression cho API responses
