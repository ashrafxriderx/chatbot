import streamlit as st
import os
from course_generator import generate_course_content
from ai_tutor import get_ai_response
from utils import initialize_session_state, format_lesson_content

# Set page configuration
st.set_page_config(
    page_title="AI Learning Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Main application layout
def main():
    # Home page - Course Generation UI
    if st.session_state.current_page == "home":
        col1, col2, col3 = st.columns([1, 10, 1])
        with col2:
            st.markdown("<h1 class='main-title'>Learn anything with AI</h1>", unsafe_allow_html=True)
            st.markdown("<p class='subtitle'>Enter a topic below to generate a personalized course for it</p>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("<p class='label'>Course Topic</p>", unsafe_allow_html=True)
                topic = st.text_input("", placeholder="Search...", label_visibility="collapsed")
                
                st.markdown("<p class='label'>Difficulty Level</p>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    beginner = st.button("Beginner", 
                                         type="primary" if st.session_state.difficulty == "Beginner" else "secondary",
                                         on_click=lambda: set_difficulty("Beginner"))
                with col2:
                    intermediate = st.button("Intermediate", 
                                             type="primary" if st.session_state.difficulty == "Intermediate" else "secondary",
                                             on_click=lambda: set_difficulty("Intermediate"))
                with col3:
                    advanced = st.button("Advanced", 
                                         type="primary" if st.session_state.difficulty == "Advanced" else "secondary",
                                         on_click=lambda: set_difficulty("Advanced"))
                
                tailor_option = st.checkbox("Tell us more to tailor the course (optional)", value=False)
                if tailor_option:
                    additional_info = st.text_area("Additional information", 
                                                  placeholder="Tell us your goals, interests, or specific areas you want to learn about")
                else:
                    additional_info = ""
                
                generate_btn = st.button("Generate Course", type="primary", use_container_width=True)
                if generate_btn and topic:
                    with st.spinner("Generating your personalized course..."):
                        # Generate course content using OpenAI
                        course_data = generate_course_content(topic, st.session_state.difficulty, additional_info)
                        st.session_state.course_data = course_data
                        st.session_state.current_page = "course"
                        st.rerun()

    # Course page - Display generated course content
    elif st.session_state.current_page == "course":
        if not st.session_state.course_data:
            st.warning("No course data available. Please generate a course first.")
            st.button("Back to Home", on_click=lambda: set_page("home"))
            return
        
        # Display course header
        course_data = st.session_state.course_data
        
        # Add a back button at the top
        st.button("← Back to AI Tutor", on_click=lambda: set_page("home"))
        
        # Display course title and progress
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h1 class='course-title'>{course_data['title']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p>{len(course_data['modules'])} modules • {sum(len(module['lessons']) for module in course_data['modules'])} lessons</p>", unsafe_allow_html=True)
        with col2:
            progress_percent = int(st.session_state.completed_lessons / st.session_state.total_lessons * 100) if st.session_state.total_lessons > 0 else 0
            st.markdown(f"<div class='progress-container'>{progress_percent}% Completed</div>", unsafe_allow_html=True)
            st.button("Upgrade", type="primary")
        
        # Main course layout with sidebar for navigation
        col1, col2 = st.columns([1, 3])
        
        # Sidebar with course outline
        with col1:
            st.button("Outline", key="outline_btn")
            st.button("Map", key="map_btn")
            
            # Display modules and lessons for navigation
            for i, module in enumerate(course_data['modules'], 1):
                module_id = f"module_{i}"
                module_expanded = i == st.session_state.current_module
                
                with st.expander(f"{i}. {module['title']}", expanded=module_expanded):
                    for j, lesson in enumerate(module['lessons'], 1):
                        lesson_id = f"{module_id}_lesson_{j}"
                        is_current = i == st.session_state.current_module and j == st.session_state.current_lesson
                        
                        # Check if lesson is completed
                        is_completed = f"{i}_{j}" in st.session_state.completed_lesson_ids
                        status_icon = "✓" if is_completed else ""
                        
                        if st.button(f"{status_icon} {j}. {lesson['title']}", 
                                    key=lesson_id,
                                    type="primary" if is_current else "secondary"):
                            st.session_state.current_module = i
                            st.session_state.current_lesson = j
                            st.rerun()
        
        # Main content area
        with col2:
            if (st.session_state.current_module > 0 and 
                st.session_state.current_lesson > 0 and 
                st.session_state.current_module <= len(course_data['modules'])):
                
                module = course_data['modules'][st.session_state.current_module - 1]
                
                if st.session_state.current_lesson <= len(module['lessons']):
                    lesson = module['lessons'][st.session_state.current_lesson - 1]
                    
                    # Display lesson info
                    st.markdown(f"<p>Lesson {st.session_state.current_lesson} of {len(module['lessons'])}</p>", unsafe_allow_html=True)
                    
                    # Lesson title and content
                    st.markdown(f"<h2>{lesson['title']}</h2>", unsafe_allow_html=True)
                    
                    # Format and display lesson content
                    formatted_content = format_lesson_content(lesson['content'])
                    st.markdown(formatted_content, unsafe_allow_html=True)
                    
                    # Mark as completed button
                    lesson_id = f"{st.session_state.current_module}_{st.session_state.current_lesson}"
                    already_completed = lesson_id in st.session_state.completed_lesson_ids
                    
                    if already_completed:
                        if st.button("✓ Marked as Done", type="primary", disabled=True):
                            pass
                    else:
                        if st.button("Mark as Done", type="primary"):
                            st.session_state.completed_lesson_ids.add(lesson_id)
                            st.session_state.completed_lessons += 1
                            st.rerun()
                    
                    # AI Tutor chat interface
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown("<h3>AI Instructor</h3>", unsafe_allow_html=True)
                        
                        # Display chat history
                        for message in st.session_state.chat_history:
                            if message["role"] == "user":
                                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div class='ai-message'>{message['content']}</div>", unsafe_allow_html=True)
                        
                        # Initial greeting if no messages
                        if not st.session_state.chat_history:
                            st.markdown("<div class='ai-message'>Hey, I am your AI instructor. How can I help you today? 🤖</div>", unsafe_allow_html=True)
                            
                            # Sample questions
                            st.markdown("<p>Some questions you might have about this lesson:</p>", unsafe_allow_html=True)
                            sample_q1 = "What are the key differences between Python 2 and Python 3, and why is it important to use Python 3 for new projects?"
                            sample_q2 = "Can you provide more examples of how Python is used in specific industries, such as finance or healthcare?"
                            sample_q3 = "How does Python compare to other popular programming languages like Java or C++ in terms of performance and ease of use?"
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.button(sample_q1, key="sample_q1", on_click=lambda q=sample_q1: ask_question(q))
                            with col2:
                                st.button(sample_q2, key="sample_q2", on_click=lambda q=sample_q2: ask_question(q))
                            with col3:
                                st.button(sample_q3, key="sample_q3", on_click=lambda q=sample_q3: ask_question(q))
                        
                        # User input for questions
                        user_question = st.text_input("Ask a question about this lesson:", key="user_question")
                        if st.button("Send", key="send_question"):
                            if user_question:
                                ask_question(user_question)
                                st.session_state.user_question = ""

# Helper functions
def set_difficulty(level):
    st.session_state.difficulty = level

def set_page(page):
    st.session_state.current_page = page
    if page == "home":
        st.session_state.current_module = 0
        st.session_state.current_lesson = 0
        st.session_state.chat_history = []

def ask_question(question):
    # Add user question to chat history
    st.session_state.chat_history.append({"role": "user", "content": question})
    
    # Get current lesson context
    current_module = st.session_state.course_data['modules'][st.session_state.current_module - 1]
    current_lesson = current_module['lessons'][st.session_state.current_lesson - 1]
    lesson_context = f"Module: {current_module['title']}\nLesson: {current_lesson['title']}\nContent: {current_lesson['content']}"
    
    # Get AI response
    with st.spinner("AI is thinking..."):
        ai_response = get_ai_response(question, lesson_context, st.session_state.chat_history)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    st.rerun()

if __name__ == "__main__":
    main()
