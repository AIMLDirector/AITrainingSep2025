import streamlit as st

st.title(" Chatbot app with Streamlit ")

user_input = st.text_input("You: ", "input your messages here...")  

st.write("Click the 'Send' button to send your message to the chatbot.")

if st.button("Send"):
    st.text_area("Chatbot: ", f"Echo: {user_input}", height=200)  
    st.success("Message sent!")

with st.sidebar:
    st.header("Generation Parameters")
    
    # Temperature: Controls randomness. Range typically from 0.0 to 2.0.
    # Lower is deterministic/factual, higher is more creative/random
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=2.0, 
        value=0.7,  # Default value
        step=0.01,
        help="Controls the randomness of the output. Lower values are more deterministic."
    )
    
    # Top-p (Nucleus Sampling): Controls the cumulative probability of chosen tokens. 
    # Range typically from 0.0 to 1.0. 
    # Recommended to only alter either temperature or top_p from default
    top_p = st.slider(
        "Top-p (Nucleus Sampling)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.9, # Default value
        step=0.01,
        help="Filters tokens based on cumulative probability mass. Only tokens that make up the top P% are considered."
    )
    
    # Top-k sampling: Controls the number of top probable tokens to consider
    top_k = st.number_input(
        "Top-k Sampling", 
        min_value=0, 
        max_value=100, # Max value can be adjusted based on model capabilities
        value=50, 
        step=1,
        help="Limits the model to the K most likely tokens at each step. Set to 0 to disable."
    )

# Main content area to display selected values
st.write(f"**Selected Temperature:** {temperature}")
st.write(f"**Selected Top-p:** {top_p}")
st.write(f"**Selected Top-k:** {top_k}")

st.markdown("---")
st.write("These values can now be passed to your Language Model API to control text generation.")

