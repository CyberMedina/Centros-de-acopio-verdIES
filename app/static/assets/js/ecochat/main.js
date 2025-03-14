const containerEcochat = document.querySelector(".container-ecochat");
const chatbotToggler = document.querySelector(".chatbot-icon");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable para almacenar el mensaje del usuario
const inputInitHeight = chatInput.scrollHeight;

// URL de la API local (Flask)
const API_URL = "http://127.0.0.1:5000/api/ecochat";

// Función para crear los elementos <li> de los mensajes
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="bx bx-leaf"></span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = message;  // Cambia textContent a innerHTML
    return chatLi;
}


// Guardar el mensaje en el localStorage
const addMessageToLocalStorage = (message, className) => {
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    chatHistory.push({ message, className });
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// Cargar historial del chat desde localStorage
const loadChatHistory = () => {
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    chatHistory.forEach(chat => {
        chatbox.appendChild(createChatLi(chat.message, chat.className));
    });
    chatbox.scrollTo(0, chatbox.scrollHeight);  // Desplazar hacia el final
}

// Generar respuesta del bot y actualizar el localStorage
const generateResponse = async (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: userMessage
        }),
    }

    try {
        const response = await fetch(API_URL, requestOptions);
        const data = await response.json();

        if (!response.ok) {
            if (response.status === 403) {
                messageElement.textContent = data.error;
                sendChatBtn.disabled = true;
                chatInput.disabled = true;
            } else {
                throw new Error(data.error);
            }
        } else {
            let botReply = data.reply;
            const currentCount = data.current_count;
            const totalMessages = data.total_messages;

            const formattedReply = botReply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            const finalFormattedReply = formattedReply.replace(/(\d+\.\s)<strong>(.*?)<\/strong>/g, '<strong>$1$2</strong>');

            messageElement.innerHTML = `${finalFormattedReply}<br><text class="mt-2 badge bg-label-info">${currentCount} de ${totalMessages}</text>`;

            // Agregar la respuesta del bot al localStorage
            addMessageToLocalStorage(messageElement.innerHTML, "incoming");
        }
    } catch (error) {
        messageElement.classList.add("error");
        messageElement.textContent = "Error en la comunicación con el servidor.";
    } finally {
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
}

// Manejar el envío de mensajes
const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Añadir el mensaje del usuario al chatbox y localStorage
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    addMessageToLocalStorage(userMessage, "outgoing");
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

// Ajustar la altura del textarea
chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Enviar mensaje con Enter
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// Enviar mensaje con el botón
sendChatBtn.addEventListener("click", handleChat);

// Cargar historial al abrir el chatbot
chatbotToggler.addEventListener("click", () => {
    document.body.classList.toggle("show-chatbot");
    containerEcochat.style.display = "none";
    loadChatHistory();  // Cargar historial al abrir el chat
});

// Cerrar el chat
closeBtn.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
    containerEcochat.style.display = "block";
});
