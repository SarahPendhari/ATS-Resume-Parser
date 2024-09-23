# ATS Resume Checker

## Description

The ATS Resume Checker is a Streamlit application designed to analyze resumes and provide feedback on how well they align with a given job description. Utilizing Natural Language Processing (NLP) techniques, this tool extracts key information from resumes and evaluates their structure, grammar, and keyword usage, helping users enhance their chances of passing through Applicant Tracking Systems (ATS).

## Features

- **PDF Resume Upload**: Users can upload their resumes in PDF format for analysis.
- **Job Description Input**: Enter the job description to compare against the resume.
- **Similarity Scoring**: Calculates a matching score between the resume and the job description.
- **Detailed Feedback**: Provides insights on resume structure, certifications, grammar, and keyword suggestions.
- **User-friendly Interface**: Easy to use with a clean layout.

## Technologies Used

- Streamlit: For the web application interface.
- PyMuPDF: For extracting text from PDF files.
- spaCy: For Natural Language Processing tasks.
- scikit-learn: For calculating similarity scores using TF-IDF.

## Installation

To run the ATS Resume Checker locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ats-resume-checker.git
   cd ats-resume-checker 
2.Create a virtual environment and activate it (optional but recommended):
```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
```
3.Install the required packages:
```bash
pip install -r requirements.txt
```
4.Run the Streamlit application:
```bash
streamlit run app.py
```

Open your web browser and go to the provided local URL (usually http://localhost:8501).

## Usage
Upload your resume in PDF format.
Enter the job description you want to match against.
Click the "Analyze Resume" button to receive feedback.
Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Special thanks to the creators of Streamlit, PyMuPDF, spaCy, and scikit-learn for their invaluable libraries that made this project possible.

### Instructions

1. Replace `https://github.com/yourusername/ats-resume-checker.git` with the actual URL of your GitHub repository.
2. Add any additional sections or information that you think are relevant.

Feel free to ask if you need further assistance!
