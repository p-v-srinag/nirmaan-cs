import re
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import word_tokenize

# --- FIX FOR NLTK ERROR ---
# We download both 'punkt' and 'punkt_tab' to ensure compatibility with all NLTK versions
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading necessary NLTK data...")
    nltk.download('punkt')
    nltk.download('punkt_tab')

class RubricScorer:
    def __init__(self):
        print("Loading models... (this may take a moment)")
        
        # --- GRAMMAR CHECKER (LOCAL JAVA SERVER) ---
        try:
            self.grammar_tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"CRITICAL ERROR: Java not found. Please install Java. Details: {e}")
            raise e
            
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Rubric Constants
        self.FILLER_WORDS = {'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah'}
        self.SALUTATIONS_GOOD = ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]
        self.SALUTATIONS_NORMAL = ["hi", "hello"]

    def analyze_transcript(self, text, duration_sec):
        """
        Main function to calculate all scores based on Nirmaan Rubric.
        """
        # Tokenize (This is where the error happened previously)
        words = word_tokenize(text)
        total_words = len(words)
        if total_words == 0: return {"error": "Empty transcript"}

        # --- 1. CONTENT & STRUCTURE (Weight: 40%) ---
        lower_text = text.lower()
        salutation_score = 0
        if any(s in lower_text[:50] for s in self.SALUTATIONS_GOOD):
            salutation_score = 4 
        elif any(s in lower_text[:50] for s in self.SALUTATIONS_NORMAL):
            salutation_score = 2
        
        # Keywords (Semantic Search)
        keywords_must = ["Name", "Age", "School class", "Family", "Hobbies interest"]
        keywords_good = ["Family details", "Origin", "Ambition goal", "Unique fact", "Achievements"]
        
        sentences = nltk.sent_tokenize(text)
        embeddings_text = self.semantic_model.encode(sentences, convert_to_tensor=True)
        
        def check_coverage(topics, threshold=0.35):
            score_accum = 0
            found_list = []
            embeddings_topics = self.semantic_model.encode(topics, convert_to_tensor=True)
            cosine_scores = util.cos_sim(embeddings_topics, embeddings_text)
            
            for i, topic in enumerate(topics):
                max_val = float(cosine_scores[i].max()) 
                if max_val > threshold:
                    score_accum += 1
                    found_list.append(topic)
            return score_accum, found_list

        count_must, found_must = check_coverage(keywords_must)
        count_good, found_good = check_coverage(keywords_good)
        
        kw_score = min(20, count_must * 4) + min(10, count_good * 2)
        flow_score = 5 if salutation_score > 0 else 0 

        content_raw = salutation_score + kw_score + flow_score
        content_weighted = (min(content_raw, 35) / 35) * 40

        # --- 2. SPEECH RATE (Weight: 10%) ---
        wpm = (total_words / duration_sec) * 60 if duration_sec > 0 else 0
        rate_score_raw = 0
        if 111 <= wpm <= 140: rate_score_raw = 10
        elif 141 <= wpm <= 160: rate_score_raw = 6
        elif 81 <= wpm <= 110: rate_score_raw = 6
        else: rate_score_raw = 2
        
        speech_weighted = rate_score_raw 

        # --- 3. LANGUAGE & GRAMMAR (Weight: 20%) ---
        # Grammar
        matches = self.grammar_tool.check(text)
        error_count = len(matches)
        errors_per_100 = (error_count / total_words) * 100
        grammar_raw = (1 - min(errors_per_100 / 10, 1)) * 10 
        
        # Vocabulary (TTR)
        unique_words = len(set([w.lower() for w in words]))
        ttr = unique_words / total_words
        vocab_raw = 0
        if ttr >= 0.9: vocab_raw = 10
        elif 0.7 <= ttr < 0.9: vocab_raw = 8
        elif 0.5 <= ttr < 0.7: vocab_raw = 6
        elif 0.3 <= ttr < 0.5: vocab_raw = 4
        else: vocab_raw = 2
        
        lang_weighted = ((grammar_raw + vocab_raw) / 20) * 20

        # --- 4. CLARITY (Filler Words) (Weight: 15%) ---
        filler_count = sum(1 for w in words if w.lower() in self.FILLER_WORDS)
        filler_rate = (filler_count / total_words) * 100
        clarity_raw = 0
        if 0 <= filler_rate <= 3: clarity_raw = 15
        elif 4 <= filler_rate <= 6: clarity_raw = 12
        elif 7 <= filler_rate <= 9: clarity_raw = 9
        elif 10 <= filler_rate <= 12: clarity_raw = 6
        else: clarity_raw = 3
        
        clarity_weighted = clarity_raw 

        # --- 5. ENGAGEMENT (Sentiment) (Weight: 15%) ---
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        # Using Compound score normalized to 0-1 scale for robustness
        score_metric = (sentiment['compound'] + 1) / 2 
        
        engage_raw = 0
        if score_metric >= 0.9: engage_raw = 15
        elif 0.7 <= score_metric < 0.9: engage_raw = 12
        elif 0.5 <= score_metric < 0.7: engage_raw = 9
        elif 0.3 <= score_metric < 0.5: engage_raw = 6
        else: engage_raw = 3
        
        engage_weighted = engage_raw

        # --- FINAL SCORE ---
        total_score = content_weighted + speech_weighted + lang_weighted + clarity_weighted + engage_weighted

        return {
            "overall_score": round(total_score, 1),
            "details": {
                "Content & Structure": {"score": round(content_weighted, 1), "feedback": f"Keywords: {len(found_must)} mandatory, {len(found_good)} optional."},
                "Speech Rate": {"score": round(speech_weighted, 1), "feedback": f"{round(wpm)} WPM"},
                "Language": {"score": round(lang_weighted, 1), "feedback": f"TTR: {round(ttr, 2)}, Grammar Errors: {error_count}"},
                "Clarity": {"score": round(clarity_weighted, 1), "feedback": f"Filler Rate: {round(filler_rate, 1)}%"},
                "Engagement": {"score": round(engage_weighted, 1), "feedback": f"Positivity: {round(score_metric, 2)}"}
            }
        }