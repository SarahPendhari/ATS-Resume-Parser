import streamlit as st
import pymupdf  # For PDF extraction
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_bytes = uploaded_file.read()
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            st.error(f"Error: Unable to read the uploaded file. {str(e)}")
            return ""
    else:
        return ""  # Handle case where no file is uploaded

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def calculate_similarity_tfidf(resume, job_desc):
    vectorizer = TfidfVectorizer().fit_transform([resume, job_desc])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1] * 100  # Convert to percentage

def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and token.is_alpha and token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']]

def suggest_improvements(resume_text, job_description):
    resume_keywords = set(extract_keywords(resume_text.lower()))
    job_keywords = set(extract_keywords(job_description.lower()))
    
    missing_keywords = job_keywords - resume_keywords
    suggestions = []
    
    if missing_keywords:
        top_keywords = list(missing_keywords)[:5]  # Limit to 5 keywords
        suggestions.append("Consider incorporating the following keywords from the job description:")
        for keyword in top_keywords:
            suggestions.append(f"  - {keyword}")
        suggestions.append("Try to naturally integrate these keywords into your experience and skills sections.")
    
    return suggestions

def analyze_resume_structure(resume_text):
    score = 0
    feedback = []
    sections = {
        'contact information': 10,
        'summary' : 15,
        'education': 20,
        'experience': 30,
        'skills': 15,
        'achievements': 10
    }
    
    for section, points in sections.items():
        if section in resume_text.lower():
            score += points
        else:
            feedback.append(f"Missing '{section.capitalize()}' section. This section is important because:")
            if section == 'contact information':
                feedback.append("  - It allows employers to easily reach you.")
            elif section == 'summary':
                feedback.append("  - It provides a quick overview of your qualifications and career objectives.")
            elif section == 'education':
                feedback.append("  - It showcases your academic background and qualifications.")
            elif section == 'experience':
                feedback.append("  - It demonstrates your relevant work history and accomplishments.")
            elif section == 'skills':
                feedback.append("  - It highlights your key abilities and competencies.")
            elif section == 'achievements':
                feedback.append("  - It emphasizes your notable accomplishments and recognition.")
    
    return score, feedback

def analyze_certifications(resume_text):
    if "certification" in resume_text.lower() or "certified" in resume_text.lower():
        return 10, []
    else:
        return 0, ["Consider adding relevant certifications:", 
                   "  - Certifications demonstrate specialized knowledge and skills.",
                   "  - They can set you apart from other candidates.",
                   "  - Look for industry-specific certifications that align with the job requirements."]

def analyze_grammar(resume_text):
    doc = nlp(resume_text)
    grammar_issues = []
    
    for sent in doc.sents:
        if len(sent) > 40:  # Check for overly long sentences
            grammar_issues.append(f"Consider breaking up this long sentence: '{sent}'")
    
    if grammar_issues:
        return 5, ["Grammar and readability could be improved:"] + grammar_issues[:3]  # Limit to 3 examples
    else:
        return 10, []

def ats_resume_checker(resume_text, job_description):
    resume_cleaned = preprocess_text(resume_text)
    job_desc_cleaned = preprocess_text(job_description)

    # Calculate similarity score
    similarity_score = calculate_similarity_tfidf(resume_cleaned, job_desc_cleaned)

    # Analyze structure
    structure_score, structure_feedback = analyze_resume_structure(resume_text)

    # Analyze certifications
    certification_score, certification_feedback = analyze_certifications(resume_text)

    # Analyze grammar
    grammar_score, grammar_feedback = analyze_grammar(resume_text)

    # Suggest improvements based on keywords
    keyword_suggestions = suggest_improvements(resume_text, job_description)

    # Final score calculation
    final_score = structure_score + certification_score + grammar_score

    all_feedback = structure_feedback + certification_feedback + grammar_feedback + keyword_suggestions

    return similarity_score, final_score, all_feedback

# Streamlit app
st.title("ATS Resume Checker")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Enter Job Description")

if st.button("Analyze Resume"):
    if uploaded_file and job_description:
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            similarity_score, final_score, feedback = ats_resume_checker(resume_text, job_description)

            st.write(f"Matching Score: {similarity_score:.2f}%")
            st.write(f"Final Resume Score: {final_score}/100")

            if feedback:
                st.write("Detailed suggestions to improve your resume:")
                for suggestion in feedback:
                    st.write(suggestion)
            else:
                st.write("Your resume matches well with the job description!")
        else:
            st.error("Unable to read the uploaded file. Please check the file and try again.")
    else:
        st.warning("Please upload a resume and enter a job description.")