# [서비스명] 일정짜기귀차나

### 서비스 아키텍쳐
>docker-compose.yml

현재는 저장된 데이터에 대해서 Embedding하거나 Vector-Search가 필요없기에 VectorDB는 구성 중 제거
다만, Config성으로 활용할 수 있는 여지를 위해 pgvector로써 PostgreSQL 배포

- **backend**(FastAPI)
- **redis** - Config등 자주 호출되는 정보, ChatMemory에 대한 캐싱용도
- **postgresql** - 대화내역 및 State 저장 및 Config 관리

### AWS Deploy
- EC2 docker-compose 기반 배포


### AI개발 도구 활용 내역
1. Curesor - IDE
: 코드 작성 어시스턴트 용도로 활용
2. Lovable
: 필요 구현부분을 기술하여 프론트엔드 및 UI 부분 초안 생성

### Tool Architecture 상세
- 카카오 지도 API 연결
- 카카오 캘린더 연동


(LangGraph 및 LangChain을 사용하지 않고 개밯하다보니 LangGraph에 기반한 MultiAgent 챗봇시스템은 최종적으로 구현하지 못하였습니다. 참고부탁드립니다.)




