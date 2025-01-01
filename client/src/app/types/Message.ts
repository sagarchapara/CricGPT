export type Message = {
    content: string;
    role: "assistant" | "user";
    timestamp: number;
    errorText?: boolean;
    isliked?: boolean;
    isdisliked?: boolean;
};