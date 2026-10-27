# 참고 사이트 분석 (2026-10-19)

## 1. 닥터재일치과 (doctorjaeil.com) — 강동구 암사동
- 플랫폼: 아임웹(imweb) 템플릿. 팝업 배너 여러 장, 사이드 플로팅 버튼.
- 색: 진청록 #0D5A65(theme-color), 흰 배경, 회색 글자. 서체 Noto Sans KR.
- title: "강동구치과 닥터재일치과 | 일요일진료 암사동치과 암사역치과 강동구 임플란트" — 지역 키워드 나열형.
- h1: "강동구 닥터재일치과 | 일요일진료, 고난도 임플란트, 매복사랑니, 의식하진정법(수면)치료"
- JSON-LD: Organization + Dentist/MedicalClinic(전화·주소·geo·openingHours) + FAQPage(홈 FAQ와 동일 내용) + ImageObject.
- 홈 구성: 히어로 → "대표원장이 직접 시행하는 의식하진정법" → 전 의료진 전문의 → 6인 전문의 협진 → 칼럼 썸네일 10개 → 진료보증제도 → 인테리어 → FAQ(카테고리 탭 5개, 25문항) → 전화·진료시간 → 푸터.
- 콘텐츠 축: 의식하진정법을 "대표원장이 직접"으로 전면에. 전문의 자격 강조. FAQ를 운영 질문(일요일·야간·직장인·응급) 중심으로 구성 → AI가 "일요일 진료 치과" 질문에 인용하기 좋음.
- 메뉴 구조: 치과소개 / 의식하진정(수면) / 임플란트 / 심미·보철 / 교정 / 사랑니 / 자연치아살리기 / 턱관절·코골이 / 소수술 / 커뮤니티 / 치아정보대백과.
- 주의: "진료보증제도", "안전하게" 같은 단정 표현 다수 → 시화점에는 쓰지 않음.

## 2. 서울비디치과 (bdbddc.com) — 천안 불당동
- 플랫폼: 자체 제작 정적/SSR. 아주 공들인 SEO·GEO 구조.
- 색: 브라운 #6B4226 + 베이지 #C8A97E + 거의 검정 #0A0D13/#1C1917 + 따뜻한 오프화이트 #FBF8F4/#FAFAF9. 서체 Pretendard. 글자 큼(히어로 70px, h2 56px).
- meta: description·keywords·geo.region/geo.position/ICBM·subject·abstract·**ai-summary**·**medical-content**(검토자 명시)·og/twitter 완비·robots max-image-preview:large.
- JSON-LD 8종: Dentist(alternateName·image 3장·geo·hasMap·areaServed 도시 목록·openingHours) / FAQPage(dateModified) / BreadcrumbList / WebSite(SearchAction) / **MedicalWebPage(lastReviewed·reviewedBy 원장 @id·speakable)** / Organization(sameAs 5개·contactPoint availableLanguage·knowsAbout) / SiteNavigationElement / VideoObject / ItemList(진료 카드).
- 홈 구성: 브랜드 스토리 히어로 → "이건 치료 안 하셔도 됩니다"(환자 안심 카피) → 소개 영상+숫자 카드 → 차별점 카드 → 고민별 해결(치과공포·시간·비용·거절·아이) → 진료 카드 6 → 가격 → 지역 섹션(천안·아산 + 지역 FAQ) → 백과사전 가이드 → 치BTI → 층별 안내 → 시설 사진 → 철학 → 리뷰 → 추천 대상 → 오시는 길 → CTA → 원장 칼럼 → 전후 사례 → 푸터.
- 모든 이미지 alt 있음(13/13). 지역 페이지(/area/cheonan, /area/asan) 별도. 치료 페이지 URL이 /treatments/<slug>로 일관.
- 주의: "서울대 출신", "천안 최대 규모", "가장 많이 선택" 등 비교·최상급 표현 많음 → 시화점에는 쓰지 않음.

## 시화점에 가져올 것 (의료법 범위 안에서)
1. **메타·구조화 데이터 세트**: Dentist(+geo, hasMap, areaServed=시흥시·정왕동·안산 일부, openingHours) / Organization(sameAs, contactPoint) / WebSite / BreadcrumbList / FAQPage(화면과 동일) / MedicalWebPage(lastReviewed·reviewedBy=원장) / SiteNavigationElement. geo.* 메타, ai-summary, medical-content 메타도 추가.
2. **운영 질문 중심 FAQ**: 수요일 야간진료, 토요일 진료, 공휴일, 주차, 접수마감, 첫 방문 절차 등 — AI가 "시화 야간진료 치과", "정왕동 토요일 치과" 질문에 인용 가능.
3. **고민별 진입(환자 상황 카드)**: 치과가 무서운 분 / 이가 많이 빠진 분 / 신경치료 받아야 한다는데 / 바쁜 직장인 — 바로드림 시화점의 전문의·의식하진정법·야간진료와 자연스럽게 연결.
4. **지역 섹션**: "시흥 정왕동·시화에서 오시는 분들께" — 성담스퀘어 5층 518호, 주변 랜드마크, 대중교통, 주차.
5. **의료진 바이라인**: 모든 치료 페이지·칼럼 하단에 "이 글은 ○○○ 원장(○○ 전문의)이 검토했습니다" + MedicalWebPage reviewedBy.
6. **치료 페이지 URL 일관성**: /treatments/<slug>.html 또는 루트 slug 일관.
7. **큰 글자·넉넉한 여백·따뜻한 오프화이트 배경**: 서울비디의 "읽히는 사이트" 감각. 단 브라운이 아니라 바로드림 로고 색(차콜 #454C56 + 옐로 #F1AE22)로.
8. **치과 백과사전/칼럼** 블록은 2단계로(안산점 사전은 안산 도메인에 있음 — 시화점은 칼럼부터).

## 가져오지 않을 것
- 최상급·비교·보증 표현, 후기 인용, 가격 단정 표(비급여 고지는 별도 페이지로 법정 양식만), 팝업 배너 남발, 게임형 콘텐츠, JS로만 렌더되는 본문.
