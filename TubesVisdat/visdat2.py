import time
import numpy as np
import pandas as pd
import streamlit as st
from MarketSize import plot_top_6_regions
from AiToolsUser import plot_AiToolsUsers
from GenAIText import plot_GenAIText
from GenAIMarketSize import map_plot_Generative_AI_MarketSize, plot_top_6_genAIMarketSize



def set_bg_color(color):
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background-color: {color};
        }}
        </style>
        """, 
        unsafe_allow_html=True
    )


set_bg_color("lightblue")


st.markdown("<h1 style='text-align: center;'>ARTIFICIAL INTELLIGENCE</h1>", unsafe_allow_html=True)

_A_I = """
Artificial intelligence (AI) is technology that enables computers and machines to simulate human learning, comprehension, problem solving, decision making, creativity and autonomy.
Applications and devices equipped with AI can see and identify objects. They can understand and respond to human language. They can learn from new information and experience. They can make detailed recommendations to users and experts. 
They can act independently, replacing the need for human intelligence or intervention (a classic example being a self-driving car). But in 2024, most AI researchers and practitioners and most AI related headlines are focused on breakthroughs in generative AI (gen AI), a technology that can create original text, images, video and other content. 
"""
st.title("What Is AI?")
def stream_data(Text):
    for word in Text.split(" "):
        yield word + " "
        time.sleep(0.05)
    data = pd.read_csv("merged_data.csv")
    yield pd.DataFrame(data)

def stream_description(Text):
    for word in Text.split(" "):
        yield word + " "
        time.sleep(0.05)

if st.button("AI Description"):
    st.write_stream(stream_data(_A_I))

with st.expander("AI Market Size", expanded=True):
    st.title("Top 5 Regions AI Market Size")
    plot_top_6_regions()  # Call the function to plot the chart
    Description = """
        This bar chart illustrates the AI market size for the top 5 regions—China, Germany, India, Japan, and the United States—measured in billions of USD. 
        Each bar is divided into segments representing different AI categories: AI Robotics, Autonomous & Sensor Technologies, Computer Vision, Machine Learning, and Natural Language Processing. 
        The United States leads significantly, followed by China, with other regions having relatively smaller market sizes.
        """
    if st.button("Description"):
        st.write_stream(stream_data(Description))


with st.expander("AI Tools User", expanded=True):
    st.title("AI Tools User")
    plot_AiToolsUsers()
    Description2 = """
    This visualization represents the growth of AI tool users worldwide from 2020 to 2024.

    - The top section displays yearly user numbers, starting from 115.9 million in 2020 and increasing steadily each year to reach 314.4 million in 2024.
    - The line graph below illustrates the continuous upward trend in AI tool adoption, indicating consistent growth in user numbers over the five-year period.

    The data highlights the increasing global reliance on AI tools.
        """
    if st.button("Description 2"):
        st.write_stream(stream_description(Description2))

with st.expander("Generative AI Trend", expanded=True):
    st.title("Generative AI Trend")
    plot_GenAIText()
    Description3 = """
        this data explain all the generative AI tools that has been used in the world from 2022
        """
    if st.button("Description 3"):
        st.write_stream(stream_description(Description3))

with st.expander("Generative AI Market Size", expanded=True):
    st.title("Generative AI Market Size")
    plot_top_6_genAIMarketSize()
    map_plot_Generative_AI_MarketSize()
    Description4 = """
    This data provides insights into the growth of the generative AI market size from 2020 to 2024 and its global distribution in 2024.

    Market Size by Region (2020–2024):
    - The chart shows rapid growth in the generative AI market size globally:
    - The United States leads consistently with significant contributions to the global market size.
    - China and other major regions like Japan, Germany, and the United Kingdom also show steady growth.
    - The worldwide market size (total global market) exhibits exponential growth, surpassing $50 billion by 2024.    
        """
    if st.button("Description 4"):
        st.write_stream(stream_description(Description4))

