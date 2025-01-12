# AI-Driven English Communication Platform

This repository hosts the codebase for an AI-powered platform designed to enhance English fluency, pronunciation, and grammar through real-time conversational practice. The platform integrates advanced AI technologies to deliver personalized, engaging, and effective learning experiences.

---

## Project Description

The **AI-Driven English Communication Platform** is a cutting-edge application that leverages artificial intelligence to help users improve their English language skills. By engaging in real-time conversations with an AI, users can enhance their fluency, pronunciation, and grammar while receiving personalized feedback and progress insights. 

Key features include:
- **Speech-to-Text Transcription**: Converts spoken language into text using Whisper models.
- **Text-to-Speech Audio Responses**: Generates clear, natural-sounding AI responses with TTS models.
- **Context-Aware Conversations**: Utilizes memory management to provide relevant and personalized interactions.
- **User Progress Tracking**: Offers feedback on language use and highlights areas for improvement.

Built with a robust tech stack including Python (Flask), Supabase, AWS, and GPU-optimized AI tools, this platform is designed for scalability, efficiency, and user engagement. It aims to make language learning accessible, interactive, and effective for users worldwide.

---

## Features

### 1. **Real-time AI-Driven Conversations**
- Engage in natural conversations with an AI that adapts to the user's goals and preferences.
- Context-aware responses based on personalized memory management.

### 2. **Speech-to-Text (STT)**
- Uses **faster-whisper** library for high-quality audio transcription.
- Supports English transcription with low latency.

### 3. **Text-to-Speech (TTS)**
- Leverages **TTS models** (`tts_models/en/ljspeech/vits`) for clear and natural-sounding audio responses.
- Audio streaming for real-time interaction.

### 4. **User Memory Management**
- Extracts and saves user-specific data like preferences, goals, and events for personalized responses.
- Retrieves and integrates relevant memories into ongoing conversations.

### 5. **Conversation History**
- Stores chat history in **Supabase** to provide context-aware responses.
- Summarizes conversations to highlight key insights and areas for improvement.

### 6. **Feedback Mechanisms**
- Provides constructive feedback on pronunciation, vocabulary, and language use.
- Summarizes user progress at the end of each session.

### 7. **User Authentication and Security**
- Implements JWT-based authentication and role-based access control.
- API key management for secure access to app functionalities.

### 8. **Cloud Integration**
- Hosted on **AWS** for scalability and reliability.
- Uses **Supabase** for database operations and user authentication.

---

## Tech Stack

### **Languages and Frameworks**
- **Python**: Backend development (Flask), AI model integration.
- **JavaScript**: Frontend development.

### **APIs**
- Custom APIs for STT, TTS, and conversation handling.

### **Platforms**
- **Supabase**: Database, authentication, and API management.
- **AWS/GCP**: Hosting and performance optimization.

### **AI Tools**
- **faster-whisper**: Fast and accurate speech-to-text.
- **TTS**: GPU-optimized text-to-speech.
- **Groq**: Advanced AI completion for chat handling.

### **Libraries**
- **Flask**: Web framework for backend APIs.
- **ThreadPoolExecutor**: Parallel processing for faster responses.

### **Hardware**
- **GPU-Optimized Servers**: Real-time transcription and audio generation.

---

## Installation

### **Prerequisites**
1. Python 3.8 or higher.
2. Node.js (for frontend integration).
3. GPU-enabled system (optional but recommended for performance).

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/ashikjoy21/convo-backend.git
   cd convo-backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Supabase:
   - Create a Supabase project and configure the database.
   - Update the environment variables in `.env` with your Supabase credentials.

4. Run the backend:
   ```bash
   python app.py
   ```
5. (Optional) Set up the frontend:
   - Navigate to the `frontend` directory and install dependencies:
     ```bash
     cd frontend
     npm install
     ```
   - Start the frontend server:
     ```bash
     npm start
     ```

---

## Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
JWT_SECRET=your-jwt-secret
TTS_MODEL_PATH=path-to-tts-model
WHISPER_MODEL_PATH=path-to-whisper-model
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

---

## Usage

1. **Sign Up / Log In**: Users can create an account or log in using the app’s authentication system.
2. **Start Conversations**: Begin a conversation with the AI and receive real-time responses.
3. **Feedback and Progress**: View personalized feedback and progress summaries at the end of each session.
4. **Integration with Devices**: Optionally integrate with smart devices for hands-free interaction.

---

## Deployment

### **Deploying on AWS**
1. Use **AWS Elastic Beanstalk** or **EC2** for hosting the backend.
2. Configure load balancing and auto-scaling for high availability.

### **Frontend Deployment**
- Use **AWS Amplify** or **Vercel** for hosting the frontend.

### **Database Hosting**
- Ensure Supabase instance is properly configured with secure access.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For questions or support, contact:
- **Email**: ashikjoy21@gmail.com


