// Wait for DOM to be fully ready
setTimeout(() => {
  initializeSidebar();
}, 500);

function initializeSidebar() {
  let MODE = "ask_document";
  let selectedSnippet = "";
  let articleContent = "";
  let isFirstMessage = true;

  const chatWindow = document.getElementById("mec-chat-window");
  const sendBtn = document.getElementById("mec-send");
  const input = document.getElementById("mec-input");
  const statusBar = document.getElementById("mec-status");
  const btnDoc = document.getElementById("btn-doc");
  const btnSel = document.getElementById("btn-sel");
  const sidebarWrapper = document.getElementById("mec-sidebar-wrapper");

  if (!chatWindow || !sendBtn || !input) {
    console.error("MEC: Sidebar elements not found");
    return;
  }

  console.log("MEC: Sidebar initialized successfully");

  // ========================================
  // FIX SCROLL - STOP PROPAGATION
  // ========================================
  
  // Stop scroll propagation on the wrapper
  if (sidebarWrapper) {
    sidebarWrapper.addEventListener('wheel', (e) => {
      e.stopPropagation();
    }, { passive: false });
  }

  // Stop scroll propagation on chat window
  if (chatWindow) {
    chatWindow.addEventListener('wheel', (e) => {
      const { scrollTop, scrollHeight, clientHeight } = chatWindow;
      const delta = e.deltaY;
      const isAtTop = scrollTop <= 0;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 1;
      
      // Prevent scrolling past boundaries
      if ((isAtTop && delta < 0) || (isAtBottom && delta > 0)) {
        e.preventDefault();
      }
      
      // Always stop propagation
      e.stopPropagation();
    }, { passive: false });

    // Also handle scroll event
    chatWindow.addEventListener('scroll', (e) => {
      e.stopPropagation();
    }, { passive: false });
  }

  // ========================================
  // AUTO-RESIZE TEXTAREA
  // ========================================
  input.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
  });

  // ========================================
  // ENTER TO SEND (Shift+Enter for new line)
  // ========================================
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // ========================================
  // MODE SWITCHING WITH ANIMATION
  // ========================================
  btnDoc.onclick = () => {
    MODE = "ask_document";
    btnDoc.classList.add("active");
    btnSel.classList.remove("active");
    document.getElementById("mec-selected-box").classList.add("hidden");
    input.placeholder = "Ask anything about this article...";
  };

  btnSel.onclick = () => {
    MODE = "ask_selected";
    btnSel.classList.add("active");
    btnDoc.classList.remove("active");
    document.getElementById("mec-selected-box").classList.remove("hidden");
    input.placeholder = "Ask about the selected text...";
  };

  // ========================================
  // RECEIVE EVENTS FROM CONTENT SCRIPT
  // ========================================
  window.addEventListener("message", (event) => {
    if (event.data.type === "MEC_SELECTED_TEXT") {
      selectedSnippet = event.data.text;
      document.getElementById("selected-content").innerText = selectedSnippet;
      
      // Auto-switch to "Ask Selected" mode
      if (selectedSnippet.length > 0) {
        btnSel.click();
      }
    }

    if (event.data.type === "MEC_ARTICLE_CONTENT") {
      articleContent = event.data.text;
    }

    if (event.data.type === "MEC_ARTICLE_INDEXED") {
      statusBar.innerText = "Ready ✓";
      statusBar.classList.add("indexed");
    }
  });

  // ========================================
  // REMOVE EMPTY STATE
  // ========================================
  function removeEmptyState() {
    const emptyState = chatWindow.querySelector('.empty-state');
    if (emptyState) {
      emptyState.style.animation = 'fadeOut 0.2s ease';
      setTimeout(() => emptyState.remove(), 200);
    }
  }

  // ========================================
  // ADD MESSAGE BUBBLE
  // ========================================
  function addMessage(sender, html) {
    if (isFirstMessage) {
      removeEmptyState();
      isFirstMessage = false;
    }

    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "mec-msg-user" : "mec-msg-ai";
    bubble.innerHTML = html;
    
    chatWindow.appendChild(bubble);
    
    // Smooth scroll to bottom
    setTimeout(() => {
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 50);
  }

  // ========================================
  // TYPING INDICATOR
  // ========================================
  function showTyping() {
    if (isFirstMessage) {
      removeEmptyState();
      isFirstMessage = false;
    }

    const loader = document.createElement("div");
    loader.id = "typing-indicator";
    loader.className = "typing";
    loader.innerHTML = `<span></span><span></span><span></span>`;
    chatWindow.appendChild(loader);
    
    setTimeout(() => {
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 50);
  }

  function hideTyping() {
    const e = document.getElementById("typing-indicator");
    if (e) {
      e.style.animation = 'fadeOut 0.2s ease';
      setTimeout(() => e.remove(), 200);
    }
  }

  // ========================================
  // HIGHLIGHT RETRIEVED CHUNKS IN ARTICLE
  // ========================================
  function highlightChunks(chunks) {
    const article = document.querySelector("article");
    if (!article) return;

    // Remove old highlights
    const oldMarks = article.querySelectorAll("mark.mediumpilot-highlight");
    oldMarks.forEach(mark => {
      const parent = mark.parentNode;
      parent.replaceChild(document.createTextNode(mark.innerText), mark);
      parent.normalize();
    });

    // Get fresh HTML
    let html = article.innerHTML;

    // Add new highlights
    chunks.forEach((text) => {
      const safe = text.trim();
      if (!safe || safe.length < 10) return;

      const escaped = safe.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const regex = new RegExp(escaped, "gi");

      html = html.replace(
        regex,
        (match) => `<mark class="mediumpilot-highlight">${match}</mark>`
      );
    });

    article.innerHTML = html;

    // Scroll to first highlight
    setTimeout(() => {
      const firstHighlight = document.querySelector("mark.mediumpilot-highlight");
      if (firstHighlight) {
        firstHighlight.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
      }
    }, 300);
  }

  // ========================================
  // FORMAT ANSWER
  // ========================================
  function renderAnswer(answerObj) {
    const { answer_title, answer } = answerObj;

    return `
      <div class="answer-container">
        <div class="answer-title">${answer_title}</div>
        <div class="answer-body">${answer}</div>
      </div>
    `;
  }

  // ========================================
  // SEND MESSAGE TO BACKEND
  // ========================================
  sendBtn.onclick = async () => {
    const text = input.value.trim();
    if (!text) return;

    // Add user message
    addMessage("user", text);
    
    // Clear input and reset height
    input.value = "";
    input.style.height = 'auto';
    
    // Show typing indicator
    showTyping();

    // Prepare payload
    const payload =
      MODE === "ask_document"
        ? {
            mode: "ask_document",
            question: text,
            article_url: location.href,
          }
        : { 
            mode: "ask_selected", 
            question: text, 
            snippet: selectedSnippet 
          };

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      hideTyping();

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      const html = renderAnswer(data.answer);
      addMessage("ai", html);

      // Highlight context in article
      if (data.answer.used_chunks && data.answer.used_chunks.length > 0) {
        highlightChunks(data.answer.used_chunks);
      }

    } catch (e) {
      hideTyping();
      addMessage("ai", `
        <div class="answer-container">
          <div class="answer-title" style="color: #DC2626;">⚠️ Connection Error</div>
          <div class="answer-body">
            Unable to reach the backend server. Please ensure it's running at 
            <code>http://127.0.0.1:8000</code>
          </div>
        </div>
      `);
    }
  };
}

// ========================================
// FADE OUT ANIMATION FOR CLEANUP
// ========================================
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    from { opacity: 1; transform: scale(1); }
    to { opacity: 0; transform: scale(0.95); }
  }
`;
document.head.appendChild(style);