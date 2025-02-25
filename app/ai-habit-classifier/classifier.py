# classifier.py
import spacy
from transformers import pipeline

def get_spacy_model(lang: str):
    """Return the appropriate spaCy model for the given language."""
    if lang.lower() == "de":
        return spacy.load("de_core_news_sm")
    else:
        return spacy.load("en_core_web_sm")

def segment_and_classify(sentence: str, lang: str = "en"):
    """
    Segments a habit sentence into candidate phrases and classifies each phrase into one of:
      - Time
      - Prior Behavior
      - Inner State
      - People
      - Location
      - Habit
      - Other

    The method uses dependency heuristics (e.g. prepositional phrases and adverbial clauses)
    to generate candidate phrases, then uses a zero-shot classifier to label each phrase.
    """
    nlp = get_spacy_model(lang)
    doc = nlp(sentence)
    
    # Gather candidate phrases based on dependency cues.
    parts = []
    used_tokens = set()
    
    # Collect prepositional phrases and adverbial clauses.
    for token in doc:
        if token.dep_ in ["prep", "advcl"]:
            span = doc[token.left_edge.i : token.right_edge.i + 1]
            phrase = span.text.strip()
            if phrase and any(ch.isalpha() for ch in phrase):
                parts.append({"phrase": phrase, "start": span.start, "end": span.end})
                used_tokens.update(range(span.start, span.end))
    
    # Gather remaining tokens as the main clause.
    remaining = [token for i, token in enumerate(doc) if i not in used_tokens]
    if remaining:
        span = doc[remaining[0].i : remaining[-1].i + 1]
        phrase = span.text.strip()
        if phrase:
            parts.append({"phrase": phrase, "start": span.start, "end": span.end})
    
    # Initialize the zero-shot classifier.
    classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
    candidate_labels = ["Time", "Prior Behavior", "Inner State", "People", "Location", "Habit", "Other"]
    
    classified_parts = []
    for part in parts:
        result = classifier(part["phrase"], candidate_labels=candidate_labels)
        domain = result["labels"][0]  # Select the top predicted label.
        classified_parts.append({"phrase": part["phrase"], "domain": domain})
    
    return classified_parts

# Quick test when running directly.
if __name__ == "__main__":
    test_sentence_en = "In the morning after I wake up I go to the bathroom and brush my teeth."
    test_sentence_de = "Am Morgen nachdem ich aufgewacht bin gehe ich ins Badezimmer und putze meine Zähne."
    
    print("English segmentation and classification:")
    for part in segment_and_classify(test_sentence_en, "en"):
        print(f"  [{part['domain']}] {part['phrase']}")
        
    print("\nGerman segmentation and classification:")
    for part in segment_and_classify(test_sentence_de, "de"):
        print(f"  [{part['domain']}] {part['phrase']}")