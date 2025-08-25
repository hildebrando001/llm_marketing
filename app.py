import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import json

load_dotenv()

## conexão com a LLM
id_model = "llama3-70b-8192"
llm = ChatGroq(
    model=id_model,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

## função de geração
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

# Campos do formulário
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
    """
    try:
        res = llm_generate(llm, prompt)

        # tentar extrair JSON se houver
        try:
            json_start = res.find("{")
            json_end = res.rfind("}") + 1
            json_part = res[json_start:json_end]

            parsed = json.loads(json_part)
            formatted_json = json.dumps(parsed, indent=2, ensure_ascii=False)

            # exibe o texto antes do JSON
            st.markdown(res[:json_start].strip())
            st.markdown("### Estrutura JSON")
            st.code(formatted_json, language="json")
        except Exception:
            # fallback: mostra tudo como texto
            st.markdown(res)

    except Exception as e:
        st.error(f"Erro: {e}")