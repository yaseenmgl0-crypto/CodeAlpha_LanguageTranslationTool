import streamlit as st
import requests

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Chinese": "zh-CN",
    "Turkish": "tr",
    "Persian": "fa",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko"
}

st.title("🌐 AI Language Translation Tool")
st.write("Translate text easily between different languages.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys())
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1
    )

text = st.text_area(
    "Enter Your Text",
    placeholder="Write your text here...",
    height=180
)

if st.button("Translate", type="primary", use_container_width=True):

    if not text.strip():
        st.warning("Please enter text first.")

    elif source == target:
        st.warning("Please select two different languages.")

    else:
        try:
            with st.spinner("Translating..."):

                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text,
                        "langpair": (
                            f"{LANGUAGES[source]}|"
                            f"{LANGUAGES[target]}"
                        )
                    },
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

                if data.get("responseStatus") == 200:
                    result = data["responseData"]["translatedText"]

                    st.subheader("Translation Result")
                    st.success(result)

                    st.download_button(
                        "Download Translation",
                        data=result,
                        file_name="translation.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(
                        data.get(
                            "responseDetails",
                            "Translation failed. Try again."
                        )
                    )

        except requests.RequestException:
            st.error(
                "Internet connection or translation service error."
            )

st.divider()

st.caption("Developed for CodeAlpha AI Internship.")
