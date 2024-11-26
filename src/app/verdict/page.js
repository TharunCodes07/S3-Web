'use client';

import { useEffect, useState } from "react";
import styles from './page.module.css';

const Role = {
  USER: "User",
  BOT: "Bot"
};

function Chatbot() {
  const [chats, setChats] = useState([
    { role: Role.BOT, text: 'Hello there! How may I help you today?' }
  ]);
  const [text, setText] = useState('');
  const [waiting, setWaiting] = useState(false);

  const userResponse = (text) => {
    setChats((previousChat) => [...previousChat, { role: Role.USER, text: text }]);
  };

  const botResponse = (text) => {
    setChats((previousChat) => [...previousChat, { role: Role.BOT, text: text }]);
  };

  const fetchData = async () => {
    const query_text = chats[chats.length - 1].text;
    const requestBody = {
      query: query_text
    };
    const response = await fetch('http://192.168.193.222:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    if (!response.ok) {
      console.error('Response status:', response.status);
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data.response;
  };

  const onSend = async () => {
    if (!text) return;
    userResponse(text);
    setWaiting(true);
    setText('');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSend();
    }
  };

  useEffect(() => {
    const handleBotResponse = async () => {
      if (waiting) {
        try {
          const data = await fetchData();
          botResponse(data);
        } catch (error) {
          console.error(error);
          botResponse("I'm sorry, I'm encountering an error. Please try again later.");
        } finally {
          setWaiting(false);
        }
      }
    };
    handleBotResponse();
  }, [waiting]);

  return (
    <div className={styles.chatContainer}>
      <h4 className={styles.chatTitle}>VERDICTIQ</h4>
      <div className={styles.chatBox}>
        {chats.map((chat, index) => (
          <div
            key={index}
            className={chat.role === Role.USER ? styles.userMessage : styles.botMessage}
          >
            {chat.text}
          </div>
        ))}
        {waiting && (
          <div className={styles.botMessage}>
            <div className={styles.loadingDots}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>
      <div className={styles.inputContainer}>
        <textarea
          className={styles.textInput}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          rows={2}
        />
        <button className={styles.sendButton} onClick={onSend}>➤</button>
      </div>
    </div>
  );
}

export default Chatbot;
