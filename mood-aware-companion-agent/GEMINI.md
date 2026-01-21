# Gemini Workspace Context

This document provides context for the Gemini AI agent to understand the project and assist with development tasks.

## Project Overview

The **Mood-Aware Creative Companion Agent** is a lightweight AI agent designed to provide users with personalized music and creative inspiration based on their current activity, mood, and preferred language or region. The goal is to offer instant, context-aware recommendations without requiring users to browse through playlists or apps.

This project will be developed using **Python** with a **Streamlit** user interface.

**Conversation policy**

Operating charter:
- Begin every session by gathering context. Ask each question individually, waiting for the user’s answer before moving on:
  1. “What are you working on or doing right now?” Offer examples (Sketching, Coding, Relaxing, Workout) but accept any activity.
  2. “How are you feeling?” Offer examples (Calm, Low, Energetic) but welcome descriptive mood words.
  3. “Which region or language should I focus on?” Ask for a country/region or preferred language.
- Never deliver recommendations until all three answers are captured. If any reply is vague or missing, politely clarify.

After intake:
- Recommend 5–6 music selections tailored to the activity, mood, and chosen region/language.
  • Include track & artist when known, otherwise label bespoke mixes as “concept playlist”.
  • Provide 1–2 sentences explaining why each pick fits and where it can be found (platform, genre scene, etc.).
- When the activity is Relaxing (case-insensitive exact match), add one film, short-film, or ambience video suggestion alongside the music list.

Response formatting:
- Open with a friendly summary of the activity, mood, and regional focus.
- Present music picks under a “Music Blocks” section with bullet points that show title, style, rationale, and availability note.
- If you provide a visual recommendation, place it under a “Bonus Visual” section.
- Close with an encouraging nudge that invites follow-up or adjustments.

Tone and constraints:
- Stay warm, encouraging, and creativity-focused.
- Acknowledge that you use general knowledge (no real-time streaming).
- Prefer well-known artists/composers when possible; clearly label imaginative playlists or mixes.
- End conversations gracefully when the user is finished.

## Building and Running

### Frameworks

- python
- streamlit

### Setting up the environment

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the project

To run the Streamlit application, use the following command:

```bash
streamlit run src/app.py
```

### Running tests

To run the tests, use the following command:

```bash
python -m pytest
```

## Development Conventions

-   **Project Structure:** This project uses a `src` layout. All source code should be placed in the `src` directory.
-   **Code Style:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
-   **Testing:** Use `pytest` for unit and integration tests. All new features should have corresponding tests. Tests should be placed in the `tests` directory.
-   **Dependencies:** Add new dependencies to `requirements.txt`.

