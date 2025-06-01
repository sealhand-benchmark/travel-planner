
import React from 'react';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  isTyping?: boolean;
  timestamp?: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ 
  message, 
  isUser, 
  isTyping = false,
  timestamp 
}) => {
  return (
    <div className={`flex gap-3 mb-4 animate-fade-in ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-primary' : 'bg-secondary'
      }`}>
        {isUser ? (
          <User className="w-4 h-4 text-secondary" />
        ) : (
          <Bot className="w-4 h-4 text-primary" />
        )}
      </div>
      
      {/* Message bubble */}
      <div className={`chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}`}>
        {isTyping ? (
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-secondary-400 rounded-full animate-typing"></div>
            <div className="w-2 h-2 bg-secondary-400 rounded-full animate-typing" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-secondary-400 rounded-full animate-typing" style={{ animationDelay: '0.4s' }}></div>
          </div>
        ) : (
          <div>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
            {timestamp && (
              <p className={`text-xs mt-1 ${isUser ? 'text-secondary-600' : 'text-secondary-400'}`}>
                {timestamp}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
