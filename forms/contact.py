import streamlit as st
import re
import requests

WEBHOOK_URL = st.secrets["WEBHOOK_URL"]


contact_info = {
    "en": {
        "title": "Contact Me",
        "name_label": "First Name",
        "email_label": "Email",
        "message_label": "Message",
        "submit_button": "Submit",
        "success_message": "Message sent",
        "webhook_error" : "Email service is not setup. Please try again later",
        "name_error": "Please provide your name",
        "email_error": "Please provide an email address",
        "valid_email": "Please provide a valid email address",
        "message error": "Please provide a message",
        "succesful_msg": "Your message has been sent correctly",
        "error_msg": "There was an error sending your message",
        "email_placeholder": "You're sending an e-mail to data.frankly@gmail.com"
    },
    "es": {
        "title": "Contáctame",
        "name_label": "Nombre",
        "email_label": "Correo",
        "message_label": "Mensaje",
        "submit_button": "Enviar",
        "success_message": "Mensaje enviado",
        "webhook_error" : "El servicio de email no está configurado. Intenta más tarde.",
        "name_error": "Por favor ingresa tu nombre",
        "email_error": "Por favor ingresa un correo electrónico",
        "valid_email": "Por favor ingresa un correo válido",
        "message_error": "Por favor ingresa un mensaje",
        "succesful_msg": "El mensaje se ha enviado correctamente",
        "error_msg": "Ha ocurrido un error al enviar el mensaje",
        "email_placeholder": "Estás enviando un correo a data.frankly@gmail.com"
    }
}

def is_valid_email(email):
    # Regex pattern for email vlaidation
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def contact_form(lang_code):
    with st.form("contact_form"):
        name = st.text_input(contact_info[lang_code]["name_label"], placeholder=contact_info[lang_code]["name_label"])
        email = st.text_input(contact_info[lang_code]["email_label"], placeholder=contact_info[lang_code]["email_label"])
        message = st.text_input(contact_info[lang_code]["message_label"], placeholder=contact_info[lang_code]["email_placeholder"])
        submit_button = st.form_submit_button(contact_info[lang_code]["submit_button"])

        if submit_button:
            if not WEBHOOK_URL:
                st.error(
                    f"{contact_info[lang_code]['webhook_error']}", icon="📧"
                )
                st.stop()

            if not name:
                st.error(f"{contact_info[lang_code]['name_error']}")
            
            if not email:
                st.error(f"{contact_info[lang_code]['email_error']}")
                st.stop()
            
            if not is_valid_email(email):
                st.error(f"{contact_info[lang_code]['valid_email']}")
                st.stop()
            
            if not message:
                st.error(f"{contact_info[lang_code]['message_error']}")
                st.stop()

            # PRepare the data and send it
            data = {"email": email, "name":name, "message":message}
            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 200:
                st.success(f"{contact_info[lang_code]['succesful_msg']}")
            else:
                st.error(f"{contact_info[lang_code]['error_msg']}")

            # st.success(contact_info[lang_code]["success_message"])
