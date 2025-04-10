import React, { useState } from "react";

function Chatbot() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState(""); // ✅ Defined but not used yet

    async function askChatbot() {
        const response = await fetch("http://127.0.0.1:5000/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            setAnswer("Error: Unable to fetch answer.");
            return;
        }

        const data = await response.json();
        setAnswer(data.answer || "No response from chatbot.");
    }

    return (
        <div>
            <input 
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask something..."
            />
            <button onClick={askChatbot}>Ask</button>
            <p>Answer: {answer}</p> {/* ✅ Now using answer */}
        </div>
    );
}

export default Chatbot;
