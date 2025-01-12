"use client"; // This is a client component 👈🏽

import { useState, useEffect, useRef, FormEvent, ChangeEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faSyncAlt, faRepeat, faSearch, faChartBar, faUserTie } from '@fortawesome/free-solid-svg-icons';
import { faCopy } from '@fortawesome/free-regular-svg-icons';
import styles from '../styles/chatBot.module.css'
import { fetchStats, sharelink, likeUnlikeStats } from '../lib/api'
import MascotSVG from '../../../public/mascot_cropped.svg'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Message } from '../types/Message';
import { v4 as uuidv4 } from 'uuid';
import MessageContainer from './MessageContainer';

type ShareLinkInfo = {
    link: string;
    createdAt: number;
};

type ChatContainerProps = {
    initialMessages?: Message[];
}

const ChatContainer: React.FC<ChatContainerProps> = ({ }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [sessionId, setSessionId] = useState<string>('');
    const [shareLinkInfo, setShareLinkInfo] = useState<ShareLinkInfo | null>(null);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);   // Track server typing status
    const chatWindowRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Initialize messages and sessionId from sessionStorage
        const storedMessages = sessionStorage.getItem('chatMessages');
        const storedSessionId = sessionStorage.getItem('sessionId');
        const storedShareLink = sessionStorage.getItem('shareLink');

        if (storedMessages) {
            setMessages(JSON.parse(storedMessages)); // Restore messages
        }

        const newSessionId = storedSessionId || uuidv4();
        setSessionId(newSessionId);

        if (!storedSessionId) {
            sessionStorage.setItem('sessionId', newSessionId);
        }

        if (storedShareLink) {
            setShareLinkInfo(JSON.parse(storedShareLink));
        }
    }, []);


    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTo({
                top: chatWindowRef.current.scrollHeight,
                behavior: 'smooth',
            });
        }
    }, [messages, isTyping]);

    useEffect(() => {
        if (messages.length > 0) {
            sessionStorage.setItem('chatMessages', JSON.stringify(messages));
        }
    }, [messages]);


    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            setMessages([...messages, { content: input, role: 'user', timestamp: Date.now() }]);
            setInput('');

            setIsTyping(true);  // Server starts typing

            try {
                const markdownContent = await fetchStats(input, getHistory(messages));
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: markdownContent, role: "assistant", timestamp: Date.now() },
                ]);
            } catch (error) {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: 'Something went wrong try again', role: 'assistant', errorText: true, timestamp: Date.now() },
                ]);
            } finally {
                setIsTyping(false);  // Server stops typing
            }
        }
    };

    const handleLikeOrDislike = async (messageIndex: number, isLike: boolean): Promise<void> => {
        // Logic to like or dislike a message
        if (messages.length === 0) {
            return;
        }

        if (messages[messageIndex] && (messages[messageIndex].isliked === true) && isLike === true) {
            console.info("Already liked");
            return;
        }

        if (messages[messageIndex] && (messages[messageIndex].isdisliked === true) && isLike === false) {
            console.info("Already disliked");
            return;
        }

        const updatedMessages = messages.map((msg, idx) =>
            idx === messageIndex ? { ...msg, isliked: isLike, isdisliked: !isLike } : msg
        );

        setMessages(updatedMessages);

        try {
            await likeUnlikeStats(sessionId, updatedMessages);
        } catch (error) {
            console.error('Failed to like or dislike', error);
            toast.error('Failed to like or dislike', {
                autoClose: 1000,
            });
        }
    };

    const handleShare = async (): Promise<void> => {

        try {
            if (shareLinkInfo && messages[messages.length - 1].timestamp < shareLinkInfo.createdAt) {
                await navigator.clipboard.writeText(shareLinkInfo.link);
                toast.success('Link copied to clipboard', {
                    autoClose: 1000,
                });
                return;
            }

            const link = await sharelink(sessionId, messages);

            sessionStorage.setItem('shareLink', JSON.stringify({ link, createdAt: Date.now() }));

            await navigator.clipboard.writeText(link);

            toast.success('Link copied to clipboard', {
                autoClose: 1000,
            });
        } catch (error) {
            console.error('Failed to share', error);
            toast.error('Failed to create link', {
                autoClose: 1000,
            });
        }
    }

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleRefresh = () => {
        // Logic to refresh chat
        //remove the session id and messages from session storage
        sessionStorage.removeItem('sessionId');
        sessionStorage.removeItem('chatMessages');
        sessionStorage.removeItem('shareLink');

        setMessages([]); // Clears messages
        setSessionId(uuidv4()); // Generates new session
        setShareLinkInfo(null); // Clears share link info
    };

    const copyToClipboard = async (content: string): Promise<void> => {
        try {
            await navigator.clipboard.writeText(content);

            toast.success('Content copied to clipboard', {
                autoClose: 1000,
            });
        } catch (err) {
            console.error('Failed to copy to clipboard', err);
            toast.error('Failed to copy to clipboard', {
                autoClose: 1000,
            });
        }
    };

    const handleRetry = async (): Promise<void> => {
        // logic to regenerate the last message
        setMessages(messages.slice(0, -1)); // Remove the last message
        const lastMessage = messages[messages.length - 2]; // Get the second last message
        setIsTyping(true);  // Server starts typing

        if (lastMessage) {
            try {
                const markdownContent = await fetchStats(lastMessage.content, getHistory(messages.slice(0, -1)));
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: markdownContent, role: "assistant", timestamp: Date.now() },
                ]);
            } catch (error) {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { content: 'Something went wrong try again', role: 'assistant', errorText: true, timestamp: Date.now() },
                ]);
            } finally {
                setIsTyping(false);  // Server stops typing
            }
        }
    };



    return (
        <div className={styles.chatContainer}>
            <ToastContainer />
            {messages.length === 0 ? (
                <div className={styles.emptyState}>
                    <MascotSVG />
                    <p className={styles.emptyStateText}>Ask anything about cricket!</p>
                </div>
            ) : (
                <>
                    <div className={styles.chatWindow} ref={chatWindowRef}>
                        {messages.sort((a) => a.timestamp).map((message, index) => (
                            <MessageContainer
                                key={index}
                                message={message}
                                isLastMessage={index === messages.length - 1}
                                onLikeOrDislike={(isLike) => handleLikeOrDislike(index, isLike)}
                                onCopy={() => copyToClipboard(message.content)}
                                onShare={index === messages.length - 1 ? handleShare : undefined}
                                onRetry={index === messages.length - 1 ? handleRetry : undefined}
                            />
                        ))}
                        {isTyping && (
                            <div className={styles.serverMessage}>
                                <img
                                    src="/mascot_cropped.svg"
                                    alt="System Icon"
                                    className={styles.icon}
                                />
                                <div className={styles.typingIndicator}>
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
                        { icon: faCopy, title: "Custom Queries", description: "Ask custom questions about cricket.", comingSoon: false },
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