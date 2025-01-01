"use client"; // This is a client component 👈🏽

import { fetchMessages } from '@/app/lib/api';
import { Message } from '@/app/types/Message';
import MessageContainer from '../../components/MessageContainer';
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import LoadingScreen from '@/app/components/LoadingScreen';

interface ChatPageProps {
    params: { id: string };
}

export default function ChatPage({ params }: ChatPageProps) {
    const { id } = params;
    const router = useRouter();
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                // Fetch messages or other data for this ID
                const fetchedMessages = await fetchMessages(id);
                setMessages(fetchedMessages);
            } catch (error) {
                console.error('Failed to fetch messages', error);
                setMessages([]);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    if (loading) {
        return (
            <LoadingScreen loading={true} />
        );
    }

    return (
        <>
            {(!messages || messages.length === 0) ? (
                <div
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100vh',
                    }}
                >
                    <img
                        src="/mascot_cropped.svg"
                        alt="Logo"
                        style={{
                            width: '200px',
                            height: '200px',
                            marginBottom: '20px',
                        }}
                    />
                    <h1 style={{ color: '#555' }}>
                        Oops! The chat you're looking for could not be found.
                    </h1>
                </div>
            ) : (
                <div>
                    <div style={{ padding: '10%' }}>
                        {messages.map((message: Message, index: number) => (
                            <MessageContainer
                                key={index}
                                message={message}
                                isLastMessage={index === messages.length - 1}
                                onLikeOrDislike={() => { }}
                                onCopy={() => { }}
                                onShare={() => { }}
                                onRetry={() => { }}
                                showIcons={false}
                            />
                        ))}
                    </div>
                </div>
            )}
        </>
    );
};
