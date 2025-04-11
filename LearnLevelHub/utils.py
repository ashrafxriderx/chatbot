import streamlit as st
import re

def initialize_session_state():
    """
    Initialize all required session state variables if they don't exist
    """
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Beginner"
    
    if "course_data" not in st.session_state:
        st.session_state.course_data = None
    
    if "current_module" not in st.session_state:
        st.session_state.current_module = 1
    
    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = 1
    
    if "completed_lesson_ids" not in st.session_state:
        st.session_state.completed_lesson_ids = set()
    
    if "completed_lessons" not in st.session_state:
        st.session_state.completed_lessons = 0
    
    if "total_lessons" not in st.session_state:
        st.session_state.total_lessons = 0
        
        # Calculate total lessons if course data exists
        if st.session_state.course_data:
            st.session_state.total_lessons = sum(
                len(module["lessons"]) for module in st.session_state.course_data["modules"]
            )
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def format_lesson_content(content):
    """
    Format lesson content with proper markdown and styling
    
    Args:
        content: Raw lesson content text
    
    Returns:
        Formatted HTML/markdown content
    """
    # Handle headings - make sure h3 and h4 are used (not h1/h2)
    content = re.sub(r'^# (.*?)$', r'### \1', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'#### \1', content, flags=re.MULTILINE)
    
    # Ensure code blocks are properly formatted
    content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
    
    # Enhance bullet points with better spacing
    content = re.sub(r'^\* (.*?)$', r'• \1<br>', content, flags=re.MULTILINE)
    content = re.sub(r'^- (.*?)$', r'• \1<br>', content, flags=re.MULTILINE)
    
    # Add paragraph breaks for readability
    content = re.sub(r'\n\n', r'<br><br>', content)
    
    return content
