"use client"; // This is a client component 👈🏽

import { useState } from 'react';

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ChatContainer from './components/ChatContainer';
import styles from './styles/home.module.css';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const onCloseSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className={styles.container}>
      <div className={styles.main}>
        <Header />
        <ChatContainer />
      </div>
    </div>
  );
}
