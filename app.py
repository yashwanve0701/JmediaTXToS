import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os

# Convert text to speech (Text-to-Speech)
def text_to_speech(text, tts_file):
    tts = gTTS(text=text, lang='en')
    tts.save(tts_file)
    return tts_file

# Match characteristics of recorded voice
def match_voice_characteristics(tts_file, recorded_voice_file, output_file):
    # Load the TTS and recorded voice audio files
    tts_audio = AudioSegment.from_file(tts_file)
    recorded_voice_audio = AudioSegment.from_file(recorded_voice_file)

    # Match volume level
    tts_audio = tts_audio.apply_gain(recorded_voice_audio.dBFS - tts_audio.dBFS)

    # Export the modified TTS audio
    tts_audio.export(output_file, format="mp3")
    return output_file

# Simple chatbot logic
def chatbot_response(user_input):
    greetings = ["hello", "hi", "hey"]
    info = ["tell me about yourself", "who are you"]
    worr = ["what do you do"]
    songg = ["what song have you sung", "tell me about your songs"]
    by = ["bye", "goodbye"]

    responses = {
        "hello": "Hey, Hi! How are you?",
        "me": "I'm Aria Harmony. I am a singer.",
        "work": "I have created several songs. I like to sing pop music.",
        "song": "I sang Chuffed Up, Crown Jewel, Dream Lover and many more songs in my singing career.",
        "bye": "Goodbye! Have a great day!"
    }

    user_input_lower = user_input.lower()

    if any(greet in user_input_lower for greet in greetings):
        return responses["hello"]
    elif any(phrase in user_input_lower for phrase in info):
        return responses["me"]
    elif any(phrase in user_input_lower for phrase in worr):
        return responses["work"]
    elif any(phrase in user_input_lower for phrase in songg):
        return responses["song"]
    elif any(phrase in user_input_lower for phrase in by):
        return responses["bye"]
    else:
        return "That sounds great."

# Streamlit web app
def main():
    st.title("Aria Harmony")

    # Step 1: Input text for chatbot
    user_input = st.text_input("You:", "Hello")

    if st.button("Send"):
        # Get chatbot response
        response_text = chatbot_response(user_input)

        # Display chatbot response text
        st.text_area("Aria Harmony:", response_text, height=100)

        tts_file = "tts_output.mp3"
        output_file = "final_output.mp3"
        recorded_voice_file = "Why me Why now.wav"  # Replace with your recorded voice file path

        # Convert chatbot response to speech
        tts_path = text_to_speech(response_text, tts_file)

        # Match characteristics of recorded voice
        matched_path = match_voice_characteristics(tts_file, recorded_voice_file, output_file)

        # Automatically play the audio file
        audio_bytes = open(matched_path, 'rb').read()
        st.audio(audio_bytes, format='audio/mp3')

if __name__ == "__main__":
    main()