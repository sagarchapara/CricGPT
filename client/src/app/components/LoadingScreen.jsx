import React from 'react';
import styles from '../styles/loadingscreen.module.css'; // Import our CSS module

function LoadingScreen({ loading }) {
    // Don't render if `loading` is false
    if (!loading) return null;

    return (
        <div className={styles.overlay}>
            <div className={styles.loaderContainer}>
                <div className={styles.spinner}>
                    {/* Note how we're combining multiple classes using template literals */}
                    <div className={`${styles.bounce} ${styles.bounce1}`} />
                    <div className={`${styles.bounce} ${styles.bounce2}`} />
                    <div className={`${styles.bounce} ${styles.bounce3}`} />
                </div>
                <p className={styles.loadingText}>Loading, please wait...</p>
            </div>
        </div>
    );
}

export default LoadingScreen;
