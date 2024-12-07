import PyPDF2
import resume_scoring as scoring
import spacy
import nltk
import resume_parser
import jobs_recommendation as jr
import events_recommendations as er

# Ensure NLTK resources are available
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

# Function to fetch resume text from a PDF
def fetch_resume(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        if not text:
            raise ValueError("No text extracted from PDF.")
        return text
    
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def parse_resume(resume_text):

    # Initialize details dictionary with all keys from the updated Resume model
    details = {
        
        'email': '',
        'skills': [],
        'degrees': [],
        'colleges': [],
        'majors':[],

        #'experience': [],
        'totalExperience':0,
        'companies':[],
        'designations': [],
        
        'achievements':[],
        'length': 0,
        'spellingMistakes': 0,
        'repeatedWords': {},
        'positiveBuzzwords': [],
        'negativeBuzzwords': [],
        'impactWords': {
            'action_words': [],
            'metrics': [],
            'weak_words': []
        },
        'bulletPoints': 0,
        'impactScore': 0,
        #'certifications': [],
        'sections':None,
        'projects': [],
        'summary': '',
        'objective': '',
        'jobs':[],
        'totalJobs':0,
        'events':[],
        'total_events':0
    }

    # Process resume text
    nlp_text = nlp(resume_text)
   

    # Extract details using various parser methods
    details['email'] = resume_parser.extract_email(resume_text)
    details['skills'] = resume_parser.extract_skills(resume_text)
    details['education'] = resume_parser.get_education_section(nlp_text)

    education_text = resume_parser.get_education_section(nlp_text)
    education = resume_parser.extract_education_details_single_dict(education_text)
    
    details['colleges'] = education['institution']
    details['degrees'] = education['degree']
    details['majors'] = education['major']

    experience_text = resume_parser.get_experience_section(nlp_text)
    experience = resume_parser.extract_experience_details(experience_text)

    #details['experience'] = resume_parser.get_experience_section(nlp_text)
    if experience:
        details['totalExperience'] = experience['total_experience_years']
    details['designations'] = experience['designations']
    details['companies'] = experience['companies']
    details['length'] = resume_parser.get_length(nlp_text)
    details['spellingMistakes'] = resume_parser.count_spelling_mistakes(nlp_text)
    details['repeatedWords'] = resume_parser.count_word_repetition(nlp_text)
    details['positiveBuzzwords'] = resume_parser.positive_buzzwords(resume_text)
    details['negativeBuzzwords'] = resume_parser.negative_buzzwords(resume_text)
    details['bulletPoints'] = resume_parser.count_bullet_points(resume_text)
    sections = resume_parser.extract_entity_sections(nlp_text)
    details['sections'] = sections
    details['projects'] = resume_parser.get_projects(sections['projects'])
    achievements = None
    if "Achievements" in sections:
        achievements = sections["Achievements"]
    details['achievements'] = resume_parser.count_bullet_points(achievements) if achievements else []
    details['scores'] = scoring.calculate_resume_score(resume_text)



    # Extract impact words and calculate impact score
    impact_words = resume_parser.extract_impact_words(resume_text)
    details['impactWords']['action_words'] = impact_words.get('action_words', [])
    details['impactWords']['metrics'] = impact_words.get('metrics', [])
    details['impactWords']['weak_words'] = impact_words.get('weak_words', [])
    details['impactScore'] = resume_parser.calculate_impact_score(details['impactWords'])

    # Placeholder for extracting certifications, projects, summary, objective, and accomplishments
    # Implement these in resume_parser if not done yet
    #details['certifications'] = resume_parser.extract_certifications(resume_text)  # List of certifications
    #details['projects'] = resume_parser.extract_projects(resume_text)              # List of projects
    #details['summary'] = resume_parser.extract_summary(resume_text)                # Summary section of resume
    #details['objective'] = resume_parser.extract_objective(resume_text)            # Objective section of resume
    #details['accomplishments'] = resume_parser.extract_accomplishments(resume_text) # Accomplishments section
    

    return details

def match_jobs_and_events(resume_text):
    """
    Matches jobs and events based on the resume text by using pre-initialized embeddings.

    Parameters:
    resume_text (list of str): A list of skills or relevant text from the resume.

    Returns:
    dict: A dictionary containing job recommendations, event recommendations, 
          and their respective counts.
    """
    details = {}

    # Ensure the job embeddings are pre-initialized
    if jr.encoded_job_embeddings is None or jr.job_listings_df is None:
        raise ValueError("Job embeddings are not initialized. Call `initialize_job_embeddings` first.")

    # Ensure the event embeddings are pre-initialized
    if er.encoded_event_embeddings is None or er.events_df is None:
        raise ValueError("Event embeddings are not initialized. Call `initialize_event_embeddings` first.")

    # Get job recommendations
    print("Fetching job recommendations...")
    details['jobs'] = jr.get_job_recommendations_sentence_transformer(resume_text)
    details['totalJobs'] = len(details['jobs'])

    # Get event recommendations
    print("Fetching event recommendations...")
    details['events'] = er.get_event_recommendations_sentence_transformer(resume_text)
    details['totalEvents'] = len(details['events'])

    return details

# Function to take a file as input and return parsed details
def extract_resume_details(pdf_file):
    resume_text = fetch_resume(pdf_file)
    return parse_resume(resume_text)

def extract_match_jobs_and_events(pdf_file):
    resume_text = fetch_resume(pdf_file)
    return match_jobs_and_events(resume_text)

