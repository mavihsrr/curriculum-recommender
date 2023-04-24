import streamlit as st
import openai
from urllib.parse import urlparse
from chat import chat
import re
prompt = [{'role':'system', 'content': '''
You are CourseGPT. You will be given a course and some future skills that need to be learned. Based on this you need to recommend courses/books or online materials for the given course and so that those future skills can be learned as well.

This will be the format of our conversation now.

Example Input: "Course: Evolutionary Algorithms, Future skills: Deep Learning, Reinforcement Learning"
Example Output: {A list of 5 courses and their urls which you recommend which complement the given course and will also help in learn those future skills.}'''}]
@st.cache_data(show_spinner=False)
def conversation(ui):
    output = chat(ui, st.session_state.message_history)
    return output
def main():
    # Set page title
    if 'search' not in st.session_state:
        st.session_state["search"] = False
    if 'message_history' not in st.session_state:
        st.session_state.message_history = prompt
    #st.session_state.message_history
    openai.api_key = st.secrets["api_key"]
    if st.session_state["search"] == False:
        title_placeholder = st.empty()
        header_placeholder = st.empty()
        course_placeholder = st.empty()
        future_skill_placeholder = st.empty()
        search_placeholder = st.empty()

        title_placeholder.title("Curriculum Recommender")
        # Set page header
        header_placeholder.header("Search for a Course and Future Skill")
        
        # Create search bar for Course and Future Skill
        course = course_placeholder.text_input("Course",value="Deep Learning")
        future_skill = future_skill_placeholder.text_input("Future Skill to Learn", "Face Recogntion, Django, AWS S3")
        
        # Create search button
        search = search_placeholder.button("Search")
    if search:
        st.session_state.search = True
        
    # If search button is clicked
    if st.session_state.search:
        # Hide search bar
        title_placeholder.empty()
        header_placeholder.empty()
        course_placeholder.empty()
        future_skill_placeholder.empty()
        search_placeholder.empty()
        
        # Move text boxes to side navigation bar
        st.sidebar.title("Search Parameters")
        st.sidebar.write(f"Course: {course}")
        st.sidebar.write(f"Future Skill to Learn: {future_skill}")
        clear = st.sidebar.button("Go Back")
        if clear:
            #st.cache_data.clear()
            st.session_state.search = False
        user_input = f"Course: {course}, Future Skills: {future_skill}. Make sure you bold the course names and give the urls and the descriptions for each course."
        
        with st.spinner("Finding the best courses..."):
            output = conversation(user_input)
        #print(output)
        output_broken = output.split("\n")[2:-2]
        while "" in output_broken:
            output_broken.remove("")
        print(output_broken)
        all_titles = []
        all_urls = []
        for i in output_broken:
            urls = re.findall(r'(https?://\S+)', i)
            result = re.search('\*\*(.*)\*\*', i)
            if result != None:
                all_titles.append(result.group(1))
            if len(urls)!= 0:
                all_urls.append(urls[0])
        output_show = "\n".join(output_broken)
        #st.write(output_show)
        all_tabs = st.tabs(all_titles)

        for i in range(len(all_tabs)):
            sentences= output_broken[i].split(". ")
            for j in sentences:
                if all_urls[i] in j:
                    sentences.remove(j)
            out = ". ".join(sentences) + "."
            all_tabs[i].write(out)
            all_tabs[i].write("Link: "+all_urls[i])
        #all_urls

if __name__ == "__main__":
    main()
