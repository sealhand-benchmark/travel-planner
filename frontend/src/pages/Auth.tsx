import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plane, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const Auth = () => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // 환경변수에서 인증키 확인
    if (password === import.meta.env.VITE_AUTH_PASSWORD) {
      localStorage.setItem('travel-auth', 'authenticated');
      navigate('/');
    } else {
      console.warn('인증키가 올바르지 않습니다.');
      setError('인증키가 올바르지 않습니다.');
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-white p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-primary-100">
          {/* Logo */}
          <div className="flex items-center justify-center mb-8">
            <div className="flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
              <Plane className="w-8 h-8 text-secondary" />
            </div>
          </div>
          
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-secondary mb-2">일정짜기귀차나</h1>
            <p className="text-secondary-500">AI 여행 계획 어시스턴트</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium text-secondary-700">
                인증키
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="인증키를 입력하세요"
                  className="pl-10 h-12 rounded-xl border-secondary-200 focus:border-primary focus:ring-primary"
                  required
                />
              </div>
              {error && (
                <p className="text-sm text-red-500 mt-2">{error}</p>
              )}
            </div>

            <Button
              type="submit"
              disabled={isLoading || !password.trim()}
              className="w-full h-12 bg-primary hover:bg-primary-500 text-secondary rounded-xl font-medium"
            >
              {isLoading ? '인증 중...' : '서비스 시작하기'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Auth;