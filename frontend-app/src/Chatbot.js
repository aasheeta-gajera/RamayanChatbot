import React, { useState, useRef, useEffect } from "react";
import "./Chatbot.css";

function Chatbot({chat}) {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState(() => {
        // Load messages from localStorage on initial render
        const savedMessages = localStorage.getItem('ramayanChatHistory');
        return savedMessages ? JSON.parse(savedMessages) : [];
    });
    const chatContainerRef = useRef(null);

     useEffect(() => {
    if (chat) {
      setMessages(chat.messages);
    }
  }, [chat]);

    // Save messages to localStorage whenever they change
    useEffect(() => {
        localStorage.setItem('ramayanChatHistory', JSON.stringify(messages));
    }, [messages]);

    // Scroll to bottom when new messages are added
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    async function askChatbot(e) {
        e.preventDefault();
        if (!question.trim()) return;

        // Add user message to chat
        const userMessage = { 
            type: 'user', 
            content: question,
            timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, userMessage]);
        setQuestion("");

        try {
            const response = await fetch("http://127.0.0.1:5000/chatbot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question }),
            });

            if (!response.ok) {
                throw new Error("Unable to fetch answer");
            }

            const data = await response.json();
            // Add bot response to chat
            const botMessage = { 
                type: 'bot', 
                content: data.answer || "No response from chatbot.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = { 
                type: 'bot', 
                content: "Error: Unable to fetch answer.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        }
    }

    const clearHistory = () => {
        if (window.confirm('Are you sure you want to clear the chat history?')) {
            setMessages([]);
            localStorage.removeItem('ramayanChatHistory');
        }
    };

    return (
        <div className="chat-container">
            {/* <div className="chat-header">
                <button onClick={clearHistory} className="clear-button">
                    Clear History
                </button>
            </div> */}
            <div className="chat-messages" ref={chatContainerRef}>
                {messages.length === 0 && (
                    <div className="welcome-message">
                        <h3>Welcome to Ramayan Chat</h3>
                        <p>Ask me anything about the Ramayan, its characters, stories, or teachings.</p>
                    </div>
                )}
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.type}`}>
                        <div className="message-avatar">
                            {message.type === 'bot' ? '🕉️' : '👤'}
                        </div>
                        <div className="message-content">
                            {message.content}
                            <div className="message-timestamp">
                                {new Date(message.timestamp).toLocaleTimeString()}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <form className="chat-input-container" onSubmit={askChatbot}>
                <input 
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask something about Ramayan..."
                    className="chat-input"
                />
                <button type="submit" className="send-button">
                    Send
                </button>
                {/* <button onClick={clearHistory} className="send-button">
    <span className="delete-icon">🗑️</span>
</button> */}

            </form>
        </div>
    );
}

export default Chatbot;

// {
//     "kanda": "Uttara Kanda",
//     "sarga": 1,
//     "shloka": 1,
//     "shloka_text": "प्राप्तराज्यस्य रामस्य राक्षसानां वधे कृते । आजग्मुर्ऋषयः सर्वे राघवं प्रतिनन्दितुम् ।। 7.1.1 ।।",
//     "transliteration": "prāptarājyasya rāmasya rākṣasānāṃ vadhe kṛte | ājagmurṛṣayaḥ sarve rāghavaṃ pratinanditum || 7.1.1 ||",
//     "translation": null,
//     "explanation": null,
//     "comments": null
// },