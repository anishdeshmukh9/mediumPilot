# 🚀 MediumPilot

<div align="center">

![MediumPilot](https://img.shields.io/badge/MediumPilot-AI_Reading_Companion-1A8917?style=for-the-badge&logo=medium&logoColor=white)

**Your AI companion for reading Medium articles**

[📺 Watch Demo](#demo) • [🎯 Features](#features) • [⚡ Quick Start](#quick-start) • [💡 How It Works](#how-it-works)

</div>

---

## 📺 Demo

<div align="center">

[![MediumPilot Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

**Click above to watch the demo video**

</div>

---

## 🎯 What is MediumPilot?

MediumPilot is a Chrome extension that adds an **AI assistant** to every Medium article you read. Ask questions, get explanations, and understand complex topics—all without leaving the page.

### ✨ Features

- 💬 **Chat with Articles** - Ask any question about the article
- ✨ **Explain Selected Text** - Highlight text and get instant explanations  
- 🎯 **Smart Answers** - Responses based on the actual article content
- 🔍 **Source Highlighting** - See exactly where answers come from
- 🎨 **Beautiful Design** - Clean sidebar that fits Medium's style
- ⚡ **Fast & Free** - Instant responses powered by AI

---

## 📊 How MediumPilot Works

```mermaid
graph TB
    A[👤 You Read a Medium Article] --> B[🤖 MediumPilot Activates]
    B --> C[📚 Article is Analyzed]
    C --> D{What Do You Want?}
    
    D -->|Ask a Question| E[💭 You Type Your Question]
    D -->|Select Text| F[✨ You Highlight Text]
    
    E --> G[🔍 AI Searches Article]
    F --> G
    
    G --> H[🧠 AI Understands Context]
    H --> I[✅ You Get Answer]
    I --> J[📍 Sources Highlighted in Article]
    
    style A fill:#667eea,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#1A8917,stroke:#333,stroke-width:3px,color:#fff
    style I fill:#f093fb,stroke:#333,stroke-width:3px,color:#fff
    style J fill:#ffd700,stroke:#333,stroke-width:2px,color:#333
```

---

## 🎬 User Journey

```mermaid
journey
    title Reading with MediumPilot
    section Opening Article
      Open Medium Article: 5: You
      Sidebar Appears: 5: MediumPilot
      Article Gets Indexed: 5: AI
    section Asking Questions
      Type Your Question: 5: You
      AI Thinks: 4: MediumPilot
      Answer Appears: 5: You
      Sources Light Up: 5: You
    section Understanding More
      Highlight Complex Text: 5: You
      Get Detailed Explanation: 5: MediumPilot
      Learn Something New: 5: You
```

---

## 🔄 Complete Flow

```mermaid
flowchart LR
    A[📖 Medium Article] --> B[🔧 Extension Loads]
    B --> C[📄 Extract Content]
    C --> D[🧩 Split into Chunks]
    D --> E[💾 Save to Database]
    
    F[❓ Your Question] --> G[🔍 Find Relevant Parts]
    G --> H[🤖 Generate Answer]
    H --> I[💬 Display in Sidebar]
    I --> J[✨ Highlight Sources]
    
    E -.-> G
    
    style A fill:#1A8917,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style I fill:#f093fb,stroke:#333,stroke-width:2px,color:#fff
    style J fill:#ffd700,stroke:#333,stroke-width:2px,color:#333
```

---

## ⚡ Quick Start

### 1️⃣ Install Backend

```bash
# Clone the project
git clone https://github.com/yourusername/mediumpilot.git
cd mediumpilot

# Install Python packages
pip install -r requirements.txt

# Add your API key
echo "HF_TOKEN=your_token_here" > .env

# Start server
python -m uvicorn main:app --reload
```

### 2️⃣ Install Extension

1. Open Chrome → Go to `chrome://extensions/`
2. Turn on **Developer mode**
3. Click **Load unpacked**
4. Select the extension folder
5. Done! 🎉

### 3️⃣ Use It

1. Visit any Medium article
2. See the sidebar appear on the right
3. Start asking questions!

---

## 💡 Two Ways to Use

```mermaid
graph TD
    A[🚀 MediumPilot] --> B[📄 Ask Document Mode]
    A --> C[✨ Ask Selected Mode]
    
    B --> D[Ask about entire article]
    B --> E[Get comprehensive answers]
    B --> F[Perfect for summaries]
    
    C --> G[Highlight specific text]
    C --> H[Get focused explanations]
    C --> I[Perfect for complex parts]
    
    style A fill:#1A8917,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#f093fb,stroke:#333,stroke-width:2px,color:#fff
```

---

## 🏗️ System Overview

```mermaid
graph TB
    subgraph "🌐 Your Browser"
        A[Medium Page]
        B[MediumPilot Sidebar]
    end
    
    subgraph "🖥️ Backend Server"
        C[API Server]
        D[AI Brain]
    end
    
    subgraph "💾 Storage"
        E[Article Database]
    end
    
    A -->|Article Content| C
    C -->|Save| E
    B -->|Question| C
    C -->|Search| E
    E -->|Relevant Parts| D
    D -->|Answer| B
    B -->|Highlight| A
    
    style A fill:#1A8917,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#f093fb,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#764ba2,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#ffd700,stroke:#333,stroke-width:2px,color:#333
```

---

## 📱 What You'll See

### The Sidebar

- **Header** - Shows status (Indexing/Ready)
- **Mode Switch** - Toggle between "Ask Document" and "Ask Selected"
- **Chat Area** - Your conversation with AI
- **Input Box** - Where you type questions

### The Magic

When you ask a question:
1. AI searches the article
2. Finds relevant paragraphs
3. Creates a clear answer
4. Highlights those paragraphs in yellow
5. Shows answer in the sidebar

---

## 🎨 Features in Detail

```mermaid
mindmap
  root((MediumPilot))
    Smart Q&A
      Natural conversation
      Context aware
      Accurate answers
    Text Selection
      Highlight any text
      Instant explanations
      Deep dives
    Visual Feedback
      Source highlighting
      Typing animations
      Clean design
    Fast Performance
      Instant responses
      Smart caching
      Efficient search
```

---

## 📂 Project Files

```
mediumpilot/
│
├── 🔧 Backend (Python)
│   ├── main.py                 → Main server
│   ├── loader.py               → Process articles
│   ├── embeddings_store.py     → Save to database
│   ├── retrieval.py            → Search articles
│   ├── rag_argumentation.py    → Build prompts
│   └── rag_generation.py       → Generate answers
│
├── 🎨 Extension (JavaScript)
│   ├── manifest.json           → Extension setup
│   ├── contentScript.js        → Extract articles
│   ├── sidebar.html            → UI structure
│   ├── sidebar.js              → UI logic
│   └── sidebar.css             → Styling
│
└── 📚 Database
    └── chroma_vector_db/       → Stored articles
```

---

## 🔄 Behind the Scenes

```mermaid
sequenceDiagram
    participant 👤 You
    participant 🎨 Sidebar
    participant 🖥️ Server
    participant 💾 Database
    participant 🤖 AI
    
    👤->>🎨: Open Medium Article
    🎨->>🖥️: Send Article Text
    🖥️->>💾: Save Article
    💾-->>🎨: ✅ Ready!
    
    👤->>🎨: Ask Question
    🎨->>🖥️: Send Question
    🖥️->>💾: Find Relevant Parts
    💾-->>🖥️: Return Matches
    🖥️->>🤖: Generate Answer
    🤖-->>🖥️: Smart Response
    🖥️-->>🎨: Send Answer
    🎨-->>👤: Show Answer + Highlights
```

---

## 🛠️ Technologies Used

```mermaid
graph LR
    A[MediumPilot] --> B[Chrome Extension]
    A --> C[Python Server]
    A --> D[AI Models]
    A --> E[Database]
    
    B --> B1[JavaScript]
    B --> B2[HTML/CSS]
    
    C --> C1[FastAPI]
    C --> C2[LangChain]
    
    D --> D1[HuggingFace]
    D --> D2[LLM]
    
    E --> E1[ChromaDB]
    E --> E2[Vector Storage]
    
    style A fill:#1A8917,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#f5576c,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#764ba2,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#ffd700,stroke:#333,stroke-width:2px,color:#333
```

---

## 🚀 Coming Soon

- 🎤 Voice input for questions
- 🔊 Listen to answers
- 📱 Mobile browser support
- 🌍 Multiple languages
- 📝 Save conversation history
- 🤝 Share insights with friends

---

## ❓ FAQ

**Q: Is it free?**  
A: Yes! You just need a free HuggingFace account.

**Q: Does it work on all websites?**  
A: Currently only Medium.com articles.

**Q: Is my data private?**  
A: Articles are stored locally on your computer.

**Q: Can I use it offline?**  
A: No, it needs internet for AI responses.

---

## 🤝 Contributing

Want to help make MediumPilot better?

1. Fork this repository
2. Make your improvements
3. Submit a pull request
4. We'll review and merge!

---

## 📧 Contact

**Created by Anish Deshmukh**

- GitHub: [@anishdeshmukhO9](https://github.com/anishdeshmukhO9)
- Email: your.email@example.com

---

<div align="center">

### ⭐ Enjoying MediumPilot? Give us a star!

**Made with ❤️ for better reading**

</div>
