🎙️ Nirmaan AI Communication Coach

A smart AI-powered tool designed to analyze and score students' spoken communication skills based on a structured rubric. This project was built as part of the Nirmaan AI Intern Case Study.

🚀 Overview

This application takes a text transcript of a student's self-introduction and analyzes it across five key dimensions:

Content & Structure: Uses Semantic Search (NLP) to find key topics (Name, Family, Hobbies) even if phrased differently.

Speech Rate: Calculates Words Per Minute (WPM) to check pacing.

Language & Grammar: Checks for grammatical errors and vocabulary richness (TTR).

Clarity: Detects filler words (um, uh, like) to measure fluency.

Engagement: Uses Sentiment Analysis to detect positive tone and confidence.

🛠️ Tech Stack & Product Decisions

Component

Tool Used

Why this choice?

Frontend

Streamlit

Allows for rapid prototyping and interactive UI in pure Python.

Semantic Matching

Sentence-Transformers

Captures meaning rather than just keywords (e.g., "I like painting" matches "Hobbies").

Grammar

Language-Tool-Python

A robust wrapper for the standard LanguageTool API/Server.

Sentiment

VADER

Optimized for social/spoken text to detect enthusiasm.

Backend

Python

The standard for AI/NLP development.

💻 Installation & Setup

Follow these steps to run the project locally on your machine.

Prerequisites

Python 3.8 or higher

Java (Required for the local Grammar Checking server)

1. Clone the Repository

git clone [https://github.com/p-v-srinag/nirmaan-cs.git](https://github.com/p-v-srinag/nirmaan-cs.git)
cd nirmaan-cs


2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt


4. Run the Application

streamlit run app.py


The app will open in your browser at http://localhost:8501.

📊 Scoring Logic (The "Brain")

The scoring engine (scorer.py) implements the Nirmaan Rubric rigorously:

Content (40%): * Salutation: Checks for specific greetings.

Keywords: Uses all-MiniLM-L6-v2 embeddings to compare student sentences against rubric topics (Score threshold > 0.35).

Speech Rate (10%): (Word Count / Duration) * 60. Ideal range: 111-140 WPM.

Language (20%): Penalizes grammar errors per 100 words and rewards high Type-Token Ratio (Vocabulary diversity).

Clarity (15%): Penalizes high frequency of filler words.

Engagement (15%): Rewards high positive sentiment probability.

👤 Author

P. V. Srinag Built for Nirmaan AI Internship Case Study