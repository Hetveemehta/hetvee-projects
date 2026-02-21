// COMMON DOM refs
const video = document.getElementById("video");
const countdownEl = document.getElementById("countdown");
const startBtn = document.getElementById("startBtn");
const liveStrip = document.getElementById("liveStrip");
const overlay = document.getElementById("overlay");
const retakeBtn = document.getElementById("retakeBtn");
const continueBtn = document.getElementById("continueBtn");

// MOBILE toggles
const stripToggle = document.getElementById("stripToggle");
const editToggleBtn = document.getElementById("editToggleBtn");
const controlPanel = document.getElementById("controlPanel");
const closePanelBtn = document.getElementById("closePanelBtn");

// =============================================
// CAMERA BOOTH
// =============================================
if (video) {
  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "user" } })
    .then(stream => {
      video.srcObject = stream;
      video.play().catch(() => { });
    })
    .catch(() => alert("Camera access denied 😭"));
}

if (startBtn) {
  startBtn.addEventListener("click", async () => {
    if (!video || !liveStrip || !countdownEl) return;

    const photos = [];
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = 720;
    canvas.height = 540;

    // intro message
    countdownEl.textContent = "okay!! smileeeee";
    await new Promise(r => setTimeout(r, 1500));

    for (let i = 0; i < 4; i++) {
      for (let j = 3; j > 0; j--) {
        countdownEl.textContent = j;
        await new Promise(r => setTimeout(r, 700));
      }
      countdownEl.textContent = "";

      if (i === 0) document.getElementById("liveStrip")?.classList.remove("hidden-strip");

      ctx.save();
      ctx.scale(-1, 1);
      ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
      ctx.restore();

      const photoData = canvas.toDataURL("image/png");
      photos.push(photoData);

      const wrapper = document.createElement("div");
      wrapper.className = "thumb-wrap";
      const thumb = document.createElement("img");
      thumb.src = photoData;
      setTimeout(() => thumb.classList.add("visible"), 20);
      wrapper.appendChild(thumb);
      liveStrip.appendChild(wrapper);

      await new Promise(r => setTimeout(r, 500));
    }

    localStorage.setItem("photos", JSON.stringify(photos));
    overlay.classList.remove("hidden");
  });
}

// Overlay buttons
if (retakeBtn) {
  retakeBtn.addEventListener("click", () => {
    localStorage.removeItem("photos");
    overlay.classList.add("hidden");
    liveStrip.innerHTML = "";
  });
}
if (continueBtn) {
  continueBtn.addEventListener("click", () => {
    document.body.style.transition = "opacity 0.35s ease";
    document.body.style.opacity = "0";
    setTimeout(() => (window.location.href = "editor.html"), 350);
  });
}

// =============================================
// EDITOR PAGE
// =============================================
(function setupEditor() {
  const editorStrip = document.getElementById("editorStrip");
  if (!editorStrip) return;

  const photos = JSON.parse(localStorage.getItem("photos")) || [];
  editorStrip.innerHTML = "";
  photos.forEach(src => {
    const img = document.createElement("img");
    img.src = src;
    editorStrip.appendChild(img);
  });

  // APPLY / REMOVE bottom text — no default watermark
const bottomInput = document.getElementById('bottomTextInput');
const applyBtn = document.getElementById('applyBottomText');
const removeBtn = document.getElementById('removeBottomText');

function getStrip() {
  return document.getElementById('editorStrip');
}

if (applyBtn && bottomInput) {
  applyBtn.addEventListener('click', () => {
    const strip = getStrip();
    if (!strip) return;

    const text = bottomInput.value.trim();

    if (text.length === 0) {
      // empty input -> remove any footer
      strip.removeAttribute('data-bottom-text');
      strip.classList.remove('bottom-design');
      return;
    }

    strip.setAttribute('data-bottom-text', text);
    strip.classList.add('bottom-design');
  });
}

if (removeBtn) {
  removeBtn.addEventListener('click', () => {
    const strip = getStrip();
    if (!strip) return;

    strip.removeAttribute('data-bottom-text');
    strip.classList.remove('bottom-design');
    if (bottomInput) bottomInput.value = '';
  });
}


  // filter controls
  document.querySelectorAll(".filter-controls button").forEach(btn => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter;
      editorStrip.querySelectorAll("img").forEach(img => {
        img.classList.remove("filter-bw", "filter-warm", "filter-cool", "filter-grain");
        if (filter !== "none") img.classList.add(`filter-${filter}`);
      });
    });
  });

  // frame controls
  document.querySelectorAll(".color-dot").forEach(dot => {
    dot.addEventListener("click", () => {
      const color = dot.dataset.frame;
      editorStrip.className = `photo-strip-vertical ${color} bottom-design`;
    });
  });

  // Download button
  const downloadBtn = document.getElementById("downloadStripBtn");
  if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {
      html2canvas(editorStrip, { scale: 2, backgroundColor: null }).then(canvas => {
        const link = document.createElement("a");
        const date = new Date().toISOString().split("T")[0];
        link.download = `INDIGO_${date}.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
      });
    });
  }
})();

// =============================================
// ================= MOBILE EDITOR PANEL =================
const openEditorBtn = document.getElementById("openEditorBtn");
const mobilePanel = document.getElementById("mobileEditorPanel");
const closeMobilePanel = document.getElementById("closeMobilePanel");

if (openEditorBtn && mobilePanel && closeMobilePanel) {
  openEditorBtn.addEventListener("click", () => {
    mobilePanel.classList.add("open");
  });

  closeMobilePanel.addEventListener("click", () => {
    mobilePanel.classList.remove("open");
  });
}
// ✅ custom bottom text input (FIXED + NO DEFAULT WATERMARK)
const bottomInput = document.getElementById("bottomTextInput");
const applyBottomText = document.getElementById("applyBottomText");
const removeBottomText = document.getElementById("removeBottomText");

if (bottomInput && applyBottomText) {
  applyBottomText.addEventListener("click", () => {
    const strip = document.getElementById("editorStrip");
    const text = bottomInput.value.trim();

    if (!strip) return;

    if (text) {
      strip.dataset.bottomText = text;
      strip.classList.add("bottom-design");
    } else {
      // if user clicks apply with empty input, just remove any text instead of forcing default
      strip.removeAttribute("data-bottom-text");
      strip.classList.remove("bottom-design");
    }
  });
}

if (removeBottomText) {
  removeBottomText.addEventListener("click", () => {
    const strip = document.getElementById("editorStrip");
    if (!strip) return;

    strip.removeAttribute("data-bottom-text");
    strip.classList.remove("bottom-design");
    bottomInput.value = "";
  });
}
