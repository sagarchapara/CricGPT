import ChatContainer from './components/ChatContainer';
import styles from './styles/home.module.css';


export default function Home() {

  return (
    <div className={styles.container}>
      <div className={styles.main}>
        <ChatContainer />
      </div>
    </div>
  );
}
