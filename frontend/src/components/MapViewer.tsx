
import React, { useEffect, useRef, useState } from 'react';
import { X, MapPin, Navigation } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface MapViewerProps {
  isOpen: boolean;
  onClose: () => void;
  location: {
    name: string;
    address?: string;
    lat?: number;
    lng?: number;
  };
}

const MapViewer: React.FC<MapViewerProps> = ({ isOpen, onClose, location }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const [mapError, setMapError] = useState(false);

  useEffect(() => {
    if (!isOpen || !mapRef.current) return;

    // Kakao Map API would be implemented here
    // For now, we'll show a placeholder with the location info
    console.log('지도 API 연동 준비:', location);
  }, [isOpen, location]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-4xl h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-full">
              <MapPin className="w-4 h-4 text-secondary" />
            </div>
            <div>
              <h3 className="font-semibold text-secondary">{location.name}</h3>
              {location.address && (
                <p className="text-sm text-secondary-500">{location.address}</p>
              )}
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="rounded-full"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Map Container */}
        <div className="flex-1 relative">
          <div 
            ref={mapRef}
            className="absolute inset-0 bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center"
          >
            {mapError ? (
              <div className="text-center">
                <MapPin className="w-16 h-16 text-secondary-300 mx-auto mb-4" />
                <p className="text-secondary-500">지도를 불러올 수 없습니다</p>
              </div>
            ) : (
              <div className="text-center">
                <div className="relative">
                  <div className="w-32 h-32 bg-primary rounded-full mx-auto mb-4 flex items-center justify-center">
                    <Navigation className="w-16 h-16 text-secondary" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-4 h-4 bg-red-500 rounded-full animate-pulse"></div>
                </div>
                <h4 className="text-lg font-semibold text-secondary mb-2">{location.name}</h4>
                <p className="text-secondary-600 mb-4">
                  카카오 지도 API 연동 예정
                </p>
                <div className="bg-white rounded-lg p-4 shadow-sm inline-block">
                  <p className="text-sm text-secondary-500">
                    좌표: {location.lat || '37.5665'}, {location.lng || '126.9780'}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200">
          <div className="flex justify-between items-center">
            <Button variant="outline" className="rounded-lg">
              길찾기
            </Button>
            <Button 
              onClick={onClose}
              className="bg-primary hover:bg-primary-500 text-secondary rounded-lg"
            >
              닫기
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapViewer;