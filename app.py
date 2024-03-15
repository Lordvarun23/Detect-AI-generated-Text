import streamlit as st
import pickle
import pandas as pd

def highlight_max(s):
    '''
    Highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
def get_probability(text):
    vectorizer_dump = pickle.load(open("vector_1000.pickel", "rb"))
    test_data_features = vectorizer_dump.transform([text])
    loaded_model = pickle.load(open("naive_bayes_model.pkl", "rb"))
    predictions = loaded_model.predict_proba(test_data_features)
    return round(predictions[0][1],4)

def about_page():
    st.title("About")
    st.write("Welcome to Genuine Verify App! This app is designed to verify the authenticity of text.")
    st.write("""
    The Genuine Verify application addresses concerns stemming from the rise of large language models (LLMs), 
    particularly regarding potential plagiarism and educational integrity in assessing writing proficiency 
    among middle and high school students. Using advanced machine learning techniques, Genuine Verify 
    distinguishes between essays authored by students and those generated by LLMs. By analyzing subtle artifacts 
    within texts, it identifies distinctions indicative of machine-generated content. This tool serves as a valuable 
    asset for educators, helping to preserve academic integrity and nurture students' writing skills in an environment
     increasingly shaped by LLM technology.""")
    st.write("Use the navigation bar to explore different sections of the app.")

def verify_page():
    st.title("Verify")
    text_input = st.text_input("Enter text to verify:")
    probability = get_probability(text_input)
    if st.button("Verify"):
        if text_input.strip():  # Verify if the input text is not empty
            background_color = f"hsl({120 * probability}, 100%, 50%)"
            probability_text = f"Probability of Given input Generated by AI: {probability}"
            # Use markdown to set background color
            st.markdown(
                f'<div style="background-color: {background_color}; padding: 10px; border-radius: 5px;">{probability_text}</div>',unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to verify.")


def model_page():
    st.title("Model")
    st.write("Information about the model goes here.")
    st.write("Logistic regression, naive Bayes, random forest, and XGBoost were employed to train models for distinguishing between AI-generated and human-generated text. Among these, logistic regression demonstrated the most effective performance.")

    # Model accuracy data
    model_accuracy_data = {
        'Model': ['Logistic Regression', 'Naive Bayes', 'Random Forest', 'XGBoost'],
        'Accuracy': [0.96, 0.91, 0.957, 0.901]
    }

    # Create DataFrame
    accuracy_df = pd.DataFrame(model_accuracy_data)
    highlighted_df = accuracy_df.style.apply(lambda x: ['background-color: cyan' if x['Model'] == 'Logistic Regression' else '' for i in x], axis=1)
    # Display table
    st.write("Model Accuracy:")
    st.write(highlighted_df)


# Set up sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["About", "Verify", "Model"])

# Display selected page based on user selection
if selected_page == "About":
    about_page()
elif selected_page == "Verify":
    verify_page()
elif selected_page == "Model":
    model_page()

# Load and display background image
    st.markdown(
        """
        <style>
        .background {
            background-image: url('https://www.google.com/imgres?imgurl=https%3A%2F%2Fminter.io%2Fblog%2Fcontent%2Fimages%2F2023%2F04%2FMeta-launches-new-subscription-based-verification-system.jpg&tbnid=5ehfNrjBKIIrnM&vet=12ahUKEwirgPee9_OEAxXB1zgGHZrfAYkQMyg2egUIARDoAQ..i&imgrefurl=https%3A%2F%2Fminter.io%2Fblog%2Fmeta-launches-new-subscription-based-verification-system%2F&docid=d3Jp-sxFv5psVM&w=1012&h=615&q=verify%20text%20related%20animated%20images&ved=2ahUKEwirgPee9_OEAxXB1zgGHZrfAYkQMyg2egUIARDoAQ'); /* Replace URL with your image URL */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh; /* Adjust height as needed */
            width: 100%; /* Adjust width as needed */
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
        }
        </style>
        <div class="background"></div>
        """,
        unsafe_allow_html=True
    )