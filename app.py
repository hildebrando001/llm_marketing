# Import required libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from dotenv import load_dotenv
import json
import re
from langdetect import detect, DetectorFactory

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Load environment variables
load_dotenv()

# Define tool for validating and fixing JSON
@tool
def validate_and_fix_json(json_string: str) -> dict:
    """Validates a JSON string and attempts to fix common errors if invalid."""
    try:
        return {"status": "valid", "json": json.loads(json_string)}
    except json.JSONDecodeError as e:
        # Attempt to fix common JSON errors (e.g., trailing commas)
        fixed_json = json_string
        fixed_json = re.sub(r',\s*}', '}', fixed_json)
        fixed_json = re.sub(r',\s*]', ']', fixed_json)
        try:
            parsed = json.loads(fixed_json)
            return {"status": "fixed", "json": parsed}
        except json.JSONDecodeError:
            return {"status": "invalid", "error": str(e), "raw": json_string}

# Initialize connection to the LLM
id_model = "llama3-70b-8192"
llm = ChatGroq(
    model=id_model,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define function to generate content using the LLM
def llm_generate(llm, prompt):
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing specialist with a focus on SEO and persuasive writing. Always respond in the language specified in the prompt."),
        ("human", "{prompt}"),
    ])
    chain = template | llm | StrOutputParser()
    res = chain.invoke({"prompt": prompt})
    return res

# Configure Streamlit page settings
st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")
st.title("Content Generator")

# Create form fields for user input
topic = st.text_input("Theme:", placeholder="Ex: mental health, saúde mental, mentale Gesundheit, психическое здоровье, salute mentale, मानसिक स्वास्थ्य, etc.")
platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tone:", ['Normal', 'Informative', 'Inspirational', 'Urgent', 'Informal'])
length = st.selectbox("Size:", ['Short', 'Medium', 'Long'])
audience = st.selectbox("Target Audience:", ['General', 'Young Adults', 'Families', 'Seniors', 'Teenagers'])
cta = st.checkbox("Include call to action")
hashtags = st.checkbox("Return Hashtags")
keywords = st.text_area("Keywords (SEO):", placeholder="Ex: well-being, bem-estar, Wohlbefinden, благополучие, benessere, कल्याण...")

# Handle content generation when the button is clicked
if st.button("Generate content"):
    # Detect the language of the topic input
    try:
        detected_language = detect(topic) if topic.strip() else "en"  # Default to English if topic is empty
        language_map = {
            "pt": "Portuguese",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ru": "Russian",
            "it": "Italian",
            "hi": "Hindi",
        }
        language = language_map.get(detected_language, "English")
    except Exception:
        language = "English"  # Fallback to English in case of error

    # Define the prompt for the LLM
    prompt = f"""
    Write an SEO-optimized text about the topic '{topic}'.
    Return only the final text in your response and do not include it in quotation marks.
    - Where it will be published: {platform}.
    - Tone: {tone}.
    - Target audience: {audience}.
    - Length: {length}.
    - {"Include a clear call to action." if cta else "Do not include a call to action"}
    - {"Return relevant hashtags at the end of the text." if hashtags else "Do not include hashtags."}
    {"- Keywords that should be present in this text (for SEO): " + keywords if keywords else ""}
    - Create an additional paragraph showing the response in a valid, structured JSON object.
    - The JSON must be properly formatted with indentation (pretty-printed).
    - The response must be entirely in {language}, including the text, hashtags, and JSON keys/values.
    """
    try:
        # Generate content using the LLM
        res = llm_generate(llm, prompt)

        # Extract text and JSON parts from the response
        json_start = res.find("{")
        json_end = res.rfind("}") + 1
        text_part = res[:json_start].strip()
        json_part = res[json_start:json_end].strip()

        # Display the generated text
        st.markdown("### Generated Content")
        st.markdown(text_part)

        # Validate and fix JSON using the tool
        result = validate_and_fix_json(json_part)

        # Display the JSON output
        st.markdown("### JSON Output")
        if result["status"] in ["valid", "fixed"]:
            st.code(json.dumps(result["json"], indent=2, ensure_ascii=False), language="json")
            if result["status"] == "fixed":
                st.warning("The original JSON contained errors but was automatically fixed.")
        else:
            st.error(f"JSON Error: {result['error']}")
            st.code(result["raw"], language="json")

    except Exception as e:
        st.error(f"Error: {e}")