import { FC } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faMagnifyingGlass, faCommentDots, faCog } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/sidebar.module.css';

// Define the type for a single chat history
interface Chat {
    id: string;
    title: string;
}

// Define the props type for Sidebar
interface SidebarProps {
    onCloseSidebar: () => void;
    onNewChat: () => void;
    onSearch: () => void;
    onSettings: () => void;
    chatHistories: Chat[];
    onSelectChat: (id: string) => void;
}

const Sidebar: FC<SidebarProps> = ({
    onCloseSidebar,
    onNewChat,
    onSearch,
    onSettings,
    chatHistories = [{ id: '1', title: 'Chat 1' }, { id: '2', title: 'Chat 2' }],
    onSelectChat,
}) => {
    return (
        <aside className={styles.sidebar}>
            {/* Top Icons */}
            <div className={styles.topIcons}>
                <button onClick={onCloseSidebar} className={styles.iconButton} aria-label="Close Sidebar">
                    <FontAwesomeIcon icon={faChevronLeft} />
                </button>
                <div className={styles.rightIcons}>
                    <button onClick={onSearch} className={styles.iconButton} aria-label="Search">
                        <FontAwesomeIcon icon={faMagnifyingGlass} />
                    </button>
                    <button onClick={onNewChat} className={styles.iconButton} aria-label="New Chat">
                        <FontAwesomeIcon icon={faCommentDots} />
                    </button>
                </div>
            </div>

            {/* Chat Histories */}
            <div className={styles.chatHistory}>
                {chatHistories.map((chat) => (
                    <div
                        key={chat.id}
                        className={styles.chatItem}
                        onClick={() => onSelectChat(chat.id)}
                        role="button"
                    >
                        <FontAwesomeIcon icon={faCommentDots} className={styles.chatIcon} />
                        <span>{chat.title}</span>
                    </div>
                ))}
            </div>

            {/* Footer with Settings */}
            <div className={styles.footer}>
                <button onClick={onSettings} className={styles.settingsButton} aria-label="Settings">
                    <FontAwesomeIcon icon={faCog} />
                    <span className={styles.settingsText}>Settings</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
