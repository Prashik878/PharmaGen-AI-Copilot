import os
import google.generativeai as genai

# जेमिनी एपीआई की (API Key) सेट करणे
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def generate_answer_stream(query, context, selected_lang):
    """
    🎯 ही फंक्शन जेमिनी मॉडेल वापरून उत्तराचे शब्द एक-एक करून (Stream) जनरेट करते.
    """
    try:
        model = genai.GenerativeModel("gemini-3.6-flash")
        # प्रॉमप्ट तयार करणे
        # 🎯 app/gemini_client.py मधील प्रॉम्टचा भाग असा अपडेट करा:

        # प्रॉमप्ट फॉरमॅट सुधारला
        prompt = f"""
        You are a Pharmaceutical Quality Assurance Expert. 
        Answer the user's query based ONLY on the provided context.
        If the context does not contain the answer, reply with 'Insufficient information'.
        
        FORMATTING RULES:
        1. Do NOT start every sentence with "Based on the provided context". 
        2. Give direct, clean, and professional answers.
        3. Use bullet points or bold text where necessary to make it highly readable and properly formatted.
        
        Language: {selected_lang}
        Context: {context}
        Query: {query}
        """

        
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        yield f"Error in Gemini Client: {str(e)}"
