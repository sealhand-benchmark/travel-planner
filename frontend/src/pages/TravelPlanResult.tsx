
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Share2, Download, Calendar, MapPin, Clock, ArrowRight, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface TravelPlan {
  id: string;
  title: string;
  duration: string;
  destination: string;
  companions: string;
  style: string;
  days: Array<{
    day: number;
    date: string;
    activities: Array<{
      time: string;
      title: string;
      location: string;
      description: string;
      duration: string;
      type: 'attraction' | 'restaurant' | 'accommodation' | 'transport';
    }>;
  }>;
}

const TravelPlanResult = () => {
  const { planId } = useParams();
  const navigate = useNavigate();
  const [shareUrl] = useState(`${window.location.origin}/plan/${planId}`);

  // Mock data - in production this would come from API/database
  const plan: TravelPlan = {
    id: planId || 'demo',
    title: '제주도 힐링 여행',
    duration: '2박 3일',
    destination: '제주도',
    companions: '연인과 함께',
    style: '자연 및 풍경 구경',
    days: [
      {
        day: 1,
        date: '2024년 5월 28일 (화)',
        activities: [
          {
            time: '09:00',
            title: '제주공항 도착',
            location: '제주국제공항',
            description: '렌터카 픽업 후 여행 시작',
            duration: '1시간',
            type: 'transport'
          },
          {
            time: '11:00',
            title: '성산일출봉',
            location: '성산일출봉',
            description: '유네스코 세계자연유산으로 지정된 명소',
            duration: '2시간',
            type: 'attraction'
          },
          {
            time: '13:30',
            title: '성산포 해산물 맛집',
            location: '성산포항 인근',
            description: '신선한 해산물로 점심 식사',
            duration: '1시간',
            type: 'restaurant'
          }
        ]
      },
      {
        day: 2,
        date: '2024년 5월 29일 (수)',
        activities: [
          {
            time: '09:00',
            title: '한라산 국립공원',
            location: '한라산 어리목탐방로',
            description: '제주의 상징 한라산 트레킹',
            duration: '4시간',
            type: 'attraction'
          },
          {
            time: '14:00',
            title: '흑돼지 맛집',
            location: '제주시 연동',
            description: '제주 특산 흑돼지 구이',
            duration: '1시간',
            type: 'restaurant'
          }
        ]
      }
    ]
  };

  const handleShare = async () => {
    if (navigator.share) {
      await navigator.share({
        title: plan.title,
        text: `${plan.duration} ${plan.destination} 여행 계획을 확인해보세요!`,
        url: shareUrl
      });
    } else {
      await navigator.clipboard.writeText(shareUrl);
      alert('링크가 클립보드에 복사되었습니다!');
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'attraction': return <MapPin className="w-4 h-4" />;
      case 'restaurant': return <Calendar className="w-4 h-4" />;
      case 'transport': return <ArrowRight className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'attraction': return 'bg-blue-100 text-blue-600';
      case 'restaurant': return 'bg-green-100 text-green-600';
      case 'transport': return 'bg-gray-100 text-gray-600';
      default: return 'bg-primary-100 text-primary-600';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-primary-200 px-4 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="rounded-lg"
          >
            <Home className="w-4 h-4 mr-2" />
            홈으로
          </Button>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={handleShare}
              className="rounded-lg"
            >
              <Share2 className="w-4 h-4 mr-2" />
              공유하기
            </Button>
            <Button className="bg-primary hover:bg-primary-500 text-secondary rounded-lg">
              <Download className="w-4 h-4 mr-2" />
              다운로드
            </Button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto p-4">
        {/* Plan Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-secondary mb-4">{plan.title}</h1>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-secondary-500">기간:</span>
              <p className="font-medium text-secondary">{plan.duration}</p>
            </div>
            <div>
              <span className="text-secondary-500">목적지:</span>
              <p className="font-medium text-secondary">{plan.destination}</p>
            </div>
            <div>
              <span className="text-secondary-500">동행자:</span>
              <p className="font-medium text-secondary">{plan.companions}</p>
            </div>
            <div>
              <span className="text-secondary-500">스타일:</span>
              <p className="font-medium text-secondary">{plan.style}</p>
            </div>
          </div>
        </div>

        {/* Daily Itinerary */}
        <div className="space-y-6">
          {plan.days.map((day) => (
            <div key={day.day} className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="bg-primary px-6 py-4">
                <h2 className="text-xl font-bold text-secondary">
                  Day {day.day} - {day.date}
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {day.activities.map((activity, index) => (
                    <div key={index} className="flex gap-4 relative">
                      {index < day.activities.length - 1 && (
                        <div className="absolute left-6 top-12 w-0.5 h-16 bg-primary-200"></div>
                      )}
                      <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${getActivityColor(activity.type)}`}>
                        {getActivityIcon(activity.type)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-lg font-semibold text-secondary">{activity.title}</span>
                          <span className="text-sm text-secondary-500">{activity.time}</span>
                          <span className="text-xs bg-secondary-100 text-secondary-600 px-2 py-1 rounded-full">
                            {activity.duration}
                          </span>
                        </div>
                        <p className="text-secondary-600 mb-1">{activity.location}</p>
                        <p className="text-sm text-secondary-500">{activity.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center py-8">
          <p className="text-secondary-400 text-sm">
            일정짜기귀차나 AI가 생성한 여행 계획입니다
          </p>
          <p className="text-secondary-300 text-xs mt-1">
            공유 링크: {shareUrl}
          </p>
        </div>
      </main>
    </div>
  );
};

export default TravelPlanResult;