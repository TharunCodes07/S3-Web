'use client';

import styles from './page.module.css';
import Link  from 'next/link';

function Home() {
    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <h1 className={styles.title}>Welcome to the AI Revolution</h1>
                <p className={styles.subtitle}>Explore, Learn, and Build with the Power of AI</p>
            </header>
            <div className={styles.tagline}>
                <p>Empowering the future with AI 🌐</p>
            </div>
            <section className={styles.features}>
                <Link href="/verdict" className={`${styles.featureCard} ${styles.link}`}>
                    <h2>AI Tool 1</h2>
                    <p>Explore cutting-edge AI tools designed for Gen Z.</p>
                </Link>
                <Link href="/respira" className={`${styles.featureCard} ${styles.link}`}>
                    <h2>AI Tool 2</h2>
                    <p>Dive into AI resources tailored for creators and innovators.</p>
                </Link>
                <Link href="/learnscope" className={`${styles.featureCard} ${styles.link}`}>
                    <h2>AI Tool 3</h2>
                    <p>Start building and experimenting with your AI ideas today.</p>
                </Link>
            </section>
        </div>
    );
}

export default Home;
