import os
import json
import google.generativeai as genai

# Initialize Google AI client
api_key = os.getenv("GOOGLE_API_KEY", "")
genai.configure(api_key=api_key)

def generate_course_content(topic, difficulty, additional_info=""):
    """
    Generate a complete course structure and content using Google AI
    
    Args:
        topic: The main course topic
        difficulty: Difficulty level (Beginner, Intermediate, Advanced)
        additional_info: Optional additional context for course customization
    
    Returns:
        Dictionary containing the course structure and content
    """
    try:
        # Setup the model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Prepare system prompt for course generation
        system_prompt = "You are an expert course creator specializing in educational content."
        
        # Prepare user prompt for course generation
        user_prompt = f"""
        Create a comprehensive, educational course on "{topic}" at a {difficulty} level.
        
        Additional requirements: {additional_info}
        
        Structure the course with the following components:
        1. A course title
        2. 5-7 modules (main topics)
        3. 5-8 lessons per module
        4. Detailed content for each lesson
        
        For each lesson, provide:
        - A clear, descriptive title
        - Comprehensive educational content (300-500 words)
        - Key concepts and takeaways
        - Examples or practical applications when relevant
        
        Format the response as a structured JSON object with the following format:
        {{
          "title": "Course Title",
          "difficulty": "Difficulty Level",
          "modules": [
            {{
              "title": "Module Title",
              "description": "Module description",
              "lessons": [
                {{
                  "title": "Lesson Title",
                  "content": "Detailed lesson content..."
                }}
              ]
            }}
          ]
        }}
        
        IMPORTANT: Your entire response must be valid JSON only, with no other text before or after.
        """
        
        # Start a chat and generate the course content
        chat = model.start_chat(history=[])
        chat.send_message(system_prompt)
        response = chat.send_message(user_prompt)
        
        # Extract and clean the JSON response
        response_text = response.text
        
        # Remove any markdown code block markers if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        # Try to find and extract JSON content if not properly formatted
        response_text = response_text.strip()
        
        # Parse and return the course data
        return json.loads(response_text)
    
    except Exception as e:
        # Return a basic error course structure
        return {
            "title": f"Error generating course on {topic}",
            "difficulty": difficulty,
            "modules": [
                {
                    "title": "Error Module",
                    "description": "An error occurred while generating the course content.",
                    "lessons": [
                        {
                            "title": "Error Information",
                            "content": f"We encountered an error while generating your course: {str(e)}. Please try again with a different topic or check your API key configuration."
                        }
                    ]
                }
            ]
        }
