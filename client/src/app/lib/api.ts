import { Message } from '../types/Message';

// api.ts
const API_URL = "http://127.0.0.1:8000";

// Type safety for environment
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            NEXT_PUBLIC_API_URL?: string;
        }
    }
}

export async function fetchStats(query: string, history: Message[] | null): Promise<string> {
    try {

        const statsUrl = new URL('/stats', API_URL).toString();

        // Fetch stats from the API using post call
        const response = await fetch(statsUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "query": query,
                "history": history,
            }),
        });

        if (!response.ok) {
            console.error("Failed to fetch stats", response.body);
            throw new Error('Failed to fetch stats');
        }

        // Parse JSON
        const data = await response.json();

        // Return data
        return data["summary"];
    } catch (error) {
        console.error('Failed to fetch stats', error);
        throw error;
    }
};

export async function likeUnlikeStats(sessionId: string, messages: Message[]): Promise<void> {
    try {
        const likeUrl = new URL('/like', API_URL).toString();

        // Fetch stats from the API using post call
        const response = await fetch(likeUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "messages": messages,
                "sessionId": sessionId,
            }),
        });

        if (!response.ok) {
            console.error("Failed to like stats", response.body);
            throw new Error('Failed to like stats');
        }
    } catch (error) {
        console.error('Failed to like stats', error);
        throw error;
    }
};

export async function sharelink(sessionId: string, messages: Message[]): Promise<string> {
    try {
        const shareUrl = new URL('/sharelink', API_URL).toString();

        // Fetch stats from the API using post call
        const response = await fetch(shareUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "sessionId": sessionId,
                "messages": messages
            }),
        });

        if (!response.ok) {
            console.error("Failed to share link", response.body);
            throw new Error('Failed to share link');
        }

        // Parse JSON
        const data = await response.json();
        return data["sharedLink"];

    } catch (error) {
        console.error('Failed to share link', error);
        throw error;
    }
};

export async function fetchMessages(sessionId: string): Promise<Message[]> {
    try {
        const messagesUrl = new URL(`/session/${sessionId}`, API_URL).toString();

        // Fetch stats from the API using post call
        const response = await fetch(messagesUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error("Failed to fetch messages", response.body);
            throw new Error('Failed to fetch messages');
        }

        // Parse JSON
        const data = await response.json();
        return data["messages"];

    } catch (error) {
        console.error('Failed to fetch messages', error);
        throw error;
    }
}