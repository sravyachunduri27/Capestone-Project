from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Initialize the SentenceTransformer model globally
print("Loading SentenceTransformer model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("Model loaded successfully.")

# Global variable to store encoded events
encoded_event_embeddings = None
events_df = None  # To store the loaded events DataFrame for later use

def initialize_event_embeddings(events_csv):
    """
    Preloads and encodes the event descriptions from a CSV file.
    
    Parameters:
    events_csv (str): Path to the event listings CSV file.

    Returns:
    None: The function updates the global `encoded_event_embeddings` and `events_df`.
    """
    global encoded_event_embeddings, events_df

    # Load event listings
    try:
        events_df = pd.read_csv(events_csv)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file: {events_csv}")
    except Exception as e:
        raise Exception(f"Error loading the CSV file: {str(e)}")

    # Encode event descriptions
    print("Encoding event descriptions...")
    encoded_event_embeddings = model.encode(events_df['description'].tolist(), convert_to_tensor=True)
    print("Event descriptions encoding complete and stored globally.")


def get_event_recommendations_sentence_transformer(resume_text):
    """
    Generates event recommendations based on cosine similarity of Sentence-BERT embeddings.

    Parameters:
    resume_text (list of str): A list of skills or relevant text from the resume.

    Returns:
    list of dict: A list of event recommendations sorted by match score, each containing:
                  id, posting_url, event_name, match_score.
    """
    global encoded_event_embeddings, events_df

    # Check if event embeddings have been initialized
    if encoded_event_embeddings is None or events_df is None:
        raise ValueError("Event embeddings are not initialized. Call `initialize_event_embeddings` first.")

    # Encode the resume text
    print("Encoding resume text...")
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    print("Resume encoding complete.")

    # Calculate cosine similarity between the resume and each event description
    print("Calculating cosine similarity...")
    cosine_scores = util.cos_sim(resume_embedding, encoded_event_embeddings)
    #similarities = util.pytorch_cos_sim(resume_embedding, encoded_event_embeddings)
    #top_event_indices = torch.topk(similarities, k=25)[1].tolist()[0]

    # Prepare a list for event recommendations
    event_recommendations = []

    # Iterate through each event and calculate match scores
    for idx, event_row in events_df.iterrows():
        match_score = cosine_scores[0][idx].item()  # Extract the cosine similarity score

        if match_score > 0.25:  # Threshold for considering a good match
            event_recommendations.append({
                'Event ID': int(event_row['id']),  # Convert to native Python int
                'Event Name': str(event_row['Name']),  # Convert to string
                'Match Score': float(match_score * 100),  # Convert to native Python float and scale to percentage
                'Registration URL': event_row['url'] if not pd.isna(event_row['url']) else '',
                'Event URL': event_row['Event URL'] if not pd.isna(event_row['Event URL']) else ''
            })

    # Sort recommendations by match score in descending order
    sorted_recommendations = sorted(event_recommendations, key=lambda x: x['Match Score'], reverse=True)

    print("Event recommendations generated successfully.")
    return sorted_recommendations

    
