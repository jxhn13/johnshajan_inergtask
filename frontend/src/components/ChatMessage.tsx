import React from 'react';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
    role: 'user' | 'assistant';
    content: string;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ role, content }) => {
    const isUser = role === 'user';

    return (
        <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-3`}>

         
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${isUser ? 'bg-blue-600 text-white' : 'bg-emerald-600 text-white'
                    }`}>
                    {isUser ? <User size={18} /> : <Bot size={18} />}
                </div>

                <div className={`p-4 rounded-2xl shadow-sm border ${isUser
                        ? 'bg-blue-600 text-white rounded-tr-none border-blue-600'
                        : 'bg-white text-slate-800 rounded-tl-none border-slate-200'
                    }`}>
                    <div className="text-sm leading-relaxed whitespace-pre-wrap">
                        {content}
                    </div>
                </div>

            </div>
        </div>
    );
};
