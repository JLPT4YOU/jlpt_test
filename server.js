require('dotenv').config();
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3001;

const examsDirectory = path.join(__dirname, 'exams');


// --- Security ---
const API_KEY = process.env.API_KEY;


const apiKeyAuth = (req, res, next) => {
  const apiKey = req.get('X-API-Key');
  if (apiKey && apiKey === API_KEY) {
    return next();
  } else {
    return res.status(401).json({ error: 'Unauthorized: Invalid or missing API key.' });
  }
};

// Apply the security middleware to all /exams routes
app.use('/exams', apiKeyAuth);


const skillDetails = {
  vocabulary: {
    id: 'vocabulary',
    name: 'Từ vựng',
    levels: {
      N1: [1, 2, 3, 4],
      N2: [1, 2, 3, 4],
      N3: [1, 2, 3],
      N4: [1, 2, 3],
      N5: [1, 2, 3],
    },
  },
  grammar: {
    id: 'grammar',
    name: 'Ngữ pháp',
    levels: {
      N1: [5, 6, 7],
      N2: [5, 6, 7],
      N3: [4, 5, 6, 7],
      N4: [4, 5, 6, 7],
      N5: [4, 5, 6, 7],
    },
  },
  reading: {
    id: 'reading',
    name: 'Đọc hiểu',
    levels: {
      N1: [8, 9, 10, 11, 12],
      N2: [8, 9, 10, 11],
      N3: [8, 9, 10],
      N4: [8, 9, 10],
      N5: [8, 9, 10],
    },
  },
  listening: {
    id: 'listening',
    name: 'Nghe hiểu',
    levels: {
      N1: [13, 14, 15],
      N2: [12, 13, 14],
      N3: [11, 12, 13, 14],
      N4: [11, 12, 13, 14],
      N5: [11, 12, 13, 14],
    },
  },
};
app.get('/', (req, res) => {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Exams API Documentation</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        h1, h2 { color: #2c3e50; }
        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        pre { background-color: #f4f4f4; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }
        li { margin-bottom: 10px; }
      </style>
    </head>
    <body>
      <h1>Exams API Documentation</h1>
      <p>Welcome to the JLPT Exams API. All API endpoints under <code>/exams</code> now require an API key.</p>
      <p>Please include the header <code>X-API-Key</code> with the value from your <code>.env</code> file in your requests.</p>

      <h2>Browsable Endpoints</h2>
      <p>You can browse the API structure step-by-step.</p>
      <ul>
        <li><code>GET /exams</code> - Lists available sources (official, custom).</li>
        <li><code>GET /exams/:source</code> - Lists available levels for a source.</li>
        <li><code>GET /exams/:source/:level</code> - Lists test types (jlpt_test, skills_test).</li>
        <li><code>GET /exams/:source/:level/jlpt_test</code> - Lists all test IDs for that level.</li>
        <li><code>GET /exams/:source/:level/skills_test</code> - Lists all available skills.</li>
        <li><code>GET /exams/:source/:level/skills_test/:skillId</code> - Lists all test IDs for a specific skill.</li>
      </ul>

      <h2>Specific Content Endpoints</h2>
      <ul>
        <li>
          <strong>Get Full Exam Content</strong><br>
          <code>GET /exams/:source/:level/jlpt_test/:id</code>
          <p>Returns the full content of a specific exam.</p>
          <p><strong>Parameters:</strong></p>
          <ul>
            <li><code>:source</code>: <code>official</code> or <code>custom</code></li>
            <li><code>:level</code>: e.g., <code>N1</code>, <code>N2</code></li>
            <li><code>:id</code>: The ID of the exam, e.g., <code>n1_2010_07</code></li>
          </ul>
          <p><strong>Example:</strong> <code>/exams/official/N1/jlpt_test/n1_2010_07</code></p>
        </li>
        <li>
          <strong>Get Filtered Exam by Skill</strong><br>
          <code>GET /exams/:source/:level/skills_test/:id/:skillId</code>
          <p>Returns specific sections of an exam that correspond to a particular skill.</p>
          <p><strong>Parameters:</strong></p>
          <ul>
            <li><code>:source</code>: <code>official</code> or <code>custom</code></li>
            <li><code>:level</code>: e.g., <code>N1</code>, <code>N2</code></li>
            <li><code>:skillId</code>: <code>vocabulary</code>, <code>grammar</code>, <code>reading</code>, or <code>listening</code></li>
            <li><code>:id</code>: The ID of the exam, e.g., <code>n1_2010_07</code></li>
          </ul>
          <p><strong>Example:</strong> <code>/exams/official/N1/skills_test/n1_2010_07/vocabulary</code></p>
        </li>
      </ul>
    </body>
    </html>
  `;
  res.send(html);
});

// --- Browsable Endpoints ---

// List sources
app.get('/exams', (req, res) => {
  res.json(['official', 'custom']);
});

// List levels for a source
app.get('/exams/:source', (req, res) => {
  fs.readdir(examsDirectory, { withFileTypes: true }, (err, files) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read exams directory' });
    }
    const levels = files
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);
    res.json(levels);
  });
});

// List test types for a level
app.get('/exams/:source/:level', (req, res) => {
    res.json(['jlpt_test', 'skills_test']);
});

// List all exam IDs for jlpt_test
app.get('/exams/:source/:level/jlpt_test', (req, res) => {
    const { source, level } = req.params;
    const directoryPath = path.join(examsDirectory, level, source);

    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            return res.status(404).json({ error: `Path not found for source '${source}' and level '${level}'.` });
        }
        const examIds = files
            .filter(file => file.endsWith('.json'))
            .map(file => path.basename(file, '.json'))
            .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));
        res.json(examIds);
    });
});

// List all skills for skills_test
app.get('/exams/:source/:level/skills_test', (req, res) => {
    res.json(Object.keys(skillDetails));
});

// List all exam IDs for a specific skill
app.get('/exams/:source/:level/skills_test/:skillId', (req, res) => {
    const { source, level, skillId } = req.params;

    if (!skillDetails[skillId]) {
        return res.status(404).json({ error: `Skill '${skillId}' not found.` });
    }

    const directoryPath = path.join(examsDirectory, level, source);

    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            return res.status(404).json({ error: `Path not found for source '${source}' and level '${level}'.` });
        }
        const examIds = files
            .filter(file => file.endsWith('.json'))
            .map(file => path.basename(file, '.json'))
            .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));
        res.json(examIds);
    });
});

// --- Specific Content Endpoints ---

// Get Full Exam Content
app.get('/exams/:source/:level/jlpt_test/:id', (req, res) => {
  const { source, level, id } = req.params;
  const filePath = path.join(examsDirectory, level, source, `${id}.json`);

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(404).json({ error: `Exam '${id}' not found in source '${source}' and level '${level}'.` });
    }
    try {
      const examData = JSON.parse(data);
      res.json(examData);
    } catch (parseErr) {
      res.status(500).json({ error: 'Failed to parse exam data.' });
    }
  });
});

// Get Filtered Exam by Skill
app.get('/exams/:source/:level/skills_test/:id/:skillId', (req, res) => {
  const { source, level, skillId, id } = req.params;

  const skillInfo = skillDetails[skillId];
  if (!skillInfo || !skillInfo.levels[level]) {
    return res.status(404).json({ error: `Skill '${skillId}' or level '${level}' is not valid.` });
  }
  const mondaisForSkill = skillInfo.levels[level];

  const filePath = path.join(examsDirectory, level, source, `${id}.json`);

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(404).json({ error: `Exam '${id}' not found in source '${source}' and level '${level}'.` });
    }
    try {
      const examData = JSON.parse(data);
      const filteredSections = examData.sections.filter(section =>
        mondaisForSkill.includes(section.mondai)
      );

      const result = {
        id: examData.id,
        title: examData.title,
        level: examData.level,
        skill: skillId,
        sections: filteredSections
      };
      res.json(result);
    } catch (parseErr) {
      res.status(500).json({ error: 'Failed to parse exam data.' });
    }
  });
});

app.listen(port, () => {
  console.log(`Exams API listening at http://localhost:${port}`);
});
