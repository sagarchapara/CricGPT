"use client"; // This is a client component 👈🏽

import { useState, useEffect, useRef, FormEvent, ChangeEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRobot, faUser, faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/chatBot.module.css'
import { fetchStats } from '../lib/api'
import MarkdownRenderer from './MarkdownRenderer';

type Message = {
    content: string;
    role: "system" | "user";
    errorText?: boolean;
};

const initMessages: Message[] = [
    {
        content: 'Hello! I am a bot. How can I help you today?', role: 'system'
    },
    {
        content: 'What can I assist you with?', role: 'system'
    },
    {
        content: 'Please provide more details.', role: 'system'
    },
    {
        content: 'I am here to help you with any questions.', role: 'system'
    },
    {
        content: 'Hi, I need help with my account.', role: 'user'
    },
    {
        content: 'Can you tell me more about your services?', role: 'user'
    },
    {
        content: 'I am having trouble logging in.', role: 'user'
    },
    {
        content: 'Thank you for your assistance.', role: 'user'
    },
    {
        content: 'Can you tell me more about your services?', role: 'user'
    },
    {
        content: 'I am having trouble logging in.', role: 'user'
    },
    {
        content: 'Thank you for your assistance.', role: 'user'
    },
    {
        content: 'I am having trouble logging in.', role: 'user'
    },
    {
        content: 'Thank you for your assistance.', role: 'system'
    }
];

const ChatContainer: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>(initMessages);
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
            setMessages([...messages, { content: input, role: 'user' }]);
            setInput('');

            setIsTyping(true);  // Server starts typing

            try {
                const markdownContent = await fetchStats(input, getHistory(messages));
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: markdownContent, role: "system" },
                ]);
            } catch (error) {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: 'Failed to fetch content', role: 'system', errorText: true },
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
                            message.role === 'system' ? styles.serverMessage : styles.userMessage
                        }
                    >
                        <FontAwesomeIcon
                            icon={message.role === 'system' ? faRobot : faUser}
                            className={styles.icon}
                        />
                        <div className={styles.messageContent}>
                            {message.role === 'system' ? (
                                <MarkdownRenderer content={message.content} />
                            ) : (
                                message.content
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

function getHistory(messages: Message[]): Message[] {
    return messages.filter((message) => message.errorText !== true)
}

export default ChatContainer;