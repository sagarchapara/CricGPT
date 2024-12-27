import React from 'react';
import MarkdownRenderer from './MarkdownRenderer';
import styles from '../styles/messageComponent.module.css';

interface Message {
    role: 'system' | 'user';
    content: string;
}

interface MessageComponentProps {
    message: Message;
}

const MessageComponent: React.FC<MessageComponentProps> = ({ message }) => {
    const copyToClipboard = async (content: string): Promise<void> => {
        try {
            await navigator.clipboard.writeText(content);
            alert('Content copied to clipboard!');
        } catch (err) {
            alert('Failed to copy content: ' + (err as Error).message);
        }
    };

    return (
        <div className={styles.messageContent}>
            {message.role === 'system' ? (
                <div className={styles.markdownWrapper}>
                    <MarkdownRenderer content={message.content} />
                    <button
                        className={styles.copyButton}
                        onClick={() => copyToClipboard(message.content)}
                    >
                        Copy
                    </button>
                </div>
            ) : (
                <div>{message.content}</div>
            )}
        </div>
    );
};

export default MessageComponent;
