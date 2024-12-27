"use client"; // This is a client component 👈🏽

import { useState, useEffect, useRef, FormEvent, ChangeEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faSyncAlt, faClipboard, faThumbsUp, faThumbsDown, faShareAlt, faSearch, faChartBar, faUserTie } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/chatBot.module.css'
import { fetchStats } from '../lib/api'
import MarkdownRenderer from './MarkdownRenderer';
import MascotSVG from '../../../public/mascot_cropped.svg'

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

    const handleRefresh = () => {
        // Logic to refresh chat
        setMessages([]); // Example: Clears messages
    };

    const copyToClipboard = async (content: string): Promise<void> => {
        try {
            await navigator.clipboard.writeText(content);
            alert('Content copied to clipboard!');
        } catch (err) {
            alert('Failed to copy content: ' + (err as Error).message);
        }
    };



    return (
        <div className={styles.chatContainer}>
            {messages.length === 0 ? (
                <div className={styles.emptyState}>
                    <MascotSVG />
                    <p className={styles.emptyStateText}>Ask anything about cricket!</p>
                </div>
            ) : (
                <>
                    <div className={styles.chatWindow} ref={chatWindowRef}>
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={
                                    message.role === 'system' ? styles.serverMessage : styles.userMessage
                                }
                            >
                                <div>
                                    {message.role === 'system' ? (
                                        <img src="/mascot_cropped.ico" alt="System Icon" className={styles.icon} />
                                    ) : (<></>)}
                                </div>

                                <div className={styles.messageContent}>
                                    {message.role === 'system' ? (
                                        <div className={styles.markdownWrapper}>
                                            <MarkdownRenderer content={message.content} />
                                            <div className={styles.actionIcons}>
                                                <div className={styles.tooltipContainer}>
                                                    <button className={styles.iconButton} onClick={() => alert('Liked!')} aria-label="Like">
                                                        <FontAwesomeIcon icon={faThumbsUp} />
                                                    </button>
                                                    <span className={styles.tooltipText}>Like</span>
                                                </div>
                                                <div className={styles.tooltipContainer}>
                                                    <button className={styles.iconButton} onClick={() => alert('Disliked!')} aria-label="Dislike">
                                                        <FontAwesomeIcon icon={faThumbsDown} />
                                                    </button>
                                                    <span className={styles.tooltipText}>Dislike</span>
                                                </div>
                                                <div className={styles.tooltipContainer}>
                                                    <button className={styles.iconButton} onClick={() => alert('Shared!')} aria-label="Share">
                                                        <FontAwesomeIcon icon={faShareAlt} />
                                                    </button>
                                                    <span className={styles.tooltipText}>Share</span>
                                                </div>
                                                <div className={styles.tooltipContainer}>
                                                    <button className={styles.iconButton} onClick={() => copyToClipboard(message.content)} aria-label="Copy">
                                                        <FontAwesomeIcon icon={faClipboard} />
                                                    </button>
                                                    <span className={styles.tooltipText}>Copy</span>
                                                </div>
                                            </div>
                                        </div>
                                    ) : (
                                        <div>{message.content}</div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {isTyping && (
                            <div className={styles.serverMessage}>
                                <img src="/mascot_cropped.ico" alt="System Icon" className={styles.icon} />                                <div className={styles.typingIndicator}>
                                    <div className={styles.typingBubble}></div>
                                    <div className={styles.typingBubble}></div>
                                    <div className={styles.typingBubble}></div>
                                </div>
                            </div>
                        )}
                    </div>
                </>
            )}

            <div className="flex-1 w-full">
                <form onSubmit={handleSubmit} className={styles.inputForm}>
                    <div className={styles.inputWrapper}>
                        <input
                            type="text"
                            value={input}
                            onChange={handleChange}
                            className={styles.inputField}
                            placeholder="Start asking..."
                        />
                        <div className={styles.tooltipContainer}>
                            <button type="submit" className={styles.sendButton} title="Submit">
                                <FontAwesomeIcon icon={faPaperPlane} />
                            </button>
                            <span className={styles.tooltipText}>Submit</span>
                        </div>
                        {/* Add Refresh Button */}
                        <div className={styles.tooltipContainer}>
                            <button
                                type="button"
                                onClick={handleRefresh}
                                className={styles.refreshButton}
                                aria-label="Refresh Chat"
                            >
                                <FontAwesomeIcon icon={faSyncAlt} />
                            </button>
                            <span className={styles.tooltipText}>Refresh Chat</span>
                        </div>

                    </div>
                </form>
            </div>
            {messages.length == 0 ? (
                <div className={styles.featuresRow}>
                    {[
                        { icon: faSearch, title: "Search Stats", description: "Find detailed player statistics.", comingSoon: false },
                        { icon: faClipboard, title: "Custom Queries", description: "Ask custom questions about cricket.", comingSoon: false },
                        { icon: faChartBar, title: "Plot Stats", description: "Visualize data with interactive charts.", comingSoon: true },
                        { icon: faUserTie, title: "Player Analysis", description: "In-depth player performance insights.", comingSoon: true },
                    ].map((feature, index) => (
                        <div
                            key={index}
                            className={`${styles.featureBlock} ${feature.comingSoon ? styles.comingSoon : ""}`}
                        >
                            <FontAwesomeIcon icon={feature.icon} className={styles.featureIcon} />
                            <h3 className={styles.featureTitle}>{feature.title}</h3>
                            <p className={styles.featureDescription}>{feature.description}</p>
                            {feature.comingSoon && <div className={styles.comingSoonBadge}>Coming Soon</div>}
                        </div>
                    ))}
                </div>

            ) : (<></>)}
        </div>
    );
}

function getHistory(messages: Message[]): Message[] {
    return messages.filter((message) => message.errorText !== true)
}

export default ChatContainer;