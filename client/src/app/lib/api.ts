type Message = {
    role: 'user' | 'system';
    content: string;
};

// api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/stats';

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
        // Fetch stats from the API using post call
        const response = await fetch(API_URL, {
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