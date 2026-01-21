import streamlit as st
from agent import get_recommendations

def main():
    st.title("🎧 Mood-Aware Creative Companion Agent")

    # Get user input
    activity = st.selectbox("What are you doing?", ["Sketching", "Coding", "Relaxing", "Workout"])
    mood = st.selectbox("How do you feel?", ["Calm", "Low", "Energetic"])
    language = st.text_input("Enter preferred region or language", "English")

    if st.button("Get Recommendations"):
        recommendations = get_recommendations(activity, mood, language)

        st.subheader("🎧 Here are your recommendations:")

        st.write("### 🎵 Music")
        for music in recommendations["music"]:
            st.write(f"**{music['title']}** by {music['artist']} ({music['genre']})")

        if recommendations["movies"]:
            st.write("### 🎬 Movies")
            for movie in recommendations["movies"]:
                st.write(f"**{movie['title']}** ({movie['genre']})")
        # st.json(recommendations)
if __name__ == "__main__":
    main()
