"use client"; // This is a client component 👈🏽

import { useState, useEffect, useRef, FormEvent, ChangeEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faSyncAlt, faRepeat, faSearch, faChartBar, faUserTie } from '@fortawesome/free-solid-svg-icons';
import { faThumbsUp as faThumbsUpRegular, faThumbsDown as faThumbsDownRegular, faCopy, faShareFromSquare } from '@fortawesome/free-regular-svg-icons';
import { faThumbsUp as faThumbsUpSolid, faThumbsDown as faThumbsDownSolid } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/chatBot.module.css'
import { fetchStats, sharelink, likeUnlikeStats } from '../lib/api'
import MarkdownRenderer from './MarkdownRenderer';
import MascotSVG from '../../../public/mascot_cropped.svg'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Message } from '../types/Message';
import { v4 as uuidv4 } from 'uuid';

type ShareLinkInfo = {
    link: string;
    createdAt: number;
};

const ChatContainer: React.FC = () => {
    const storedMessages = sessionStorage.getItem('chatMessages');
    const storedSessionId = sessionStorage.getItem('sessionId');

    //generate a new sessionid - uuid if not present
    const sessionId = storedSessionId || uuidv4();
    if (!storedSessionId) {
        sessionStorage.setItem('sessionId', sessionId);
    }

    const shareLinkInfo = sessionStorage.getItem('shareLink') ? JSON.parse(sessionStorage.getItem('shareLink') as string) as ShareLinkInfo : null;

    const [messages, setMessages] = useState<Message[]>(storedMessages ? JSON.parse(storedMessages) : []);
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

    useEffect(() => {
        sessionStorage.setItem('chatMessages', JSON.stringify(messages));
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
                toast.success('link copied to clipboard', {
                    autoClose: 1000,
                });
                return;
            }

            const link = await sharelink(sessionId, messages);

            sessionStorage.setItem('shareLink', JSON.stringify({ link, createdAt: Date.now() }));

            await navigator.clipboard.writeText(link);

            toast.success('link copied to clipboard', {
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
        setMessages([]); // Example: Clears messages
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
                        {messages.sort(a => a.timestamp).map((message, index) => (
                            <div
                                key={index}
                                className={
                                    message.role === "assistant" ? styles.serverMessage : styles.userMessage
                                }
                            >
                                <div>
                                    {message.role === 'assistant' ? (
                                        <img src="/mascot_cropped.ico" alt="System Icon" className={styles.icon} />
                                    ) : (<></>)}
                                </div>

                                <div className={styles.messageContent}>
                                    {message.role === 'assistant' ? (
                                        <div className={styles.markdownWrapper}>
                                            <MarkdownRenderer content={message.content} />
                                            <div className={styles.actionIcons}>
                                                {[
                                                    { icon: message.isliked ? faThumbsUpSolid : faThumbsUpRegular, label: "Like", action: () => handleLikeOrDislike(index, true) },
                                                    { icon: message.isdisliked ? faThumbsDownSolid : faThumbsDownRegular, label: "Dislike", action: () => handleLikeOrDislike(index, false) },
                                                    { icon: faCopy, label: "Copy", action: () => copyToClipboard(message.content) },
                                                ].map((btn, idx) => (
                                                    <div key={idx} className={styles.tooltipContainer}>
                                                        <button className={styles.iconButton} onClick={btn.action} aria-label={btn.label}>
                                                            <FontAwesomeIcon icon={btn.icon} />
                                                        </button>
                                                        <span className={styles.tooltipText}>{btn.label}</span>
                                                    </div>
                                                ))}
                                                {index === messages.length - 1 && (
                                                    [
                                                        { icon: faShareFromSquare, label: "Create link", action: () => handleShare() },
                                                        { icon: faRepeat, label: "Retry", action: () => handleRetry() },
                                                    ].map((btn: { icon: any, label: string, action: () => void }, idx: number) => (
                                                        <div key={idx} className={styles.tooltipContainer}>
                                                            <button className={styles.iconButton} onClick={btn.action} aria-label={btn.label}>
                                                                <FontAwesomeIcon icon={btn.icon} />
                                                            </button>
                                                            <span className={styles.tooltipText}>{btn.label}</span>
                                                        </div>
                                                    ))
                                                )}
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