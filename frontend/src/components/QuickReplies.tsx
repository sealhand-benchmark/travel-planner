
import React from 'react';

interface QuickRepliesProps {
  options: string[];
  onSelect: (option: string) => void;
}

const QuickReplies: React.FC<QuickRepliesProps> = ({ options, onSelect }) => {
  return (
    <div className="flex flex-wrap gap-2 mb-4 animate-fade-in">
      {options.map((option, index) => (
        <button
          key={index}
          onClick={() => onSelect(option)}
          className="quick-reply-btn"
        >
          {option}
        </button>
      ))}
    </div>
  );
};

export default QuickReplies;
