
# 🎨 PoetLens – AI-Powered Poetry Generator

PoetLens is an AI-powered web application that transforms images into creative poetry. It uses image captioning and generative AI to understand the visual elements in an uploaded image and generate meaningful poems inspired by them.

Upload an image, let AI interpret the scene, and discover the poetry hidden within it!

## ✨ Features

- **Image Upload:** Upload an image in JPG, JPEG, or PNG format.
- **AI Image Captioning:** Uses the BLIP image captioning model to identify objects and understand the scene.
- **AI Poetry Generation:** Uses Google's Gemini API to generate creative poems based on the image caption.
- **Interactive Interface:** Simple and user-friendly interface built with Streamlit.
- **Creative Expression:** Converts visual inspiration into words and emotions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyTorch | Deep learning framework |
| Hugging Face Transformers | Image captioning |
| BLIP | Image understanding and caption generation |
| Google Gemini API | AI-powered poetry generation |
| Pillow (PIL) | Image processing |
| Python-dotenv | Environment variable management |

## 📂 Project Structure

```text
PoetLens/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

> Note: The `.env` file contains your API key and should never be uploaded to GitHub.

## ⚙️ Installation and Setup

Follow these steps to run PoetLens on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/PriyaM-0725/PoetLens.git
```

### 2. Navigate to the Project Directory

```bash
cd PoetLens
```

### 3. Create a Virtual Environment

It is recommended to use Python 3.10.

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key
```

Replace `your_actual_gemini_api_key` with your API key.

**Important:** Never share your API key or commit your `.env` file to GitHub.

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🚀 How It Works

1. The user uploads an image through the Streamlit interface.
2. The BLIP model analyzes the image and generates a descriptive caption.
3. The generated caption is passed to Google's Gemini API.
4. Gemini interprets the visual description and creates a poem.
5. The generated poem is displayed in the PoetLens interface.

## 🧠 AI Models and APIs

- **BLIP:** Salesforce/blip-image-captioning-base
- **Generative AI:** Google Gemini (gemini-2.5-flash)

## 📌 Requirements

- Python 3.10 recommended
- Internet connection for downloading the BLIP model and accessing Gemini
- Google Gemini API key
- Sufficient RAM and storage for the PyTorch and Transformers dependencies

## 🔮 Future Enhancements

- Support for multiple poetry styles and genres.
- Multilingual poem generation.
- Download generated poems as PDF or text files.
- Voice narration of generated poetry.
- Improved image interpretation and personalized poem generation.

## 👩‍💻 Author

**Mohanapriya M**

GitHub: [PriyaM-0725](https://github.com/PriyaM-0725)

---

*PoetLens – Where Images Become Poetry.*
