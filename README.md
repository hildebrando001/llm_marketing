# Content Generator
[Content Generator](https://llmmarketing-7xncskmckva3w8vk2stayu.streamlit.app/)

A Streamlit-based web application that generates SEO-optimized marketing content using the Grok language model (LLaMA 3, 70B) via LangChain. The app allows users to customize content by specifying the topic, platform, tone, length, target audience, and optional features like call-to-action and hashtags. It also includes a tool for validating and fixing JSON output to ensure proper formatting.

## Features
- **Customizable Content Generation**: Create SEO-optimized text for platforms like Instagram, Facebook, LinkedIn, Blog, or Email.
- **Flexible Parameters**: Choose tone (Normal, Informative, Inspirational, Urgent, Informal), length (Short, Medium, Long), and target audience (General, Young Adults, Families, Seniors, Teenagers).
- **Optional Features**: Include a call-to-action and/or relevant hashtags.
- **JSON Validation**: Automatically validates and corrects JSON output for reliable formatting.
- **Pretty-Printed Output**: Displays generated text and JSON in a clean, readable format with syntax highlighting.

## Prerequisites
- Python 3.8+
- Streamlit
- LangChain
- LangChain-Grok
- python-dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/content-generator.git
   cd content-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Grok API key:
   ```env
   GROQ_API_KEY=your-api-key-here
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`.

3. Fill in the form:
   - **Theme**: Enter the topic (e.g., mental health, healthy eating).
   - **Platform**: Select the target platform (Instagram, Facebook, LinkedIn, Blog, Email).
   - **Tone**: Choose the tone of the content.
   - **Length**: Select the desired length.
   - **Target Audience**: Choose the audience.
   - **Include Call to Action**: Check to add a CTA.
   - **Return Hashtags**: Check to include hashtags.
   - **Keywords (SEO)**: Add SEO keywords (optional).

4. Click **Generate Content** to see the output, including the text, hashtags (if selected), and a formatted JSON object.

## Example Output
For a topic like "Martial Arts" with hashtags enabled:
```
Unlock the Power of Martial Arts!
Discover the ancient art of discipline, focus, and self-improvement. Martial arts is more than just a workout, it's a journey to master your body and mind. From Karate to Taekwondo, Judo to Kung Fu, each style offers unique benefits for a stronger, healthier you. Improve your flexibility, boost your confidence, and relieve stress. Find a martial arts class near you and start your transformation today!

#MartialArts #FitnessMotivation #SelfImprovement #Karate #Taekwondo #Judo #KungFu #Discipline #Focus #Wellness

### JSON Output
{
  "text": "Unlock the Power of Martial Arts!\nDiscover the ancient art of discipline, focus, and self-improvement...",
  "hashtags": [
    "#MartialArts",
    "#FitnessMotivation",
    "#SelfImprovement",
    "#Karate",
    "#Taekwondo",
    "#Judo",
    "#KungFu",
    "#Discipline",
    "#Focus",
    "#Wellness"
  ]
}
```

## Project Structure
- `app.py`: Main application script.
- `.env`: Environment file for storing the Grok API key (not tracked in Git).
- `requirements.txt`: List of Python dependencies.

## Dependencies
Listed in `requirements.txt`:
```
streamlit
langchain
langchain-grok
python-dotenv
```

## Notes
- The app uses the Grok API (LLaMA 3, 70B model) for content generation. Ensure you have a valid API key from xAI.
- The JSON validation tool automatically fixes common JSON errors (e.g., trailing commas) to ensure reliable output.
- For production, consider adding error logging and rate-limiting for API calls.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.