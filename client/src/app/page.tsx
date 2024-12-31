"use client"; // This is a client component 👈🏽

import { useState } from 'react';

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ChatContainer from './components/ChatContainer';
import styles from './styles/home.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <div className={styles.main}>
        <ChatContainer />
      </div>
      <footer className={styles.footer}>
        <p>© {new Date().getFullYear()} CricStatsAI. All rights reserved.</p>
      </footer>
    </div>
  );
}
