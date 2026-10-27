# 시화점 홈페이지 공개 전 확인표 (2026-10-26 기준)

## 원장 검토 필요 (의료 내용)
- [ ] 치료 페이지 20개 본문 — 특히 sedation.html(의식하진정법: 모니터링·당일 운전 금지·보호자 동반 문구), immediate-loading.html(조건 설명), wisdom.html(신경 감각 저하 안내), whitening.html(임신·수유 제한)
- [ ] 각 페이지 "검토" 바이라인의 원장 배정(이진학/한지상/고수연) — 현재 임의 배정
- [ ] about.html "통증을 줄이기 위한 마취 방법" → 실제 장비 이름으로 교체 (site.json anesthesia_device)
- [ ] 전문의 설명 문구(통합치의학과/치과보존과) 2종

## 사실 정보 (site.json에 입력하면 자동 반영)
- [ ] domain — 사용할 도메인 (현재 임시 https://barodreamsihwa.kr)
- [ ] biz_no — 사업자등록번호
- [ ] naver_place.url, kakao_url, same_as(블로그·인스타 등)
- [ ] geo.lat/lng — 지도 좌표
- [ ] directions / parking / transit — 찾아오는 길·주차·대중교통
- [ ] fees[] + fees_date — 비급여 금액(의료법 제45조 고지 의무, 공개 전 필수)
- [ ] gtm_id — GTM 컨테이너 ID (새 컨테이너 또는 안산점 컨테이너에 시화점 트리거 추가)
- [ ] 구글 비즈니스 프로필 상호 "바로드림치과의원 시화점"으로 변경

## 사진 (assets/img/ 에 파일명 그대로 넣으면 자동 반영)
- hero.jpg (첫 화면, 가로), family.jpg (대기실·세로), exterior.jpg (외관), dr-lee.jpg, dr-ko.jpg (세로 3:4), dr-han.jpg(안산점 사진 임시 사용 중)
- tour-lobby.jpg, tour-room.jpg, tour-consult.jpg, tour-ct.jpg, tour-steril.jpg, tour-exterior.jpg
- og.jpg (1200×630, 공유 미리보기)

## 배포
- [ ] GitHub 저장소 barodreamdc/barodream-sihwa 생성(원장) → 파일 올리기(클로드) → Pages 켜기 → CNAME
- [ ] DNS A 레코드 → GitHub Pages, www CNAME
- [ ] 구글 서치콘솔·네이버 서치어드바이저 등록, sitemap.xml 제출, IndexNow 키
- [ ] 안산점 사이트에 시화점 링크 1개(푸터 "다른 지점") — 서로 별도 기관임을 명시

## 자동 점검 결과 (2026-10-26)
- 내부 링크·이미지 경로·JSON-LD 문법: 오류 0
- axe-core 접근성(WCAG 2.1 AA + best-practice), 데스크톱·모바일 전 페이지: 위반 0
- 의료광고법 금지어 스캔(최고·보장·완치·무통·후기 등): 해당 없음(부정문 2건은 허용)
- 페이지 무게: HTML 20~30KB, 이미지 총 65KB(사진 추가 시 WebP 변환 예정)
