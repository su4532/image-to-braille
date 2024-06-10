import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import io
import louis


def transcribe_text(image):
    base64_image = encode_image_to_base64(image)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that responds in Markdown. Please help me with my tasks!"},
            {"role": "user", "content": [
                {"type": "text", "text": "Please transcribe all the text in the image. After you are finished, convert this to Grade 2 UEB Braille and return the Braille translation."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                 }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def encode_image_to_base64(photo):
    buffered = io.BytesIO()
    photo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def text_to_braille(text):
    return louis.translateString(["braille-patterns.cti", "en-us-g2.ctb"], text)


def braille_to_text(braille):
    return louis.backTranslateString(["braille-patterns.cti", "en-us-g2.ctb"], braille)


client = OpenAI(api_key="sk-proj-lkykaHkX6lNZxxpd1viCT3BlbkFJ17cFSBytIyoXJ9o4Kihb")
MODEL = "gpt-4o"


st.title("Image Text Transcription App")
st.write("Upload a photo and get the transcribed text from the image.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("")
    st.write("Transcribing...")

    final_text = transcribe_text(image)

    st.write("Transcribed text:")
    st.write(final_text)

    braille_text = text_to_braille(final_text)

    st.write("Braille text:")
    st.write(braille_text)

# # Streamlit app
# st.title("Liblouis Test App")
# text_input = st.text_input("Enter text to convert to braille:")
# if text_input:
#   braille_output = text_to_braille(text_input)
#   st.write("Braille Output:", braille_output)