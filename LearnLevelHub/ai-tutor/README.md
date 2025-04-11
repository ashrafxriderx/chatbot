# AI Tutor Application

An interactive AI tutor that generates personalized courses on any topic using Google's Gemini 1.5 Pro model.

## Features

- Generate comprehensive courses on any topic
- Choose difficulty level (Beginner, Intermediate, Advanced)
- Interactive AI tutor that answers questions about lessons
- Track your progress through the course
- Beautiful and intuitive user interface

## Setup Instructions

1. **Prerequisites**
   - Python 3.9 or newer
   - A Google AI API key from [Google AI Studio](https://makersuite.google.com/)

2. **Installation**

   Clone or extract this project to a folder on your computer, then:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install required packages
   pip install -r requirements.txt
   ```

3. **API Key Setup**

   Create a `.env` file in the project folder with your Google AI API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual API key.

4. **Running the Application**

   ```bash
   streamlit run app.py
   ```

   The application will open in your default web browser at http://localhost:8501

## Usage

1. **Generate a Course**
   - Enter a topic in the search box
   - Select a difficulty level
   - Optionally add custom requirements
   - Click "Generate Course"

2. **Navigate the Course**
   - Browse modules and lessons from the sidebar
   - Read lesson content in the main area
   - Mark lessons as completed to track progress

3. **Use the AI Tutor**
   - Ask questions about the current lesson
   - Get personalized explanations from the AI
   - Try the sample questions or ask your own

## Troubleshooting

- If you see errors about missing modules, make sure you've installed all dependencies.
- If you get API key errors, check that your Google AI API key is set up correctly in the `.env` file.
- Make sure your Google AI key has access to the Gemini 1.5 Pro model.

## Credits

This application was created with:
- Streamlit - For the web interface
- Google Gemini AI - For course generation and AI tutoring
- Python - For the backend logic

## License

This project is for educational purposes only. Feel free to modify and use it for your personal learning needs.