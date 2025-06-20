from flask import Flask, render_template_string, request
import openai
import base64
import os

# === CONFIG ===
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Listing Generator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 700px;
      margin: 50px auto;
      background: #fff;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h1 {
      text-align: center;
      color: #333;
    }
    form {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    input[type="file"] {
      padding: 8px;
    }
    input[type="submit"] {
      padding: 10px;
      background: #007bff;
      border: none;
      color: #fff;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
    }
    input[type="submit"]:hover {
      background: #0056b3;
    }
    .result {
      background: #f9f9f9;
      padding: 15px;
      border-radius: 4px;
      margin-top: 20px;
      white-space: pre-wrap;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Listing Generator</h1>
    <p style="text-align:center;">Upload an item photo and let AI generate your listing details!</p>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" required>
      <input type="submit" value="Generate Listing">
    </form>

    {% if result %}
      <div class="result">
        <h3>Generated Listing:</h3>
        <pre>{{ result }}</pre>
      </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            img_bytes = file.read()
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{base64_img}"

            chat_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are an expert at writing online marketplace listings. "
                                    "Given this image, generate the following:\\n"
                                    "- A clear, SEO-friendly title (under 80 characters)\\n"
                                    "- A detailed description that covers brand, color, style, material, condition, and any unique features\\n"
                                    "- 5-10 relevant keywords (comma-separated)\\n\\n"
                                    "Do not make up details that are not visible in the image."
                                )
                            },
                            { "type": "image_url", "image_url": image_data_url }
                        ]
                    }
                ],
                max_tokens=500
            )
            result = chat_response.choices[0].message.content

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
