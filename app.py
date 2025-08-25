import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Defining the tool to validate and correct JSON
@tool
def validate_and_fix_json(json_string: str) -> dict:
    """Valida um JSON e tenta corrigir erros comuns se inválido."""
    try:
        # Try to parse the JSON
        return {"status": "valid", "json": json.loads(json_string)}
    except json.JSONDecodeError as e:
        # Attempts to correct common errors (e.g., missing quotation marks, extra commas)
        fixed_json = json_string
        # Remove extra commas before }
        fixed_json = re.sub(r',\s*}', '}', fixed_json)
        # Removes extra commas before ]
        fixed_json = re.sub(r',\s*]', ']', fixed_json)
        try:
            # TTry parsing again
            parsed = json.loads(fixed_json)
            return {"status": "fixed", "json": parsed}
        except json.JSONDecodeError:
            return {"status": "invalid", "error": str(e), "raw": json_string}

# Connection with LLM
id_model = "llama3-70b-8192"
llm = ChatGroq(
    model=id_model,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Generation function
def llm_generate(llm, prompt):
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing specialist with a focus on SEO and persuasive writing."),
        ("human", "{prompt}"),
    ])
    chain = template | llm | StrOutputParser()
    res = chain.invoke({"prompt": prompt})
    return res

st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")
st.title("Content Generator")

# Form fields
topic = st.text_input("Theme:", placeholder="Ex: mental health, healthy eating, prevention, etc.")
platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tone:", ['Normal', 'Informative', 'Inspirational', 'Urgent', 'Informal'])
length = st.selectbox("Size:", ['Short', 'Medium', 'Long'])
audience = st.selectbox("Target Audience:", ['General', 'Young Adults', 'Families', 'Seniors', 'Teenagers'])
cta = st.checkbox("Include call to action")
hashtags = st.checkbox("Return Hashtags")
keywords = st.text_area("Keywords (SEO):", placeholder="Ex: well-being, preventive medicine...")

if st.button("Generate content"):
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
    - Generate the text in the language identified in the topic.
    """
    try:
        res = llm_generate(llm, prompt)

        # Extract text and JSON
        json_start = res.find("{")
        json_end = res.rfind("}") + 1
        text_part = res[:json_start].strip()
        json_part = res[json_start:json_end].strip()

        # Display the generated text
        st.markdown("### Generated Content")
        st.markdown(text_part)

        # Use the tool to validate/correct JSON
        result = validate_and_fix_json(json_part)

        # Display the JSON
        st.markdown("### JSON Output")
        if result["status"] in ["valid", "fixed"]:
            st.code(json.dumps(result["json"], indent=2, ensure_ascii=False), language="json")
            if result["status"] == "fixed":
                st.warning("The original JSON contained errors, but it was automatically fixed.")
        else:
            st.error(f"Erro no JSON: {result['error']}")
            st.code(result["raw"], language="json")

    except Exception as e:
        st.error(f"Erro: {e}")