import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faThumbsUp as faThumbsUpRegular,
    faThumbsDown as faThumbsDownRegular,
    faCopy,
    faShareFromSquare,
} from '@fortawesome/free-regular-svg-icons';
import {
    faThumbsUp as faThumbsUpSolid,
    faThumbsDown as faThumbsDownSolid,
    faRepeat,
} from '@fortawesome/free-solid-svg-icons';
import MarkdownRenderer from './MarkdownRenderer';
import styles from '../styles/chatBot.module.css';
import { Message } from '../types/Message';

type MessageContainerProps = {
    message: Message;
    isLastMessage: boolean;
    onLikeOrDislike: (isLike: boolean) => void;
    onCopy: () => void;
    onShare?: () => void;
    onRetry?: () => void;
    showIcons?: boolean;
};

const MessageContainer: React.FC<MessageContainerProps> = ({
    message,
    isLastMessage,
    onLikeOrDislike,
    onCopy,
    onShare,
    onRetry,
    showIcons = true,
}) => (
    <div
        className={
            message.role === 'assistant' ? styles.serverMessage : styles.userMessage
        }
    >
        <div>
            {message.role === 'assistant' ? (
                <img
                    src="/mascot_cropped.svg"
                    alt="System Icon"
                    className={styles.icon}
                />
            ) : null}
        </div>

        <div className={styles.messageContent}>
            {message.role === 'assistant' ? (
                <div className={styles.markdownWrapper}>
                    <MarkdownRenderer content={message.content} />
                    {showIcons && (
                        <div className={styles.actionIcons}>
                            {[
                                {
                                    icon: message.isliked ? faThumbsUpSolid : faThumbsUpRegular,
                                    label: 'Like',
                                    action: () => onLikeOrDislike(true),
                                },
                                {
                                    icon: message.isdisliked ? faThumbsDownSolid : faThumbsDownRegular,
                                    label: 'Dislike',
                                    action: () => onLikeOrDislike(false),
                                },
                                { icon: faCopy, label: 'Copy', action: onCopy },
                            ].map((btn, idx) => (
                                <div key={idx} className={styles.tooltipContainer}>
                                    <button
                                        className={styles.iconButton}
                                        onClick={btn.action}
                                        aria-label={btn.label}
                                    >
                                        <FontAwesomeIcon icon={btn.icon} />
                                    </button>
                                    <span className={styles.tooltipText}>{btn.label}</span>
                                </div>
                            ))}
                            {isLastMessage && onShare && onRetry && (
                                <>
                                    {[
                                        { icon: faShareFromSquare, label: 'Create link', action: onShare },
                                        { icon: faRepeat, label: 'Retry', action: onRetry },
                                    ].map((btn, idx) => (
                                        <div key={idx} className={styles.tooltipContainer}>
                                            <button
                                                className={styles.iconButton}
                                                onClick={btn.action}
                                                aria-label={btn.label}
                                            >
                                                <FontAwesomeIcon icon={btn.icon} />
                                            </button>
                                            <span className={styles.tooltipText}>{btn.label}</span>
                                        </div>
                                    ))}
                                </>
                            )}
                        </div>
                    )}
                </div>
            ) : (
                <div>{message.content}</div>
            )}
        </div>
    </div>
);

export default MessageContainer;
