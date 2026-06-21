const FORM_SUBMIT_ENDPOINT = "https://formsubmit.co/ajax/lekhtembhare@gmail.com";
const DESTINATION_EMAIL = "lekhtembhare@gmail.com";

const form = document.getElementById("registrationForm");
const statusEl = document.getElementById("formStatus");
const popup = document.getElementById("successPopup");
const popupMessage = document.getElementById("popupMessage");
const closePopup = document.getElementById("closePopup");

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

const particles = document.getElementById("particles");
if (particles) {
  for (let i = 0; i < 45; i += 1) {
    const particle = document.createElement("span");
    const size = Math.random() * 6 + 3;
    const duration = Math.random() * 20 + 10;
    particle.style.setProperty("--size", `${size}px`);
    particle.style.setProperty("--duration", `${duration}s`);
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.opacity = `${Math.random() * 0.6 + 0.2}`;
    particles.appendChild(particle);
  }
}

if (window.lucide) {
  lucide.createIcons();
}

const sendToFormSubmit = async (formData) => {
  const response = await fetch(FORM_SUBMIT_ENDPOINT, {
    method: "POST",
    headers: { Accept: "application/json" },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Form submission failed.");
  }

  return response.json().catch(() => ({}));
};

const showPopup = (message) => {
  if (!popup || !popupMessage) {
    return;
  }

  popupMessage.textContent = message;
  popup.classList.add("show");
  popup.setAttribute("aria-hidden", "false");
};

if (closePopup && popup) {
  closePopup.addEventListener("click", () => {
    popup.classList.remove("show");
    popup.setAttribute("aria-hidden", "true");
  });
}

const buildMailtoUrl = (payload) => {
  const lines = [
    "New registration details:",
    "",
    `Full Name: ${payload.fullName || ""}`,
    `Mobile: ${payload.mobile || ""}`,
    `Email: ${payload.email || ""}`,
    `Address: ${payload.address || ""}`,
    `College: ${payload.college || ""}`,
    `University: ${payload.university || ""}`,
    `Track: ${payload.track || ""}`,
    `Semester: ${payload.semester || ""}`,
    `Branch: ${payload.branch || ""}`,
  ];

  const subject = encodeURIComponent("New Registration - CodeX");
  const body = encodeURIComponent(lines.join("\n"));
  return `mailto:${DESTINATION_EMAIL}?subject=${subject}&body=${body}`;
};

const seatProgress = document.querySelector(".seat-progress");
if (seatProgress) {
  const filled = Number(seatProgress.dataset.filled || 0);
  const total = Number(seatProgress.dataset.total || 0);
  const percent = total ? Math.min((filled / total) * 100, 100) : 0;
  const bar = seatProgress.querySelector(".seat-bar span");
  const label = seatProgress.querySelector(".seat-label");

  if (label && total) {
    label.textContent = `${filled} / ${total} seats filled`;
  }

  if (bar) {
    bar.style.width = "0%";
    requestAnimationFrame(() => {
      bar.style.width = `${percent}%`;
    });
  }
}

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (statusEl) {
      statusEl.textContent = "Sending...";
    }

    const formData = new FormData(form);
    const payload = {};
    formData.forEach((value, key) => {
      payload[key] = value;
    });

    if (!form.checkValidity()) {
      if (statusEl) {
        statusEl.textContent = "Please fill all required fields correctly.";
      }
      form.reportValidity();
      return;
    }

    try {
      formData.append("_subject", "New Registration - CodeX");
      formData.append("_template", "table");
      formData.append("_captcha", "false");

      await sendToFormSubmit(formData);
      if (statusEl) {
        statusEl.textContent = "Submission sent successfully.";
      }
      form.reset();
      showPopup("Thanks! Our team will contact you soon.");
    } catch (error) {
      if (statusEl) {
        statusEl.textContent = "Email service unreachable. Opening email draft...";
      }
      window.location.href = buildMailtoUrl(payload);
    }
  });
}

const chatbot = document.getElementById("chatbot");
if (chatbot) {
  const toggleBtn = chatbot.querySelector(".chatbot-toggle");
  const panel = chatbot.querySelector(".chatbot-panel");
  const closeBtn = chatbot.querySelector(".chatbot-close");
  const messages = chatbot.querySelector(".chatbot-messages");
  const chatbotForm = chatbot.querySelector(".chatbot-form");
  const input = chatbot.querySelector(".chatbot-input");
  const quickButtons = chatbot.querySelectorAll(".chatbot-quick button");

  const state = { lang: "en" };

  const responses = {
    en: {
      greet:
        "Hi! I can help with our services and courses. Ask about courses, interview prep, resume guidance, or contact info.",
      services:
        "Our services include AI interview prep, mock interviews, resume guidance, AI career assistance, real industry projects, AI tools learning, industry-level mentorship, online classes, hands-on training, and job-ready portfolio support. Courses: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting.",
      courses:
        "Courses: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting.",
      contact:
        "Contact: +91 8766787283, +91 9529783209, or email lekhtembhare@gmail.com. WhatsApp: +91 8766787283, +91 9529783209.",
      fallback:
        "I can explain courses, interview prep, resume guidance, or contact info. What would you like to know?",
    },
    hi: {
      greet:
        "नमस्ते! मैं CodeX सहायक हूं। आप कोर्स, इंटरव्यू प्रेप, रिज़्यूमे गाइडेंस या संपर्क के बारे में पूछ सकते हैं।",
      services:
        "हमारी सेवाएं: AI इंटरव्यू तैयारी, मॉक इंटरव्यू, रिज़्यूमे गाइडेंस, AI करियर असिस्टेंस, रियल इंडस्ट्री प्रोजेक्ट्स, AI टूल्स लर्निंग, इंडस्ट्री-लेवल मेंटरशिप, ऑनलाइन क्लासेस, हैंड्स-ऑन ट्रेनिंग और जॉब-रेडी पोर्टफोलियो सपोर्ट। कोर्स: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting।",
      courses:
        "कोर्स: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting।",
      contact:
        "संपर्क: +91 8766787283, +91 9529783209 या ईमेल lekhtembhare@gmail.com. WhatsApp: +91 8766787283, +91 9529783209.",
      fallback:
        "मैं कोर्स, इंटरव्यू प्रेप, रिज़्यूमे गाइडेंस या संपर्क की जानकारी बता सकता हूं। आप क्या जानना चाहते हैं?",
    },
    mr: {
      greet:
        "नमस्कार! मी CodeX सहाय्यक आहे. तुम्ही कोर्सेस, इंटरव्ह्यू तयारी, रिझ्युमे मार्गदर्शन किंवा संपर्काबद्दल विचारू शकता.",
      services:
        "आमच्या सेवा: AI इंटरव्ह्यू तयारी, मॉक इंटरव्ह्यू, रिझ्युमे मार्गदर्शन, AI करिअर सहाय्य, रिअल इंडस्ट्री प्रोजेक्ट्स, AI टूल्स लर्निंग, इंडस्ट्री-लेव्हल मेंटॉरशिप, ऑनलाईन क्लासेस, हॅन्ड्स-ऑन ट्रेनिंग आणि जॉब-रेडी पोर्टफोलिओ सपोर्ट. कोर्सेस: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting.",
      courses:
        "कोर्सेस: Web Development, App Development, Data Analytics, Full Stack Development, LLM In Machine Learning, Machine Learning, RAG, AI Consulting.",
      contact:
        "संपर्क: +91 8766787283, +91 9529783209 किंवा ईमेल lekhtembhare@gmail.com. WhatsApp: +91 8766787283, +91 9529783209.",
      fallback:
        "मी कोर्सेस, इंटरव्ह्यू तयारी, रिझ्युमे मार्गदर्शन किंवा संपर्क माहिती सांगू शकतो. तुम्हाला काय माहिती हवी आहे?",
    },
  };

  const marathiHints = ["काय", "कसे", "कुठे", "तुमचे", "तुम्ही", "आहे", "आहात", "मला", "मी", "हवे", "हवी", "नमस्कार"];
  const hindiHints = ["क्या", "कैसे", "कहाँ", "आप", "है", "हैं", "मुझे", "कृपया", "धन्यवाद", "नमस्ते"];
  const devanagariRegex = /[\u0900-\u097F]/;

  const detectLanguage = (text) => {
    const lower = text.toLowerCase();
    if (lower.includes("marathi")) {
      return "mr";
    }
    if (lower.includes("hindi")) {
      return "hi";
    }
    if (lower.includes("english")) {
      return "en";
    }
    if (devanagariRegex.test(text)) {
      const isMarathi = marathiHints.some((hint) => text.includes(hint));
      const isHindi = hindiHints.some((hint) => text.includes(hint));
      if (isMarathi && !isHindi) {
        return "mr";
      }
      return "hi";
    }
    return "en";
  };

  const getIntent = (text) => {
    if (/\b(hi|hello|hey)\b/i.test(text) || /नमस्ते|नमस्कार/.test(text)) {
      return "greet";
    }
    if (/service|services|सेवा|सेवाएं|सेवा|सेवे/i.test(text)) {
      return "services";
    }
    if (/course|courses|कोर्स|कोर्सेस/i.test(text)) {
      return "courses";
    }
    if (/bridge\s?ai|bridgeai|ब्रिज/i.test(text)) {
      return "services";
    }
    if (/interview|resume|portfolio|career|इंटरव्यू|रिज़्यूमे|रेज्यूमे|करियर/i.test(text)) {
      return "services";
    }
    if (/contact|call|phone|whatsapp|email|संपर्क|फोन|कॉल|व्हाट्सएप|ईमेल/i.test(text)) {
      return "contact";
    }
    return "fallback";
  };

  const addMessage = (text, role) => {
    if (!messages) {
      return;
    }
    const bubble = document.createElement("div");
    bubble.classList.add("chatbot-msg", role);
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  };

  const setOpen = (open) => {
    if (!panel || !toggleBtn) {
      return;
    }
    panel.classList.toggle("open", open);
    panel.setAttribute("aria-hidden", open ? "false" : "true");
    toggleBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open && input) {
      input.focus();
    }
  };

  const respondTo = (text, intentOverride, langOverride) => {
    const lang = langOverride || detectLanguage(text);
    state.lang = lang;
    const intent = intentOverride || getIntent(text);
    const reply = responses[lang][intent] || responses[lang].fallback;
    addMessage(reply, "bot");
  };

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = panel && panel.classList.contains("open");
      setOpen(!isOpen);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      setOpen(false);
    });
  }

  if (chatbotForm && input) {
    chatbotForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const value = input.value.trim();
      if (!value) {
        return;
      }
      addMessage(value, "user");
      respondTo(value);
      input.value = "";
    });
  }

  quickButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const intent = button.dataset.intent;
      const label = button.textContent.trim();
      addMessage(label, "user");
      respondTo(label, intent, state.lang);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && panel && panel.classList.contains("open")) {
      setOpen(false);
    }
  });

  addMessage(responses.en.greet, "bot");
}
