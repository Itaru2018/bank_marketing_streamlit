import streamlit as st

def main():
    st.header('Contact')
    st.markdown('''
                If you'd like to get in touch, feel free to reach out through any of the links below:
                
                ---

                **Email**
                [itaruyasumura@gmail.com](mailto:itaruyasumura@gmail.com)

                **LinkedIn**
                [https://linkedin.com/in/itaru-yasumura-27b05a1b2](https://linkedin.com/in/itaru-yasumura-27b05a1b2)

                **GitHub**
                - **Jupyter notebook**
                [https://github.com/Itaru2018/bankmarketing_jupyter](https://github.com/Itaru2018/bankmarketing_jupyter)

                - **Deployment**
                  - Front end:
                  [https://github.com/Itaru2018/bank_marketing_streamlit](https://github.com/Itaru2018/bank_marketing_streamlit)
                
                  - Back end:
                  [https://github.com/Itaru2018/bank_marketing_fastapi](https://github.com/Itaru2018/bank_marketing_fastapi)

                ''')


# Allow this file to be tested on its own
if __name__ == "__main__":
    main()