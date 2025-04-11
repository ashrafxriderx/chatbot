import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google AI client
api_key = os.getenv("GOOGLE_API_KEY", "")
genai.configure(api_key=api_key)

def get_ai_response(question, lesson_context, chat_history):
    """
    Generate AI tutor response based on user question and lesson context
    
    Args:
        question: User's question
        lesson_context: The current lesson content for context
        chat_history: Previous conversation history
    
    Returns:
        AI-generated response
    """
    try:
        # Setup the model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create system message
        system_prompt = f"""You are an AI tutor specializing in teaching about the current topic.
        You are helping the student with a specific lesson. Here's the context of the current lesson:
        
        {lesson_context}
        
        Respond to the student's question in a helpful, educational manner.
        Provide clear explanations with examples when appropriate.
        Keep responses concise but thorough.
        If you don't know the answer, say so instead of making up information.
        """
        
        # Format conversation history for Google AI
        chat = model.start_chat(history=[])
        
        # Add system prompt first
        chat.send_message(system_prompt)
        
        # Add chat history (last 5 messages max to avoid token limits)
        for msg in chat_history[-5:]:
            role = "user" if msg["role"] == "user" else "model"
            if role == "user":
                chat.send_message(msg["content"])
            
        # Send the current question
        response = chat.send_message(question)
        
        return response.text
    
    except Exception as e:
        return f"I'm sorry, I encountered an error while generating a response. Please try again. Error details: {str(e)}"