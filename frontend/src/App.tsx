import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Sparkles } from 'lucide-react';
import { ChatMessage } from './components/ChatMessage';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

function App() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/query', {
                query: userMessage,
                history: messages.map(msg => ({
                    role: msg.role,
                    content: msg.content
                }))
            });

            const answer = response.data.answer;

            setMessages(prev => [...prev, { role: 'assistant', content: answer }]);
        } catch (error) {
            console.error("Error querying backend:", error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "Sorry, I encountered an error connecting to the server."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="h-screen bg-slate-50 flex flex-col items-center p-4 md:p-8 font-sans overflow-hidden">

            {/* Header */}
            <header className="w-full max-w-4xl flex items-center gap-3 mb-4 shrink-0">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl shadow-lg flex items-center justify-center text-white">
                    <Sparkles size={20} />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Insurance Assistant</h1>
                    <p className="text-slate-500 text-sm">Inerg</p>
                </div>
            </header>

            {/* Chat Container */}
            <main className="w-full max-w-4xl flex-1 bg-white rounded-3xl shadow-xl border border-slate-100 flex flex-col overflow-hidden h-[80vh]">

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-slate-200">
                    {messages.length === 0 && (
                        <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 p-8 opacity-75">
                            <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-4 text-slate-300">
                                <Sparkles size={32} />
                            </div>
                            <h3 className="text-lg font-medium text-slate-600 mb-2">How can I help you?</h3>
                            <p className="max-w-xs text-sm">Ask about insurance policies, coverage details, or claim procedures.</p>
                        </div>
                    )}

                    {messages.map((msg, idx) => (
                        <ChatMessage key={idx} role={msg.role} content={msg.content} />
                    ))}

                    {isLoading && (
                        <div className="flex w-full mb-4 justify-start">
                            <div className="flex max-w-[80%] flex-row items-start gap-3">
                                <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center shrink-0 animate-pulse">
                                    <Sparkles size={18} />
                                </div>
                                <div className="p-4 rounded-2xl bg-white border border-slate-200 rounded-tl-none shadow-sm">
                                    <div className="flex gap-1.5 items-center h-5">
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></span>
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-slate-100 bg-slate-50/50 backdrop-blur-sm">
                    <form onSubmit={handleSubmit} className="relative flex items-center">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question about insurance..."
                            className="w-full pl-5 pr-14 py-4 rounded-xl border border-slate-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-slate-800 placeholder:text-slate-400 bg-white"
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading}
                            className="absolute right-2 p-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-8 text-center text-slate-400 text-xs">
                © 2026 Inerg Insurance AI.
            </footer>
        </div>
    );
}

export default App;
