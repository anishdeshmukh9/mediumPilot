/*************************************
 * Inject Sidebar Into Medium Page
 *************************************/
const sidebarUrl = chrome.runtime.getURL("sidebar.html");
fetch(sidebarUrl)
  .then((res) => res.text())
  .then((html) => {
    const wrapper = document.createElement("div");
    wrapper.id = "mec-sidebar-wrapper";
    wrapper.innerHTML = html;
    document.body.appendChild(wrapper);

    const script = document.createElement("script");
    script.src = chrome.runtime.getURL("sidebar.js");
    document.body.appendChild(script);

    // ========================================
    // CRITICAL: ISOLATE SIDEBAR SCROLLING
    // ========================================
    setTimeout(() => {
      const sidebar = document.getElementById("mec-sidebar-wrapper");
      if (sidebar) {
        // Prevent all scroll events from bubbling
        sidebar.addEventListener('wheel', (e) => {
          e.stopPropagation();
        }, { capture: true, passive: true });

        sidebar.addEventListener('touchmove', (e) => {
          e.stopPropagation();
        }, { capture: true, passive: true });

        // Prevent mouseenter/mouseover from affecting page scroll
        sidebar.addEventListener('mouseenter', () => {
          document.body.style.overflow = 'hidden';
        });

        sidebar.addEventListener('mouseleave', () => {
          document.body.style.overflow = '';
        });
      }
    }, 100);
  });


/*************************************
 * TEXT SELECTION HANDLER
 *************************************/
document.addEventListener("mouseup", () => {
  const sel = window.getSelection().toString().trim();
  if (sel.length > 0) {
    window.postMessage({ type: "MEC_SELECTED_TEXT", text: sel });
  }
});


/*************************************
 * EXTRACT FULL ARTICLE CONTENT
 *************************************/
function extractFullArticle() {
  const articleRoot =
    document.querySelector("article") ||
    document.querySelector(".meteredContent") ||
    document.body;

  return articleRoot.innerText;
}


/*************************************
 * AUTO-SEND ARTICLE TO BACKEND (ONCE)
 *************************************/
let articleSent = false;

function sendArticleToBackend() {
  if (articleSent) return;

  const text = extractFullArticle();
  const url = location.href;

  console.log("MEC: Sending article to backend...");

  fetch("http://127.0.0.1:8000/index-article", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      article_url: url,
      article_content: text
    })
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("MEC: Article indexed:", data);
      window.postMessage({ type: "MEC_ARTICLE_INDEXED", data });
    })
    .catch((err) => console.error("MEC: Index error:", err));

  articleSent = true;
}


/*************************************
 * WAIT FOR PAGE TO RENDER THEN SEND
 *************************************/
setTimeout(sendArticleToBackend, 1500);


/*************************************
 * Also send article content to sidebar.js
 *************************************/
setTimeout(() => {
  window.postMessage({
    type: "MEC_ARTICLE_CONTENT",
    text: extractFullArticle()
  });
}, 1800);