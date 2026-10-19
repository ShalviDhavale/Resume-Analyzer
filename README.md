# CareerAI — Smart Resume Analyzer & Career Guide

CareerAI is a responsive PHP application for students exploring their next career step. It compares resume evidence with a selected job description, highlights skill gaps, recommends adjacent roles, and can produce a personalized improvement report with Google Gemini.

## Features

- Responsive landing page and dashboard with resume upload or paste input.
- Server-side PDF MIME/signature and 5 MB checks with text extraction through local Python 3.10 and `pypdf`.
- Predefined editable job descriptions and custom descriptions.
- Gemini structured JSON analysis, with evidence-aware profile extraction and estimated match score.
- Clearly labelled keyword comparison fallback when Gemini is not configured or unavailable.
- Skill gap filters, chart, career recommendations, and checkable learning roadmap.
- AI improvement report, text report download, and browser print / Save as PDF.
- Temporary PHP session storage; uploaded PDF remains in PHP's temporary upload location and is not copied into the public uploads directory.

## Stack

PHP 8.1+, HTML, CSS, vanilla JavaScript, Google Gemini REST API, Python `pypdf`, Chart.js, and jsPDF. Chart.js, jsPDF, and Google Fonts load from public CDNs; an internet connection is needed for those assets. No database is required.

## Requirements

- XAMPP with PHP 8.1 or newer, Apache, and the PHP `curl`, `fileinfo`, and `mbstring` extensions enabled.
- Python 3.10 at `C:\Users\dhava\AppData\Local\Programs\Python\Python310\python.exe`, with `pypdf` installed for that interpreter.
- A Google AI Studio Gemini API key for AI analysis and report generation. The keyword fallback works without a key.

## Setup in XAMPP

1. Place this folder at `C:\xampp\htdocs\ResumeAnalyzer`.
2. Confirm pypdf is installed for the configured interpreter:

   ```powershell
   & "C:\Users\dhava\AppData\Local\Programs\Python\Python310\python.exe" -m pip show pypdf
   ```

3. Ensure the project-root `.env` contains your Gemini configuration. Keep it private and never commit it. `GEMINI_MODEL` defaults to `gemini-3.6-flash`; change it if that model is not enabled for your key.
4. In XAMPP Control Panel, start Apache.
5. Open `http://localhost/ResumeAnalyzer/`.

You can also run PHP's built-in development server from the project folder using `php -S localhost:8000` and open `http://localhost:8000`.

## Gemini configuration

The API key is read by PHP from the process environment or the root `.env` file. It is sent in the server-side `x-goog-api-key` request header and is never embedded in browser code. The application calls Google's `generateContent` REST API and requests JSON output. Resume text and the job description are sent to Google only when the user submits an analysis; report generation sends them again as context. Tell users before submitting if using this with another person's resume.

If no key is present or Gemini errors, CareerAI returns a clearly labelled keyword comparison. The fallback does not claim to be AI, does not infer education or experience, and does not generate a personalized report. Set a valid key to enable all AI features.

## PDF extraction

PDF parsing uses the Python `extract_pdf.py` helper and the installed `pypdf` package. PHP passes the temporary upload path to Python as a separate process argument (without a shell command), reads a JSON response, and enforces a timeout. The app validates size, MIME type, and PDF signature, and does not retain the uploaded file. Text-based PDFs are supported; scanned image-only files require OCR and are reported as containing no selectable text. Pasted resume text remains available without Python PDF extraction.

## Privacy and security notes

- Configure Apache/PHP with current security updates and avoid exposing `.env` through a misconfigured server.
- The `.gitignore` excludes `.env` and Composer's `vendor` directory.
- The Gemini API key remains server-side. Resume text and job description are sent to Google's API when AI is enabled.
- Analysis is kept in the PHP session to support report generation and is not stored in MySQL. Session files are written under `storage/sessions` and Apache access is denied for that folder. Clear the browser session to remove it sooner; set a suitable PHP session lifetime on shared machines.
- This practical project has no login or per-user isolation beyond PHP sessions. Do not host it publicly without adding authentication, CSRF protection, rate limiting, and privacy review.
- Rendered user and model text is inserted into the page as escaped text. External resource links are only rendered for HTTPS URLs.

## Troubleshooting

- **PDF support is unavailable:** confirm the configured Python executable exists and run `& "C:\Users\dhava\AppData\Local\Programs\Python\Python310\python.exe" -m pip show pypdf`; alternatively paste resume text.
- **Gemini fallback appears:** confirm `.env` is in the project root, `GEMINI_API_KEY` is valid, PHP cURL is enabled, the configured model is available to the key, and outbound HTTPS is allowed.
- **Could not read PDF:** use a text-based PDF (not an image-only scan), or paste its text. OCR is not included.
- **Chart is missing:** allow the Chart.js CDN (`cdn.jsdelivr.net`) or check the browser network panel.
- **Blank or server error:** review Apache's PHP error log and ensure PHP 8.1+, `mbstring`, `fileinfo`, and `curl` are enabled.

## Project structure

```text
ResumeAnalyzer/
├── index.php
├── extract_pdf.py
├── api/
│   ├── common.php
│   ├── analyze_resume.php
│   └── generate_report.php
├── assets/
│   ├── css/style.css
│   └── js/app.js
├── storage/sessions/.htaccess
├── uploads/.gitkeep
├── reports/.gitkeep
├── composer.json
├── .env.example
├── .htaccess
├── .gitignore
└── README.md
```

## Practical limitations

This version uses sessions rather than permanent history or a database. PDF text extraction does not include OCR. The report can be downloaded as PDF through jsPDF or printed / saved as PDF from the browser. Online model availability and API quotas depend on the Gemini account.
