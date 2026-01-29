const input = document.querySelector(".chat-input");
const sendBtn = document.querySelector(".send-btn");
const chatContainer = document.querySelector(".chat-container");
const toggleAudioBtn = document.getElementById("toggle-audio");

let audioEnabled = false;  
let bgmStarted = false;

const bgm = new Audio("/static/audio/backsound-animenya.mp3");
bgm.volume = 0.35;
bgm.loop = true;

function playBGM() {
    if (!audioEnabled) return;

    bgm.play().catch(() => {});
}

toggleAudioBtn.textContent = "🔇";

toggleAudioBtn.addEventListener("click", () => {
    audioEnabled = !audioEnabled;

    bgm.muted = !audioEnabled;

    toggleAudioBtn.textContent = audioEnabled ? "🔊" : "🔇";

    if (audioEnabled) {
        if (!bgmStarted) {
            bgmStarted = true;
            bgm.volume = 0;
            playBGM();

            // fade in
            let vol = 0;
            const fade = setInterval(() => {
                if (vol < 0.35) {
                    vol += 0.02;
                    bgm.volume = vol;
                } else {
                    clearInterval(fade);
                }
            }, 120);
        } else {
            bgm.play().catch(() => {});
        }
    } else {
        bgm.pause();
    }
});

function typeBotMessage(fullText, wrapper) {
    const bubble = wrapper.querySelector(".bubble-left");
    let i = 0;
    const speed = 15;

    const formattedText = fullText
        .replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

    function typing() {
        if (i < formattedText.length) {
            bubble.innerHTML = formattedText.slice(0, i + 1);
            i++;
            setTimeout(typing, speed);
        }
    }

    typing();
}

function addMessage(text, side = "right", withTyping = false) {
    const wrapper = document.createElement("div");
    wrapper.classList.add(side === "right" ? "msg-right" : "msg-left");

    if (side === "left") {
        const avatar = document.createElement("img");
        avatar.src = "/static/Image/elaina-profil.jpg";
        avatar.classList.add("msg-avatar");
        wrapper.appendChild(avatar);
    }

    const bubble = document.createElement("div");
    bubble.classList.add(side === "right" ? "bubble-right" : "bubble-left");

    if (side === "right" || !withTyping) {
        bubble.innerHTML = text.replace(/\n/g, "<br>");
    }

    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    if (side === "left" && withTyping) {
        typeBotMessage(text, wrapper);
    }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "right");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => addMessage(data.reply, "left", true))
    .catch(() => addMessage("Server error 😵‍💫", "left", true));
}

document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        bgm.pause();
    } else if (bgmStarted && audioEnabled) {
        bgm.play().catch(() => {});
    }
});

document.addEventListener("DOMContentLoaded", () => {
    addMessage("Hi, aku Elaina. Ada yang bisa aku bantu?", "left", true);
});

const bgVideo = document.querySelector(".bg-video");

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    bgVideo.pause();
  } else {
    bgVideo.play().catch(() => {});
  }
});

const texts = [
  "Welcome to Elaina’s World",
  "Elaina Bot",
  "Let’s Chat"
];

const typingEl = document.getElementById("typing-text");

let textIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typingSpeed = 90;
const deletingSpeed = 50;
const delayAfterType = 1500;

function typeEffect() {
  const currentText = texts[textIndex];

  if (!isDeleting) {
    typingEl.textContent = currentText.slice(0, charIndex + 1);
    charIndex++;

    if (charIndex === currentText.length) {
      setTimeout(() => (isDeleting = true), delayAfterType);
    }
  } else {
    typingEl.textContent = currentText.slice(0, charIndex - 1);
    charIndex--;

    if (charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % texts.length;
    }
  }

  setTimeout(
    typeEffect,
    isDeleting ? deletingSpeed : typingSpeed
  );
}

typeEffect();

