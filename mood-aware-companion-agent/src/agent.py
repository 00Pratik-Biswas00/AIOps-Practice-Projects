import os
import random
import google.genai as genai # Use the new google.genai SDK
from ddgs import DDGS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Predefined default recommendations
DEFAULT_RECOMMENDATIONS = {
    "music": [
        {"title": "Lofi Study Beats", "artist": "Various", "genre": "Lofi Hip Hop"},
        {"title": "Peaceful Piano", "artist": "Various", "genre": "Classical/Relaxation"},
        {"title": "Upbeat Pop Hits", "artist": "Various", "genre": "Pop"},
        {"title": "Jazz for Focus", "artist": "Various", "genre": "Jazz"},
        {"title": "Electronic Chillout", "artist": "Various", "genre": "Electronic"},
    ],
    "movies": [
        {"title": "The Intouchables", "genre": "Comedy-drama"},
        {"title": "Spirited Away", "genre": "Animation"},
    ]
}

# --- Gemini API Setup ---
# The google.genai library automatically picks up GEMINI_API_KEY from environment variables.
# No explicit genai.configure() call is needed if the environment variable is set.

def _get_gemini_recommendations(prompt):
    """Generates recommendations using the Gemini API."""
    # Check if API key is available before proceeding with Gemini call
    if not os.getenv("GEMINI_API_KEY"):
        print("Gemini API key not found in environment variables. Skipping Gemini recommendations.")
        return None
    try:
        client = genai.Client() # Initialize the client
        response = client.models.generate_content( # Use client.models.generate_content
            model='gemini-2.0-flash', # Specify the model
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None

def get_recommendations(activity, mood, language):
    """
    Returns music and movie recommendations using Gemini API, with fallback to DuckDuckGo search,
    and then to default recommendations.
    """
    recommendations = {"music": [], "movies": []}
    
    # --- 1. Try Gemini API first ---
    print("Attempting to get recommendations from Gemini API.")
    with open("agent_instructions.txt", "r") as f:
        instructions = f.read()

    gemini_prompt = (
        f"{instructions}\n\n"
        f"Based on the above, please provide music recommendations for someone who is "
        f"**{activity}** and feeling **{mood}**. The recommendations should be in the "
        f"**{language}** language or from that region.\n\n"
        "Please provide 5 music recommendations in the format: 'Song Title - Artist Name'.\n"
    )
    if activity.lower() == "relaxing":
        gemini_prompt += "\nAlso, please provide 2 movie recommendations in the format: 'Movie Title'."
    
    gemini_response = _get_gemini_recommendations(gemini_prompt)
    if gemini_response:
        music_count = 0
        movie_count = 0
        lines = gemini_response.strip().split('\n')
        for line in lines:
            if ' - ' in line and music_count < 5: # Limit to 5 music recommendations
                parts = line.split(' - ', 1)
                recommendations["music"].append({"title": parts[0].strip(), "artist": parts[1].strip(), "genre": "Categorized by Gemini"})
                music_count += 1
            # Simple check for movie titles (assuming they don't have ' - ')
            elif activity.lower() == "relaxing" and not ' - ' in line and line.strip() and movie_count < 2: # Limit to 2 movie recommendations
                 recommendations["movies"].append({"title": line.strip(), "genre": "Categorized by Gemini"})
                 movie_count += 1
        
        if recommendations["music"] or recommendations["movies"]:
            return recommendations

    # --- 2. Fallback to DuckDuckGo Search ---
    print("Gemini API failed or returned no results. Trying DuckDuckGo Search.")
    try:
        # --- Music search (DDGS) ---
        music_queries = [
            f"{language} {mood} songs for {activity} spotify",
            f"{language} {mood} songs for {activity} youtube",
            f"popular {language} {mood} songs"
        ]
        
        for m_query in music_queries:
            with DDGS() as ddgs:
                music_results_ddgs = list(ddgs.text(m_query, max_results=5))

            if music_results_ddgs:
                for result in music_results_ddgs:
                    title_full = result.get('title', '').replace(' - Topic', '').strip()
                    snippet = result.get('body', '').strip() # Use snippet for additional filtering

                    # Aggressive filtering for irrelevant results
                    irrelevant_keywords = ["playlist", "mix", "album", "top ", "best of", "how to", "guide", "article"]
                    if any(keyword in title_full.lower() for keyword in irrelevant_keywords) or \
                       any(keyword in snippet.lower() for keyword in irrelevant_keywords):
                        continue

                    # Attempt to extract cleaner title and artist
                    title = ""
                    artist = "Unknown Artist"

                    # Pattern: "Song Title - Artist" or "Artist - Song Title"
                    if ' - ' in title_full:
                        parts = title_full.split(' - ', 1)
                        if len(parts[0].split()) < len(parts[1].split()): # Heuristic: shorter part is often title
                             title = parts[0].strip()
                             artist = parts[1].strip()
                        else:
                             title = parts[1].strip()
                             artist = parts[0].strip()
                    elif ' by ' in title_full: # Pattern: "Song Title by Artist"
                        parts = title_full.split(' by ', 1)
                        title = parts[0].strip()
                        artist = parts[1].strip()
                    else: # Fallback to full title if no clear pattern
                        title = title_full
                        # Try to find artist in snippet
                        if "artist:" in snippet.lower():
                            artist = snippet.lower().split("artist:", 1)[1].split(',')[0].strip()
                        elif "by " in snippet.lower():
                            artist = snippet.lower().split("by ", 1)[1].split(',')[0].strip()
                    
                    # Basic validation for title and artist
                    if len(title) > 3 and "unknown" not in artist.lower(): # Avoid too short or unparseable titles
                        recommendations["music"].append({
                            "title": title, 
                            "artist": artist, 
                            "genre": "Unknown (via DDGS)"
                        })
                if len(recommendations["music"]) >= 5: # Stop if enough music found
                    break
        
        # --- Movie search (DDGS) ---
        if activity.lower() == "relaxing":
            movie_queries = [
                f"{language} {mood} movies IMDB",
                f"best {language} {mood} films"
            ]
            for m_query in movie_queries:
                with DDGS() as ddgs:
                    movie_results_ddgs = list(ddgs.text(m_query, max_results=2))
                if movie_results_ddgs:
                    for result in movie_results_ddgs:
                        title_full = result.get('title', '').strip()
                        # Simple heuristic: remove year from title if present
                        title_clean = title_full.split(' (')[0].strip()
                        
                        # Filter out non-movie results
                        irrelevant_movie_keywords = ["list of", "tv series", "show", "documentary"]
                        if any(keyword in title_clean.lower() for keyword in irrelevant_movie_keywords):
                            continue

                        recommendations["movies"].append({"title": title_clean, "genre": "Unknown (via DDGS)"})
                    if len(recommendations["movies"]) >= 2: # Stop if enough movies found
                        break


        # If we got results from DDGS, return them
        if recommendations["music"] or recommendations["movies"]:
            return recommendations

    except Exception as e:
        print(f"An error occurred during DuckDuckGo search: {e}")
        
    # --- 3. Final Fallback to Default Recommendations ---
    print("DuckDuckGo search failed or returned no results. Using default recommendations.")
    recommendations["music"] = random.sample(DEFAULT_RECOMMENDATIONS["music"], min(5, len(DEFAULT_RECOMMENDATIONS["music"])))
    if activity.lower() == "relaxing":
        recommendations["movies"] = random.sample(DEFAULT_RECOMMENDATIONS["movies"], min(2, len(DEFAULT_RECOMMENDATIONS["movies"])))
        
    return recommendations

