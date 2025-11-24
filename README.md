# 🎙️ Nirmaan AI Communication Coach


## 📖 Project Overview
This tool is an AI-powered assessment engine designed to analyze spoken communication skills. Built as part of the **Nirmaan AI Intern Case Study**, it processes student transcripts to generate a rubric-based score (0-100) and provides actionable feedback.

The system combines **Rule-based Logic**, **Natural Language Processing (NLP)**, and **Semantic Search** to evaluate students on five key dimensions defined in the official rubric.

---

## ⚙️ Tech Stack & Product Decisions
To ensure scalability, ease of use, and robust scoring, the following technical decisions were made:

| Component | Technology | Reasoning (Product Thinking) |
| :--- | :--- | :--- |
| **Frontend UI** | **Streamlit** | Chosen for its rapid development cycle and ability to handle Python-based data visualization natively without complex React/HTML boilerplate. |
| **Semantic Analysis** | **Sentence-Transformers** (`all-MiniLM-L6-v2`) | Used instead of simple keyword matching to understand *context*. It detects concepts like "Hobbies" even if the student says "I enjoy painting" (which a regex might miss). |
| **Grammar Engine** | **LanguageTool** | A rule-based grammar checker that is more reliable for specific error counting than generative LLMs, which can hallucinate errors. |
| **Sentiment Analysis** | **VADER** | Specifically tuned for social media and spoken text, making it ideal for detecting enthusiasm in self-introductions. |

---

## 📊 Scoring Logic (The Algorithm)

The application implements a weighted scoring system based on the provided Excel rubric:

### 1. Content & Structure (Weight: 40%)
* **Salutation:** Detects formal greetings (e.g., "Good Morning", "Hello Everyone").
* **Keyword Coverage:** Uses **Cosine Similarity** on sentence embeddings to match student speech against required topics (Name, Family, Hobbies, Ambition).
* **Flow:** Checks if the introduction follows a logical sequence.

### 2. Speech Rate (Weight: 10%)
* **Formula:** $\text{WPM} = (\text{Word Count} / \text{Duration in Seconds}) \times 60$
* **Scoring:**
    * **Ideal (111-140 WPM):** 10 Points
    * **Fast/Slow:** 6 Points
    * **Too Fast/Too Slow:** 2 Points

### 3. Language & Grammar (Weight: 20%)
* **Grammar:** Calculates error density per 100 words.
    * *Formula:* $1 - \min(\frac{\text{Errors per 100 words}}{10}, 1)$
* **Vocabulary (TTR):** Measures **Type-Token Ratio** (Unique Words / Total Words) to assess lexical diversity.

### 4. Clarity (Weight: 15%)
* **Filler Words:** Counts specific hesitations (`um`, `uh`, `like`, `you know`).
* **Penalty:** Higher percentage of filler words results in a lower score.

### 5. Engagement (Weight: 15%)
* **Sentiment Analysis:** Calculates a compound positivity score. High enthusiasm (>0.9 probability) is rewarded with full points.

---

## 💻 How to Run Locally

Follow these steps to deploy the application on your local machine.

### Prerequisites
* **Python 3.8+**
* **Java Runtime Environment (JRE)** (Required for the Grammar Checking server)

### Step 1: Clone the Repository
```bash
git clone [https://github.com/p-v-srinag/nirmaan-cs.git](https://github.com/p-v-srinag/nirmaan-cs.git)
cd nirmaan-cs
```
### Step 2: Set up Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Run the App
```bash
streamlit run app.py
```
The application will launch automatically in your browser at http://localhost:8501.

### Output
<img width="1658" height="812" alt="Screenshot 2025-11-24 at 10 57 34" src="https://github.com/user-attachments/assets/42876e1b-5cf3-4799-b168-26e162460fd7" />
<img width="435" height="792" alt="Screenshot 2025-11-24 at 10 58 34" src="https://github.com/user-attachments/assets/2d59cf32-1be1-458d-b1c7-c6566dbfd320" />


### Author
P. V. Srinag Submitted for Nirmaan AI Internship Case Study
