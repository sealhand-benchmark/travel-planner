import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plane, Sparkles, LogOut, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import ChatMessage from '@/components/ChatMessage';
import QuickReplies from '@/components/QuickReplies';
import PlanProgress from '@/components/PlanProgress';
import ChatInput from '@/components/ChatInput';
import MapViewer from '@/components/MapViewer';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: string;
  quickReplies?: string[];
}

interface SessionResponse {
  session_id: string;
  session_created_at: string;
}

const Index = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: '안녕하세요! 여행 계획을 세우는 게 번거로우셨죠?🎉\n저와 함께 대화하면서 완벽한 여행 계획을 만들어 보세요!\n\n누구와 함께 가시나요?',
      isUser: false,
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
      quickReplies: ['혼자', '연인과 함께', '가족과 함께', '친구들과 함께']
    }
  ]);
  
  const [isTyping, setIsTyping] = useState(false);
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState('companions');
  const [mapViewer, setMapViewer] = useState<{
    isOpen: boolean;
    location: { name: string; address?: string; lat?: number; lng?: number; };
  }>({
    isOpen: false,
    location: { name: '' }
  });
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // 컴포넌트 마운트 시 세션 ID 생성
    const initializeSession = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/chat/session_id', {
          method: 'POST',
        });
        const data: SessionResponse = await response.json();
        setSessionId(data.session_id);
      } catch (error) {
        console.error('세션 초기화 실패:', error);
      }
    };

    initializeSession();

    // 컴포넌트 언마운트 시 EventSource 정리
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('travel-auth');
    navigate('/auth');
  };

  const handleGeneratePlan = () => {
    const planId = `plan-${Date.now()}`;
    navigate(`/plan/${planId}`);
  };

  const handleSendMessage = async (content: string) => {
    if (content === '계획서 보기') {
      handleGeneratePlan();
      return;
    }

    if (!sessionId) {
      console.error('세션 ID가 없습니다.');
      return;
    }

    const newMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, newMessage]);
    setIsTyping(true);

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const eventSource = new EventSource(
      `http://localhost:8000/api/chat/response/${sessionId}?user_input=${encodeURIComponent(content)}`
    );
    eventSourceRef.current = eventSource;

    let assistantMessageId = `ai-${Date.now()}`;
    let accumulatedContent = '';

    eventSource.onmessage = (event) => {
      try {
          const data = JSON.parse(event.data);
          
          console.log("data", data);

        if (data.error) {
          console.error('에러 발생:', data.error);
          return;
        }

        // chunk 누적
        accumulatedContent += data.message;
        console.log(accumulatedContent);

        setMessages(prev => {
          // 마지막 메시지가 assistant(=isUser: false)이고, id가 assistantMessageId면 이어붙임
          if (
            prev.length > 0 &&
            !prev[prev.length - 1].isUser &&
            prev[prev.length - 1].id === assistantMessageId
          ) {
            // 마지막 assistant 메시지 업데이트
            const updated = [...prev];
            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              content: accumulatedContent,
            };
            return updated;
          } else {
            // 새 assistant 메시지 추가
            return [
              ...prev,
              {
                id: assistantMessageId,
                content: accumulatedContent,
                isUser: false,
                timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
              },
            ];
          }
        });
      } catch (error) {
        console.error('메시지 처리 중 에러:', error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource 에러:', error);
      eventSource.close();
      setIsTyping(false);
    };

    eventSource.addEventListener('end', () => {
      eventSource.close();
      setIsTyping(false);
    });
  };

  const handleQuickReply = (option: string) => {
    handleSendMessage(option);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-primary-200 px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-full">
              <Plane className="w-5 h-5 text-secondary" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-secondary">일정짜기귀차나</h1>
              <p className="text-xs text-secondary-500">AI 여행 계획 어시스턴트</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm text-secondary-600">온라인</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              className="rounded-lg"
            >
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <div className="flex-1 max-w-4xl mx-auto w-full flex flex-col">
        {/* Progress Bar */}
        <div className="p-4">
          {/* <PlanProgress completedSteps={completedSteps} currentStep={currentStep} /> */}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 pb-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div key={message.id}>
                <ChatMessage
                  message={message.content}
                  isUser={message.isUser}
                  timestamp={message.timestamp}
                />
                {message.quickReplies && !message.isUser && (
                  <QuickReplies
                    options={message.quickReplies}
                    onSelect={handleSendMessage}
                  />
                )}
              </div>
            ))}
            
            {isTyping && (
              <ChatMessage
                message=""
                isUser={false}
                isTyping={true}
              />
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isTyping}
          placeholder="여행 계획에 대해 말씀해 주세요..."
        />
      </div>

      {/* Map Viewer Modal */}
      <MapViewer
        isOpen={mapViewer.isOpen}
        onClose={() => setMapViewer(prev => ({ ...prev, isOpen: false }))}
        location={mapViewer.location}
      />
    </div>
  );
};

export default Index;