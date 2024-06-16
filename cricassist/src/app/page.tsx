"use client"; // This is a client component 👈🏽

import { useState, useEffect, useRef, FormEvent, ChangeEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRobot, faUser, faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import styles from './styles/ChatBot.module.css';
import { fetchStats } from './lib/api';
import MarkdownRenderer from './components/MarkdownRenderer';

type Message = {
  text: string;
  sender: 'user' | 'server';
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);   // Track server typing status
  const chatWindowRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTo({
        top: chatWindowRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isTyping]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setInput('');
      
      setIsTyping(true);  // Server starts typing

      try {
        const markdownContent = await fetchStats(input, messages.map(message => message.text));
        setMessages(prevMessages => [
          ...prevMessages,
          { text: markdownContent, sender: 'server' },
        ]);
      } catch (error) {
        setMessages(prevMessages => [
          ...prevMessages,
          { text: 'Failed to fetch content', sender: 'server' },
        ]);
      } finally {
        setIsTyping(false);  // Server stops typing
      }
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatWindow} ref={chatWindowRef}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={
              message.sender === 'server' ? styles.serverMessage : styles.userMessage
            }
          >
            <FontAwesomeIcon
              icon={message.sender === 'server' ? faRobot : faUser}
              className={styles.icon}
            />
            <div className={styles.messageContent}>
              {message.sender === 'server' ? (
                <MarkdownRenderer content={message.text} />
              ) : (
                message.text
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className={styles.serverMessage}>
            <FontAwesomeIcon icon={faRobot} className={styles.icon} />
            <div className={styles.typingIndicator}>
              <div className={styles.typingBubble}></div>
              <div className={styles.typingBubble}></div>
              <div className={styles.typingBubble}></div>
            </div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className={styles.inputForm}>
        <div className={styles.inputWrapper}>
          <input
            type="text"
            value={input}
            onChange={handleChange}
            className={styles.inputField}
            placeholder="Type your message..."
          />
          <button type="submit" className={styles.sendButton}>
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </div>
      </form>
    </div>
  );
}