const API_URL = 'http://127.0.0.1:8000/stats';

export async function fetchStats(query: string, history: string[] | null): Promise<string> {
    try {
        // Fetch stats from the API using post call
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "query": query,
                "history": history
            }),
        });
        
        // Parse JSON
        const data = await response.json();
        
        // Return data
        return data["summary"];
    } catch (error) {
      throw new Error('Failed to fetch joke');
    }
  };