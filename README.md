# AACE It! 🗣️✨
### Augmentative & Alternative Communication Meets Interactive Speech Practice

**CodeRed Orion 2026 | Hackathon Project**

AACE It! is an accessibility-focused web application designed to support people with speech and communication difficulties through **Augmentative and Alternative Communication (AAC)**, AI-powered phrase suggestions, text-to-speech, and interactive communication practice.

Our goal is to make communication more accessible, engaging, and empowering by combining practical communication tools with opportunities to practice communication skills.

## 💜 The Problem

Communication is essential to everyday life, but not everyone communicates through speech in the same way.

People with speech and communication difficulties may rely on AAC tools to express their needs, feelings, questions, and ideas.

Traditional communication tools can also present challenges, including the effort required to construct messages, reliance on typing, and limited opportunities for engaging communication practice.

We wanted to explore how AI and accessible software design could help address these challenges.

## 💡 Our Solution

**AACE It! combines AAC-style communication with interactive practice in one application.**

Users can select communication cards, type messages, receive AI-powered phrase suggestions, and have their messages spoken aloud.

The application also includes communication practice activities designed to make learning and practicing more interactive.

Rather than focusing solely on speech production, AACE It! recognizes that **communication itself is the priority**. Users can communicate through text, selectable phrases, and synthesized speech without needing to speak.

## ✨ Features

### 💬 My Words — AAC Communication

An AAC-inspired communication interface that helps users express themselves.

- **Quick Communication Cards:** Select common needs, emotions, questions, and social phrases.
- **Custom Message Editor:** Type or edit messages before communicating.
- **AI Phrase Suggestions:** Use Google Gemini to generate up to three contextually relevant communication phrases.
- **Text-to-Speech:** Convert messages into spoken audio using ElevenLabs.
- **Message Controls:** Clear messages or remove the last word.
- **Accessible Communication Options:** Communicate using selectable buttons rather than relying exclusively on typing.

Example:

A user enters:

> I need

Gemini can suggest complete phrases such as:

- I need some water.
- I need help, please.
- I need a break.

The user can select a suggestion and have it spoken aloud.

### 🔊 Text-to-Speech

AACE It! integrates **ElevenLabs** to generate spoken audio from text.

This allows users to communicate verbally through synthesized speech without needing to produce speech themselves.

### 🧠 AI-Powered Phrase Suggestions

AACE It! uses **Google Gemini** to help users construct communication phrases.

The AI is instructed to generate short, natural, first-person suggestions relevant to the user's input.

Suggestions are intended to support communication, not make decisions on behalf of the user.

### 🎮 Match It! — Communication Practice

An interactive matching activity where users practice associating communication concepts with the correct responses.

The game includes:

- Multiple-choice matching rounds
- Answer checking and feedback
- Difficulty-based exercises

### 🎤 Say It! — Speech Practice

A speech practice feature designed around short words and phrases.

The backend includes practice exercises and answer-checking functionality, with speech-to-text integration available through ElevenLabs.

**Development status:** The full frontend speech-practice experience is still being integrated.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Streamlit | Interactive web frontend |
| FastAPI | Backend API and application logic |
| Google Gemini | AI-powered phrase suggestions |
| ElevenLabs | Text-to-speech and speech-to-text |
| Pydantic | Request validation |
| SlowAPI | API rate limiting |
| Git & GitHub | Version control and collaboration |

## 🏗️ System Architecture

AACE It! separates the user interface from its backend services.

```text
                 AACE It!
              Streamlit UI
             localhost:8501
                    |
                    | HTTP Requests
                    v
                FastAPI
             localhost:8000
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
      Gemini     ElevenLabs   Practice
       API          API        Games
        |           |           |
        v           v           v
      Phrase      Speech      Exercises
    Suggestions   Services    & Feedback
```

**Frontend:** Handles navigation, communication cards, message editing, prediction selection, audio playback, and practice interfaces.

**Backend:** Handles request validation, Gemini phrase generation, ElevenLabs API integration, and practice game logic.

## 📁 Project Structure

```text
CodeRedOrion/
│
├── BackEnd/
│   ├── main.py
│   ├── practice.py
│   ├── requirements.txt
│   └── keys.env
│
├── FrontEnd/
│   ├── app.py
│   ├── myWordsUI.py
│   └── games/
│       ├── matchItUI.py
│       └── sortItUI.py
│
└── README.md
```

**Security note:** `keys.env` contains private API credentials and must not be committed to GitHub.

## 🚀 Getting Started

### Prerequisites

Before running the application, install:

- Python 3.12
- Git
- A Google Gemini API key
- An ElevenLabs API key

### 1. Clone the repository

```bash
git clone https://github.com/MossyStone/CodeRedOrion.git
cd CodeRedOrion
```

### 2. Set up the backend

From the project root:

```powershell
cd BackEnd
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure API keys

Create a file named `keys.env` inside the `BackEnd` folder.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

Replace the placeholder values with your own credentials.

Never upload API keys or `.env` files containing secrets to a public repository.

### 4. Start the backend

While inside `BackEnd`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

The backend will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### 5. Start the frontend

Open a second terminal.

From the project root:

```powershell
cd FrontEnd
py -3.12 -m pip install streamlit requests
py -3.12 -m streamlit run app.py
```

Open the application at:

http://localhost:8501

Keep both terminals running while using AACE It!.

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Backend health check |
| `/suggest` | POST | Generate Gemini phrase suggestions |
| `/speak` | POST | Generate spoken audio |
| `/transcribe` | POST | Convert recorded speech to text |
| `/practice/say-it` | GET | Retrieve speech practice exercises |
| `/practice/say-it/{exercise_id}` | GET | Retrieve an individual exercise |
| `/practice/say-it/check` | POST | Check a speech practice attempt |
| `/practice/match-it` | GET | Retrieve matching rounds |
| `/practice/match-it/{round_id}` | GET | Retrieve an individual matching round |
| `/practice/match-it/check` | POST | Check a matching answer |

## ♿ Accessibility Philosophy

AACE It! is built around the principle that **everyone deserves a way to communicate**.

Our design priorities include:

- **Communication first:** Users should be able to express needs without completing speech exercises.
- **Multiple communication methods:** Support typed text, selectable phrases, and synthesized speech.
- **User autonomy:** AI suggestions are optional, and users choose what they want to communicate.
- **Simple interactions:** Reduce unnecessary steps when constructing and speaking messages.
- **Engaging practice:** Provide opportunities to practice communication without making practice a requirement for access.

AACE It! is an early prototype and has not undergone formal accessibility testing or clinical validation.

It is not intended to replace a personalized AAC system, speech-language pathologist, or professional communication assessment.

## 🚧 Challenges & Lessons Learned

Building AACE It! during a hackathon presented several challenges.

**Integrating multiple APIs:** We connected Google Gemini and ElevenLabs through a FastAPI backend while maintaining a separate Streamlit frontend.

**Reducing AI response times:** Initial Gemini phrase generation could take approximately 30 seconds. Adjusting the model's thinking configuration substantially improved response speed.

**Handling API availability:** External AI services can experience temporary outages or high demand. This reinforced the importance of keeping essential communication features available independently of AI suggestions.

**Managing Streamlit state:** Updating messages through interactive communication cards required careful session-state management and callbacks.

**Designing for accessibility:** We approached the application as a communication aid first and a practice platform second.

## 🔮 Future Improvements

We would like to continue developing AACE It! beyond the hackathon.

Potential improvements include:

- Combining multiple AAC cards to build custom messages
- Customizable communication boards and vocabulary
- Local phrase suggestions when AI services are unavailable
- Improved keyboard navigation and screen-reader compatibility
- More interactive communication practice games
- Expanded speech practice and feedback
- Additional voice customization options
- User testing with AAC users and accessibility professionals
- Mobile-friendly interfaces and broader device support

## 👩‍💻 Team

Built by a two-person student development team for **CodeRed Orion 2026**.

This project brings together our interests in software development, artificial intelligence, and accessibility.

## 🙏 Acknowledgments

- **CodeRed Orion** — For providing the opportunity to develop and present this project.
- **Google Gemini** — For AI-powered phrase suggestions.
- **ElevenLabs** — For speech synthesis and transcription technologies.
- **Streamlit & FastAPI** — For the frameworks used to build our application.

---

### 💜 AACE It!
**Your words. Your voice. Your way.**

*Built to explore a more accessible future for communication.*
