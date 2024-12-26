import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/header.module.css';

export default function Header() {
    return (
        <header className={styles.header}>
            <h2 className={styles.title}>
                CricStatsAI
            </h2>
        </header>
    );
}
