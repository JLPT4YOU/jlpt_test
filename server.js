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


// Updated part classification system based on MONDAI_PART_MAPPING.md
const skillDetails = {
  vocabulary: {
    id: 'vocabulary',
    name: 'Từ vựng',
    levels: {
      N1: [1, 2, 3, 4, 5],  // Mondai 1-5
      N2: [1, 2, 3, 4, 5],  // Mondai 1-5
      N3: [1, 2, 3, 4, 5],  // Mondai 1-5
      N4: [1, 2, 3, 4, 5],  // Mondai 1-5
      N5: [1, 2, 3, 4],     // Mondai 1-4
    },
  },
  grammar: {
    id: 'grammar',
    name: 'Ngữ pháp',
    levels: {
      N1: [6, 7, 8],        // Mondai 6-8
      N2: [6, 7, 8],        // Mondai 6-8
      N3: [6, 7, 8],        // Mondai 6-8
      N4: [6, 7, 8],        // Mondai 6-8
      N5: [5, 6, 7],        // Mondai 5-7
    },
  },
  reading: {
    id: 'reading',
    name: 'Đọc hiểu',
    levels: {
      N1: [9, 10, 11, 12, 13],    // Mondai 9-13
      N2: [9, 10, 11, 12, 13],    // Mondai 9-13
      N3: [9, 10, 11, 12],        // Mondai 9-12
      N4: [9, 10, 11],            // Mondai 9-11
      N5: [8, 9, 10],             // Mondai 8-10
    },
  },
  listening: {
    id: 'listening',
    name: 'Nghe hiểu',
    levels: {
      N1: [14, 15, 16, 17, 18],       // Mondai 14-18
      N2: [14, 15, 16, 17, 18, 19],   // Mondai 14-19 (some exams have 19)
      N3: [13, 14, 15, 16, 17],       // Mondai 13-17
      N4: [12, 13, 14, 15],           // Mondai 12-15
      N5: [11, 12, 13, 14],           // Mondai 11-14
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
        <li><code>GET /exams/:source/:level</code> - Lists test types (jlpt_test).</li>
        <li>
          <code>GET /exams/:source/:level/jlpt_test</code> - Lists all tests for that level (each item includes <code>id</code> and <code>title</code>).
          <br/>Supports pagination: <code>?page=&limit=</code>. Defaults: <code>page=1</code>, <code>limit=10</code> when any is provided.
          <br/><em>Examples:</em>
          <br/><code>/exams/official/N1/jlpt_test?page=1&limit=10</code>
          <br/><code>/exams/official/N1/jlpt_test?page=2&limit=10</code>
        </li>
      </ul>

      <h2>Specific Content Endpoints</h2>
      <ul>
        <li>
          <strong>Get Full or Filtered Exam Content</strong><br>
          <code>GET /exams/:source/:level/jlpt_test/:id</code>
          <p>Returns the full exam by default. Add <code>?skills=...</code> to get only certain skills.</p>
          <p><strong>Parameters:</strong></p>
          <ul>
            <li><code>:source</code>: <code>official</code> or <code>custom</code></li>
            <li><code>:level</code>: e.g., <code>N1</code>, <code>N2</code></li>
            <li><code>:id</code>: The ID of the exam, e.g., <code>n1_2010_07</code></li>
            <li><code>skills</code> (optional query): Comma-separated list of skill IDs: <code>vocabulary</code>, <code>grammar</code>, <code>reading</code>, <code>listening</code>.</li>
          </ul>
          <p><strong>Examples:</strong></p>
          <ul>
            <li>Full: <code>/exams/official/N1/jlpt_test/n1_2010_07</code></li>
            <li>1 skill: <code>/exams/official/N1/jlpt_test/n1_2010_07?skills=vocabulary</code></li>
            <li>2 skills: <code>/exams/official/N1/jlpt_test/n1_2010_07?skills=vocabulary,grammar</code></li>
            <li>3 skills: <code>/exams/official/N1/jlpt_test/n1_2010_07?skills=vocabulary,grammar,reading</code></li>
            <li>All 4 skills or no <code>skills</code> param = full exam.</li>
          </ul>
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
    res.json(['jlpt_test']);
});

// List exams (id and title) for jlpt_test (supports pagination with ?page=&limit=)
app.get('/exams/:source/:level/jlpt_test', async (req, res) => {
    const { source, level } = req.params;
    const { page, limit } = req.query;
    const directoryPath = path.join(examsDirectory, level, source);

    try {
        const files = await fs.promises.readdir(directoryPath);
        const examIds = files
            .filter(file => file.endsWith('.json'))
            .map(file => path.basename(file, '.json'))
            .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));

        const readTitles = async (ids) => {
            const entries = await Promise.all(ids.map(async (id) => {
                const filePath = path.join(directoryPath, `${id}.json`);
                try {
                    const data = await fs.promises.readFile(filePath, 'utf8');
                    const parsed = JSON.parse(data);
                    return { id, title: parsed.title || null };
                } catch (e) {
                    return { id, title: null };
                }
            }));
            return entries;
        };

        // If page or limit is provided, return paginated result with items (id,title)
        if (typeof page !== 'undefined' || typeof limit !== 'undefined') {
            const p = Math.max(parseInt(page || '1', 10) || 1, 1);
            const l = Math.max(parseInt(limit || '10', 10) || 10, 1);
            const totalItems = examIds.length;
            const totalPages = Math.max(Math.ceil(totalItems / l), 1);
            const currentPage = Math.min(p, totalPages);
            const start = (currentPage - 1) * l;
            const end = start + l;
            const pageIds = examIds.slice(start, end);
            const items = await readTitles(pageIds);

            return res.json({
                items,
                page: currentPage,
                limit: l,
                totalItems,
                totalPages,
                hasPrev: currentPage > 1,
                hasNext: currentPage < totalPages
            });
        }

        // No pagination: return full list of {id, title}
        const items = await readTitles(examIds);
        return res.json(items);
    } catch (err) {
        return res.status(404).json({ error: `Path not found for source '${source}' and level '${level}'.` });
    }
});



// --- Specific Content Endpoints ---

// Get Full or Filtered Exam Content (preferred endpoint)
app.get('/exams/:source/:level/jlpt_test/:id', (req, res) => {
  const { source, level, id } = req.params;
  const { skills } = req.query;
  const filePath = path.join(examsDirectory, level, source, `${id}.json`);

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(404).json({ error: `Exam '${id}' not found in source '${source}' and level '${level}'.` });
    }
    try {
      const examData = JSON.parse(data);

      // If no skills specified, return full exam
      if (!skills) {
        return res.json(examData);
      }

      // Parse and validate requested skills
      const requestedSkills = skills
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);

      // If all listed skills cover all available skills, return full exam
      const allSkills = Object.keys(skillDetails);
      const uniqueRequested = [...new Set(requestedSkills)];
      const coversAll = uniqueRequested.length === allSkills.length && uniqueRequested.every(s => allSkills.includes(s));
      if (coversAll) {
        return res.json(examData);
      }

      // Filter sections based on the 'part' field directly (preferred method)
      // This uses the actual part classification from the exam data
      const filteredSections = examData.sections.filter(section => {
        return uniqueRequested.includes(section.part);
      });

      // Fallback: if no sections match by part, try mondai-based filtering
      // (for backward compatibility or edge cases)
      if (filteredSections.length === 0) {
        let mondaisForSkills = [];
        for (const skillId of uniqueRequested) {
          const info = skillDetails[skillId];
          if (info && info.levels[level]) {
            mondaisForSkills.push(...info.levels[level]);
          }
        }
        
        if (mondaisForSkills.length > 0) {
          mondaisForSkills = [...new Set(mondaisForSkills)];
          const fallbackSections = examData.sections.filter(section =>
            mondaisForSkills.includes(section.mondai)
          );
          
          if (fallbackSections.length > 0) {
            filteredSections.push(...fallbackSections);
          }
        }
      }

      // No valid sections found
      if (filteredSections.length === 0) {
        return res.status(404).json({ error: `No sections found for skills '${uniqueRequested.join(', ')}' in level '${level}'.` });
      }

      const result = {
        id: examData.id,
        title: examData.title,
        level: examData.level,
        skills: uniqueRequested,
        sections: filteredSections,
      };

      return res.json(result);
    } catch (parseErr) {
      return res.status(500).json({ error: 'Failed to parse exam data.' });
    }
  });
});



app.listen(port, () => {
  console.log(`Exams API listening at http://localhost:${port}`);
});
