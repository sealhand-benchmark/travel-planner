
import React from 'react';
import { CheckCircle, Circle, MapPin, Calendar, Users, Heart } from 'lucide-react';

interface PlanProgressProps {
  completedSteps: string[];
  currentStep: string;
}

const PlanProgress: React.FC<PlanProgressProps> = ({ completedSteps, currentStep }) => {
  const steps = [
    { id: 'companions', label: '동행자', icon: Users },
    { id: 'style', label: '여행 스타일', icon: Heart },
    { id: 'destination', label: '여행지', icon: MapPin },
    { id: 'dates', label: '일정', icon: Calendar },
  ];

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-primary-200 mb-4">
      <h3 className="text-sm font-medium text-secondary-600 mb-3">여행 계획 진행상황</h3>
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isCompleted = completedSteps.includes(step.id);
          const isCurrent = currentStep === step.id;
          const Icon = step.icon;
          
          return (
            <div key={step.id} className="flex flex-col items-center">
              <div className={`relative flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all ${
                isCompleted 
                  ? 'bg-primary border-primary' 
                  : isCurrent 
                    ? 'border-primary bg-primary-50' 
                    : 'border-gray-300 bg-gray-50'
              }`}>
                {isCompleted ? (
                  <CheckCircle className="w-4 h-4 text-secondary" />
                ) : (
                  <Icon className={`w-4 h-4 ${isCurrent ? 'text-primary-600' : 'text-gray-400'}`} />
                )}
              </div>
              <span className={`text-xs mt-1 ${
                isCompleted || isCurrent ? 'text-secondary-600 font-medium' : 'text-gray-400'
              }`}>
                {step.label}
              </span>
              {index < steps.length - 1 && (
                <div className={`absolute top-4 left-full w-8 h-0.5 ${
                  completedSteps.includes(steps[index + 1].id) ? 'bg-primary' : 'bg-gray-300'
                }`} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PlanProgress;
