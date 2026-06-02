import ollama


async def generate_local_ai_summary(data):

    if not data:

        return "No analytics data available."

    prompt = f"""
    You are an analytics expert.

    Analyze this website analytics data and provide:
    
    1. Key trends
    2. Important observations
    3. Business insights
    4. Short recommendations

    Keep the response concise and professional.

    Analytics Data:
    {data}
    """

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]