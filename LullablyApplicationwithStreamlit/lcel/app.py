import streamlit as st
from components.generate_lullaby import generate_lullaby





def main():
    st.set_page_config(
        page_title="Generative  Children's Lullaby",
        layout="centered"
    )

    st.title(
        "Let AI write and Translate a Lullaby for You"
    )

    st.header(
        "Get Started..."
    )

    location_input = st.text_input(
        label="Where is the story set?"
    )

    main_character_input = st.text_input(
        label="What's the main character?"
    )
    language_input = st.text_input(
        label="Translate story into ..."
    )

    submit_button = st.button(
        "Submit"
    )

    if location_input and main_character_input and language_input:
        if submit_button:
            with st.spinner("Generating lullaby..."):
                response = generate_lullaby(
                    location=location_input,
                    name=main_character_input,
                    language=language_input
                )
                with st.expander("English Version"):
                    st.write(
                        response['story']
                    )
                with st.expander(f"{language_input} Version"):
                    st.write(
                        response['translated']
                    )


            st.success("Lullaby Successfullu Generated!")

    pass

if __name__ == '__main__':
    main()