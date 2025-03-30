import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from io import BytesIO
from docx import Document

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Groq
client = Groq()

# Interface utilisateur avec Streamlit
st.set_page_config(page_title="Transcription Audio | RostaingAI", layout="centered")
st.title("🎙️Transcription Audio: RostaingAI")

st.write("Enregistrez un message vocal ou téléversez un fichier audio, et nous le transcrirons en texte.")

# Option de téléchargement ou prise de photo
tab1, tab2 = st.tabs(["📂 Télécharger ", "🎤 Enregistrer"])

with tab1:
    uploaded_file = st.file_uploader("Téléversez un fichier audio", type=["mp3", "wav", "m4a"]) 

with tab2:
    audio_file = st.audio_input("Enregistrez votre message vocal")

file_path = None

if audio_file is not None:
    file_path = "temp_audio.m4a"
    with open(file_path, "wb") as f:
        f.write(audio_file.read())

elif uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

if file_path:
    # Transcription avec Groq
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            response_format="text",
            temperature=0.0
        )
    
    # Affichage du résultat
    st.subheader("📝 Transcription :")
    st.write(transcription)
    
    # Sauvegarde en fichier texte
    txt_filename = "transcription.txt"
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(transcription)
    st.download_button("📥 Télécharger en TXT", data=open(txt_filename, "rb").read(), file_name=txt_filename, mime="text/plain")
    
    # Sauvegarde en fichier Word
    doc = Document()
    doc.add_paragraph(transcription)
    doc_bytes = BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    st.download_button("📥 Télécharger en DOCX", data=doc_bytes.getvalue(), file_name="transcription.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    # Suppression du fichier temporaire
    os.remove(file_path)
    os.remove(txt_filename)