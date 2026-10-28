# -*- coding: utf-8 -*-
"""홈·소개·위치·의료진·커뮤니티·법정 페이지 본문."""
import html, datetime
TODAY = datetime.date.today().isoformat()
def esc(s): return html.escape(s, quote=True)

DOC_SLUG = {'이진학':'lee','한지상':'han','고수연':'ko'}

def img_or_ph(path, alt, ph_text, style='aspect-ratio:4/3', cls=''):
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if path and os.path.exists(os.path.join(root, path)):
        try:
            from PIL import Image
            w,h = Image.open(os.path.join(root, path)).size
        except Exception:
            w,h = 800,600
        return f'<figure><img src="{path}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async" style="{style};object-fit:cover;width:100%;height:auto" class="{cls}"></figure>'
    return f'<div class="ph" style="{style}">{esc(ph_text)}</div>'

HOME_FAQ = [
  ('수면치료와 의식하진정법은 같은 건가요?','흔히 수면치료라고 부르지만 치과에서 시행하는 정확한 이름은 의식하진정법입니다. 적용 가능 여부는 건강 상태에 따라 상담에서 확인합니다.'),
  ('수요일 야간진료는 몇 시까지인가요?','수요일은 저녁 9시까지 진료하며 접수는 8시에 마감합니다. 오후 5시 30분부터 6시까지는 휴게시간입니다.'),
  ('토요일에도 진료하나요?','토요일은 오전 10시부터 오후 2시까지 진료하며 접수는 1시에 마감합니다.'),
  ('공휴일에는 쉬나요?','공휴일은 휴진이 원칙입니다. 진료하는 공휴일은 홈페이지 공지사항과 네이버 플레이스 공지로 미리 안내합니다.'),
]

def doctor_card(d, site):
    slug = DOC_SLUG[d['name']]
    photo = img_or_ph(f'assets/img/dr-{slug}.jpg', f'{d["name"]} {d["title"]}', f'[{d["name"]} 원장 실제 사진]', 'aspect-ratio:3/4')
    cred = ' · '.join(d['bio'][1:4]) if len(d['bio'])>1 else ''
    q = f'<p class="q">“{esc(d["quote"])}”</p>' if d.get('quote') else ''
    return f'''<article class="card doc">{photo}<div><h3>{esc(d["name"])}<small>{esc(d["title"])}</small></h3><p class="spec">{esc(d["specialty"])}</p><p class="cred">{esc(cred)}</p>{q}<a href="doctor-{slug}.html" style="font-size:14px;font-weight:600;display:inline-block;margin-top:10px">소개 더 보기</a></div></article>'''

def HOME(site, hours_strip, hours_table):
    tel = site['phone_display']
    docs = site['doctors']
    body = f'''
<section class="hero"><div class="wrap"><div class="grid g6-6" style="align-items:center;gap:64px">
  <div>
    <h1>저도 어렸을 때<br>치과가 무서웠습니다.</h1>
    <p class="lead">그래서 어떻게 하면 덜 아프게 치료할 수 있을지 늘 생각합니다. 검사 결과와 치료 방법을 먼저 설명드리고, 결정은 들으신 뒤에 하셔도 됩니다.</p>
    <p class="by">바로드림치과의원 시화점 대표원장 이진학</p>
    <div class="btns"><a class="btn btn-p" href="tel:{tel}" data-ev="contact_call">전화 {tel}</a><a class="btn btn-s" href="location.html">진료시간·오시는 길</a></div>
    <p class="ask">상담 시 어떤 것부터 물어보고 싶으세요? 편하게 물어보셔도 됩니다.</p>
  </div>
  {img_or_ph('assets/img/hero.jpg','바로드림치과의원 시화점 진료실','[이진학 원장 또는 진료실 실제 사진 — 따뜻한 톤]')}
</div></div></section>
{hours_strip()}
<section class="sec"><div class="wrap"><div class="grid g5-7" style="gap:64px;align-items:start">
  {img_or_ph('assets/img/family.jpg','가족이 함께 오는 바로드림치과의원 시화점 대기실','[대기실 또는 가족 환자 안내 장면 실제 사진]','aspect-ratio:4/5')}
  <div class="prose">
    <h2 style="margin-top:0">한 가족의 주치의가 되고 싶은 치과입니다</h2>
    <p>어린아이부터 할아버지, 할머니까지 가족이 함께 오시는 분들이 많습니다. 한 가족의 치아를 오래 보다 보면 가족이 비슷하게 겪는 문제가 보입니다. 충치가 잘 생기는 체질, 잇몸이 약한 체질은 가족끼리 닮는 경우가 많아서, 한 분을 볼 때 가족 이야기를 함께 듣는 것이 진료에 도움이 됩니다.</p>
    <p>살릴 수 있는 치아는 치과보존과 전문의가 끝까지 살립니다. 살리기 어려운 치아는 억지로 두지 않고 임플란트로 잇습니다. 어느 쪽인지는 검사 결과를 보고 원장들이 함께 판단해 설명드립니다.</p>
    <p><a href="about.html" style="font-weight:600">병원 소개 더 읽기</a></p>
  </div>
</div></div></section>
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head"><h2>진료 안내</h2><p class="small muted">항목을 누르면 치료 과정과 주의사항을 설명하는 페이지로 이동합니다.</p></div>
  <div class="grid g5 dir">
    <div><h3>임플란트</h3><a href="implant.html">임플란트</a><a href="implant-all-on-x.html">풀아치 임플란트(All-on-X)</a><a href="implant-navigation.html">네비게이션 임플란트</a><a href="immediate-loading.html">즉시로딩</a><a href="denture.html">틀니(오버덴처)</a></div>
    <div><h3>의식하진정법</h3><a href="sedation.html">의식하진정법이란</a><p class="note">많은 분들이 수면치료라고 부르지만 정확한 이름은 의식하진정법입니다. 임플란트, 충치·신경·잇몸·보철 치료에 적용할 수 있습니다.</p></div>
    <div><h3>보존·일반진료</h3><a href="cavity.html">충치치료</a><a href="rootcanal.html">신경치료</a><a href="gum.html">잇몸치료</a><a href="wisdom.html">사랑니 발치</a><a href="scaling.html">스케일링</a><a href="resin.html">레진</a><a href="inlay.html">인레이·온레이</a><a href="crown.html">크라운</a><a href="prosthesis.html">보철치료</a></div>
    <div><h3>심미치료</h3><a href="whitening.html">치아미백</a><a href="laminate.html">라미네이트</a><a href="resin-front.html">앞니 레진</a></div>
    <div><h3>턱관절</h3><a href="tmj.html">턱관절 치료</a></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>증상으로 찾기</h2><a href="symptoms.html">전체 보기</a></div>
  <div class="related" style="gap:12px"><a href="symptom-sensitive.html">이가 시려요</a><a href="symptom-bleeding-gum.html">잇몸에서 피가 나요</a><a href="symptom-loose-tooth.html">치아가 흔들려요</a><a href="symptom-pain-chewing.html">씹을 때 아파요</a><a href="symptom-jaw-click.html">턱에서 소리가 나요</a><a href="symptom-dental-fear.html">치과가 무서워요</a><a href="symptom-missing-tooth.html">이가 빠졌어요</a><a href="symptom-wisdom-pain.html">사랑니가 아파요</a></div>
</div></section>
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head"><h2>의료진</h2><a href="doctors.html">의료진 소개</a></div>
  <div class="grid g3" style="gap:24px">{''.join(doctor_card(d, site) for d in docs)}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="grid g5-7" style="gap:56px">
  <div><div class="sec-head" style="margin-bottom:12px"><h2 style="font-size:22px">공지사항</h2><a href="notice.html">전체 보기</a></div>
    <div class="list"><a href="notice.html#open"><span class="tag">공지</span><span>바로드림치과의원 시화점 홈페이지를 열었습니다</span><span class="date num">{TODAY[:7].replace('-','.')}</span></a><a href="notice.html#holiday"><span class="tag">공지</span><span>공휴일 진료 안내</span><span class="date num">{TODAY[:7].replace('-','.')}</span></a></div></div>
  <div><div class="sec-head" style="margin-bottom:12px"><h2 style="font-size:22px">칼럼</h2><a href="column.html">전체 보기</a></div>
    <div class="list"><a href="sedation.html"><span class="tag">의식하진정법</span><span>수면치료라고 부르는 것의 정확한 이름</span><span class="date">이진학 원장</span></a><a href="immediate-loading.html"><span class="tag">임플란트</span><span>즉시로딩은 누구나 할 수 있는 방법이 아닙니다</span><span class="date">이진학 원장</span></a><a href="rootcanal.html"><span class="tag">신경치료</span><span>신경치료 후 꼭 크라운을 해야 하나요</span><span class="date">고수연 원장</span></a></div></div>
</div></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="grid g5-7" style="align-items:start">
  <div><h2>오시는 길</h2><p style="font-family:var(--font-serif);font-size:20px;line-height:1.5;margin:14px 0 8px">경기 시흥시 정왕대로 210<br>성담스퀘어 5층 518호</p><p class="small muted">지번 경기 시흥시 정왕동 1734-2 · 우편번호 15066<br>{esc(site.get('directions','건물 5층으로 올라오시면 518호입니다. 주차·대중교통 안내는 진료시간·오시는 길 페이지를 참고해 주세요.'))}</p>
    <div class="btns" style="margin-top:16px"><a class="btn btn-p" href="tel:{tel}" data-ev="contact_call">전화 {tel}</a><a class="btn btn-s" href="{site['naver_place'].get('url') or 'location.html'}" data-ev="contact_naver" rel="noopener">네이버 지도</a></div></div>
  <div>{img_or_ph('assets/img/exterior.jpg','성담스퀘어 건물 외관','[지도 또는 건물 외관 실제 사진]','height:320px')}</div>
</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>자주 묻는 질문</h2><a href="faq.html">전체 보기</a></div><div class="faq" style="max-width:820px">{''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q,a in HOME_FAQ)}</div></div></section>
'''
    page = dict(file='index.html', title='바로드림치과의원 시화점 | 시흥 정왕동 치과 — 전문의 임플란트·의식하진정법·충치·신경치료',
                description='시흥 정왕동 성담스퀘어 5층 바로드림치과의원 시화점. 통합치의학과 전문의와 치과보존과 전문의가 임플란트, 의식하진정법(흔히 수면치료), 충치·신경·잇몸치료를 진료합니다. 수요일 야간진료 21시까지, 토요일 진료. 전화 031-498-2282.',
                ai_summary='바로드림치과의원 시화점은 경기 시흥시 정왕동 성담스퀘어 5층 518호에 있는 치과입니다. 통합치의학과 전문의 이진학·한지상, 치과보존과 전문의 고수연이 진료하며 임플란트, 의식하진정법, 충치·신경·잇몸치료, 심미치료, 턱관절 치료를 합니다. 수요일 21시까지 야간진료, 토요일 14시까지 진료, 일·공휴일 휴진. 전화 031-498-2282.')
    return dict(page=page, body=body, faq=HOME_FAQ)

FAQ_ALL = HOME_FAQ + [
  ('처음 가면 어떤 순서로 진행되나요?','접수 후 문진표를 작성하시고, 필요한 검사(엑스레이 등)를 한 뒤 원장이 검진하고 설명드립니다. 치료는 설명을 들으신 뒤 결정하셔도 됩니다.'),
  ('예약 없이 가도 되나요?','가능하지만 대기 시간이 길어질 수 있어 전화 예약을 권합니다. 수요일 저녁과 토요일은 특히 예약이 몰립니다.'),
  ('전문의가 직접 진료하나요?','네. 통합치의학과 전문의 이진학·한지상 원장과 치과보존과 전문의 고수연 원장이 상담과 치료를 직접 맡습니다. 전문의는 보건복지부가 인정하는 자격입니다.'),
  ('치과보존과 전문의는 어떤 전문의인가요?','충치치료·신경치료처럼 자연치아를 살리는 분야를 추가로 수련하고 자격을 받은 치과의사입니다.'),
  ('통합치의학과 전문의는 어떤 전문의인가요?','여러 진료 분야를 함께 수련한 뒤 보건복지부가 인정하는 자격을 받은 치과의사입니다.'),
  ('안산점과 시화점은 같은 병원인가요?','같은 바로드림치과 그룹이지만 각각 별도의 의료기관입니다. 이 홈페이지는 시화점(시흥 정왕동)만 안내합니다. 안산점은 barodreamdental.kr에서 확인하실 수 있습니다.'),
  ('비급여 비용은 어디서 확인하나요?','비급여 안내 페이지에 항목별 금액을 고지하고 있으며, 정확한 비용은 검사 후 상담에서 설명드립니다.'),
  ('주차는 어떻게 하나요?','[주차 안내 확인 후 기재]'),
]

def PAGES(site, hours_table, page_hero, faq_html, ld_breadcrumb, ld_faq):
    tel = site['phone_display']; addr = site['address']['road']
    P = []
    # 병원소개
    p = dict(file='about.html', h1='인사말·소개', title='병원 소개 | 바로드림치과의원 시화점 — 시흥 정왕동 치과',
             description='저도 어렸을 때 치과가 무서웠습니다. 바로드림치과의원 시화점 이진학 대표원장의 인사말과 진료 원칙, 한 가족의 주치의가 되고 싶은 이유.', lead='치료보다 설명을 먼저 드리는 치과가 되고 싶습니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('병원소개','about.html')]) + f'''
<section class="sec"><div class="wrap"><div class="grid g5-7" style="gap:64px;align-items:start">
  {img_or_ph('assets/img/dr-lee.jpg','이진학 대표원장','[이진학 원장 실제 사진]','aspect-ratio:3/4')}
  <div class="prose">
    <h2 style="margin-top:0">저도 어렸을 때 치과 통증이 무서웠습니다</h2>
    <p>그래서 어떻게 하면 덜 아프게 치료할 수 있을지 생각하며 {esc(site.get('anesthesia_device','통증을 줄이기 위한 마취 방법'))}과 의식하진정법을 시행하고 있습니다. 많은 분들이 수면치료라고 부르지만, 정확한 이름은 의식하진정법입니다. 치과 치료가 두려워 미뤄 오신 분이라면, 치료를 결정하기 전에 먼저 어떤 방법이 있는지 들어 보셔도 됩니다.</p>
    <h2>한 가족의 주치의가 되고 싶습니다</h2>
    <p>어린아이부터 할아버지, 할머니까지 가족이 함께 오시는 분들이 많습니다. 한 가족의 치아를 오래 보다 보면 가족이 비슷하게 겪는 문제가 보입니다. 충치가 잘 생기는 체질, 잇몸이 약한 체질은 가족끼리 닮는 경우가 많아서, 한 분을 볼 때 가족 이야기를 함께 듣는 것이 진료에 도움이 됩니다. 시화점은 그렇게 한 가족의 주치의가 되고 싶은 치과입니다.</p>
    <h2>살릴 치아와 잇는 치아를 함께 판단합니다</h2>
    <p>살릴 수 있는 치아는 치과보존과 전문의가 끝까지 살립니다. 살리기 어려운 치아는 억지로 두지 않고 임플란트로 잇습니다. 어느 쪽인지는 검사 결과를 보고 원장들이 함께 판단해 설명드립니다. 치료 후에는 맞물림(교합)을 세밀하게 조정하고 정기 점검으로 관리합니다.</p>
    <h2>설명을 먼저 드립니다</h2>
    <p>검사 결과와 치료 선택지, 예상 기간과 비용을 먼저 말씀드립니다. 지금 치료가 필요하지 않다면 그렇게 말씀드립니다. 결정은 들으신 뒤에 하셔도 되고, 설명만 듣고 돌아가셔도 괜찮습니다.</p>
    <p class="by muted">바로드림치과의원 시화점 대표원장 이진학</p>
    <div class="btns" style="margin-top:24px"><a class="btn btn-p" href="doctors.html">의료진 소개</a><a class="btn btn-s" href="location.html">진료시간·오시는 길</a></div>
  </div>
</div></div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('병원소개','about.html')])]; p['prio']='0.8'; P.append(p)

    # 진료시간·오시는 길
    p = dict(file='location.html', h1='진료시간·오시는 길', title='진료시간·오시는 길 | 바로드림치과의원 시화점 — 시흥 정왕동 성담스퀘어 5층',
             description=f'바로드림치과의원 시화점 위치: {addr}. 수요일 야간진료 21시까지, 토요일 14시까지, 일·공휴일 휴진. 전화 {tel}. 주차·대중교통 안내.', lead='경기 시흥시 정왕대로 210 성담스퀘어 5층 518호')
    p['body'] = page_hero(p, [('홈','index.html'),('오시는 길','location.html')]) + f'''
<section class="sec"><div class="wrap"><div class="grid g6-6" style="gap:56px;align-items:start">
  <div>
    <h2 style="margin-bottom:16px">진료시간</h2>{hours_table()}
    <h2 style="margin:40px 0 12px">주소</h2>
    <p style="font-family:var(--font-serif);font-size:20px;line-height:1.5">경기 시흥시 정왕대로 210 성담스퀘어 5층 518호</p>
    <p class="small muted" style="margin-top:8px">지번 경기 시흥시 정왕동 1734-2 · 우편번호 15066</p>
    <p class="small" style="margin-top:12px">{esc(site.get('directions','[찾아오는 길 안내 — 건물 입구, 엘리베이터, 주변 랜드마크 확인 후 기재]'))}</p>
    <h2 style="margin:40px 0 12px">주차·대중교통</h2>
    <p class="small">{esc(site.get('parking','[주차 안내 확인 후 기재]'))}</p>
    <p class="small" style="margin-top:8px">{esc(site.get('transit','[버스·지하철 안내 확인 후 기재]'))}</p>
    <div class="btns" style="margin-top:24px"><a class="btn btn-p" href="tel:{tel}" data-ev="contact_call">전화 {tel}</a><a class="btn btn-s" href="{site['naver_place'].get('url') or '#'}" data-ev="contact_naver" rel="noopener">네이버 지도에서 보기</a></div>
  </div>
  <div>{img_or_ph('assets/img/exterior.jpg','성담스퀘어 건물 외관','[지도 또는 건물 외관 실제 사진]','height:360px')}
    <p class="caption" style="margin-top:12px">지도는 네이버 지도 링크로 연결됩니다. 길찾기 앱에서는 "바로드림치과의원 시화점" 또는 도로명 주소로 검색해 주세요.</p></div>
</div>
<div style="margin-top:56px"><h2 style="margin-bottom:12px">동네별 오시는 길</h2>
<p class="small muted" style="margin-bottom:16px">출발하는 동네를 고르면 그 동네 기준으로 가는 방법과 자주 묻는 내용을 보실 수 있습니다.</p>
<div class="related" style="gap:12px">''' + ''.join(f'<a href="{h}">{l}</a>' for l, h in [('시흥 시내에서','siheung-dental.html'),('정왕동에서','jeongwang-dental.html'),('배곧에서','baegot-dental.html'),('시화에서','sihwa-dental.html')]) + '''</div>
<p class="small muted" style="margin-top:20px">함께 보기: <a href="siheung-night-dental.html">수요일 야간진료 안내</a> · <a href="siheung-implant.html">시흥에서 임플란트 상담 받으실 때</a></p></div>
</div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('오시는 길','location.html')])]; p['prio']='0.9'; P.append(p)

    # 둘러보기
    p = dict(file='tour.html', h1='병원 둘러보기', title='병원 둘러보기 | 바로드림치과의원 시화점',
             description='바로드림치과의원 시화점의 대기실, 진료실, 상담실, 검사 장비를 실제 사진으로 소개합니다.', lead='실제 사진으로 보는 시화점 진료 공간입니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('병원소개','about.html'),('병원 둘러보기','tour.html')]) + f'''
<section class="sec"><div class="wrap"><div class="grid g3" style="gap:16px">
  {img_or_ph('assets/img/tour-lobby.jpg','대기실','[대기실 실제 사진]','height:260px')}
  {img_or_ph('assets/img/tour-room.jpg','진료실','[진료실 실제 사진]','height:260px')}
  {img_or_ph('assets/img/tour-consult.jpg','상담실','[상담실 실제 사진]','height:260px')}
  {img_or_ph('assets/img/tour-ct.jpg','검사 장비','[CT 등 검사 장비 실제 사진]','height:260px')}
  {img_or_ph('assets/img/tour-steril.jpg','소독실','[소독·멸균 공간 실제 사진]','height:260px')}
  {img_or_ph('assets/img/tour-exterior.jpg','건물 외관','[건물 외관 실제 사진]','height:260px')}
</div><p class="caption" style="margin-top:16px">모든 사진은 바로드림치과의원 시화점에서 실제로 촬영한 것입니다.</p></div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('병원소개','about.html'),('병원 둘러보기','tour.html')])]; P.append(p)

    # 다른 지점 안내
    br = site.get('branches', [])
    cards = ''.join(f'''<div class="card" style="padding:28px">
    <h2 style="margin:0 0 6px;font-size:22px">{esc(b["name"])}</h2>
    <p class="small muted" style="margin:0 0 14px">{esc(b.get("note",""))}</p>
    <p class="small" style="margin:0 0 6px">{esc(b["address"])}</p>
    <p class="small" style="margin:0 0 18px">전화 <a href="tel:{esc(b["phone"].replace('-',''))}">{esc(b["phone"])}</a></p>
    <a class="btn btn-s" href="{esc(b["url"])}" rel="noopener">{esc(b["name"])} 홈페이지</a>
  </div>''' for b in br)
    p = dict(file='branches.html', h1='다른 지점 안내', title='안산점·향남점 안내 | 바로드림치과의원 시화점',
             description='바로드림치과 안산점(안산 고잔동)과 향남점(화성 향남읍)의 주소, 전화, 홈페이지 안내. 세 지점은 각각 별도로 개설된 의료기관입니다.', lead='같은 이름을 쓰는 안산점과 향남점이 있습니다. 가까운 곳으로 방문하시면 됩니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('병원소개','about.html'),('다른 지점 안내','branches.html')]) + f'''
<section class="sec"><div class="wrap">
  <div class="prose" style="max-width:720px;margin-bottom:40px">
    <p>바로드림치과 안산점, 향남점, 시화점은 각각 별도로 개설된 의료기관이며, 진료·예약·비용은 각 지점에서 따로 안내합니다. 원장들은 서로 소통하며 필요한 경우 환자분을 다른 지점으로 안내해 드립니다. 이 홈페이지는 시화점(시흥시 정왕동) 홈페이지입니다.</p>
  </div>
  <div class="grid g2" style="gap:20px">{cards}</div>
  <p class="caption" style="margin-top:24px">시화점 문의는 {tel}, 주소는 {esc(addr)} 입니다.</p>
</div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('병원소개','about.html'),('다른 지점 안내','branches.html')])]; p['prio']='0.4'; P.append(p)

    # 비급여 안내
    fees = site.get('fees', [])
    rows = ''.join(f'<tr><td>{esc(f["item"])}</td><td class="num" style="text-align:right">{esc(f["price"])}</td><td class="small muted">{esc(f.get("note",""))}</td></tr>' for f in fees) if fees else \
        ''.join(f'<tr><td>{n}</td><td class="num" style="text-align:right">[금액 확인 후 기재]</td><td class="small muted"></td></tr>' for n in ['임플란트(픽스처·보철 포함)','풀아치 임플란트','네비게이션 가이드','뼈이식','틀니(전체/부분)','크라운(지르코니아)','크라운(금)','인레이(세라믹)','인레이(금)','레진','라미네이트','치아미백(전문가)','치아미백(자가)','의식하진정법','턱관절 장치','스케일링(비급여 해당 시)','사랑니 발치(매복, 비급여 해당 시)'])
    p = dict(file='fees.html', h1='비급여 안내', title='비급여 진료비용 안내 | 바로드림치과의원 시화점',
             description='의료법 제45조에 따른 바로드림치과의원 시화점 비급여 진료비용 고지. 임플란트, 크라운, 인레이, 레진, 라미네이트, 미백, 의식하진정법 등 항목별 금액.', lead='의료법 제45조에 따라 비급여 진료비용을 고지합니다. 실제 비용은 검사 후 상담에서 설명드립니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('병원소개','about.html'),('비급여 안내','fees.html')]) + f'''
<section class="sec"><div class="wrap"><div class="card" style="padding:8px 24px 24px;overflow-x:auto" tabindex="0" role="region" aria-label="비급여 진료비용 표">
<table style="border-collapse:collapse;width:100%;font-size:15px;min-width:560px"><thead><tr style="background:var(--bg-2)"><th style="text-align:left;padding:12px 8px">항목</th><th style="text-align:right;padding:12px 8px">금액(원)</th><th style="text-align:left;padding:12px 8px">비고</th></tr></thead><tbody>{rows}</tbody></table>
</div>
<p class="caption" style="margin-top:16px">고지 기준일 {esc(site.get('fees_date','[기재]'))}. 금액은 치료 범위와 재료에 따라 달라질 수 있으며, 건강보험 적용 항목은 별도입니다. 65세 이상 틀니·임플란트 건강보험 적용 여부는 상담에서 확인해 드립니다.</p>
</div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('비급여 안내','fees.html')])]; P.append(p)

    # 의료진 목록
    p = dict(file='doctors.html', h1='의료진 소개', title='의료진 소개 | 바로드림치과의원 시화점 — 통합치의학과·치과보존과 전문의',
             description='바로드림치과의원 시화점 의료진: 이진학 대표원장(통합치의학과 전문의), 한지상 원장(통합치의학과 전문의), 고수연 원장(치과보존과 전문의). 전문의 자격과 이력.', lead='전문의는 치과대학 졸업 후 해당 분야를 추가로 수련하고 보건복지부가 인정하는 자격을 받은 치과의사입니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('의료진','doctors.html')]) + f'''
<section class="sec"><div class="wrap"><h2 style="margin-bottom:24px">원장 소개</h2><div class="grid g3" style="gap:24px">{''.join(doctor_card(d, site) for d in site['doctors'])}</div>
<div class="prose" style="margin-top:56px"><h2>전문의 자격에 대하여</h2>
<p><b>통합치의학과 전문의</b>는 여러 진료 분야를 함께 수련한 뒤 보건복지부가 인정하는 자격을 받은 치과의사입니다. 임플란트, 보철, 의식하진정법처럼 여러 분야가 겹치는 치료 계획을 세우는 데 도움이 됩니다.</p>
<p><b>치과보존과 전문의</b>는 충치치료·신경치료처럼 자연치아를 살리는 분야를 전문으로 수련하고 자격을 받은 치과의사입니다. 까다로운 신경치료, 재신경치료, 넓은 충치의 수복을 맡습니다.</p>
<p>바로드림치과의원 시화점에서는 살릴 수 있는 치아는 치과보존과 전문의가, 살리기 어려운 치아는 임플란트·보철로 잇는 쪽을 통합치의학과 전문의가 맡아, 검사 결과를 보고 함께 판단해 설명드립니다.</p></div></div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('의료진','doctors.html')])]; p['prio']='0.8'; P.append(p)

    # 공지사항
    p = dict(file='notice.html', h1='공지사항', title='공지사항 | 바로드림치과의원 시화점', description='바로드림치과의원 시화점 공지: 공휴일 진료, 휴진, 진료시간 변경 안내.', lead='진료시간 변경과 공휴일 진료 여부를 여기에서 먼저 안내합니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('커뮤니티','notice.html'),('공지사항','notice.html')]) + f'''
<section class="sec"><div class="wrap prose">
<article id="open" class="card" style="padding:28px;margin-bottom:16px"><p class="caption num">{TODAY}</p><h2 style="margin:6px 0 12px;font-size:22px">바로드림치과의원 시화점 홈페이지를 열었습니다</h2><p style="margin:0">진료 안내와 의료진, 진료시간을 이곳에서 확인하실 수 있습니다. 궁금한 점은 전화 {tel}로 문의해 주세요.</p></article>
<article id="holiday" class="card" style="padding:28px"><p class="caption">상시</p><h2 style="margin:6px 0 12px;font-size:22px">공휴일 진료 안내</h2><p style="margin:0">공휴일은 휴진이 원칙입니다. 진료하는 공휴일이 있으면 이 페이지와 네이버 플레이스 공지에 미리 안내합니다.</p></article>
</div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('공지사항','notice.html')])]; P.append(p)

    # 칼럼
    p = dict(file='column.html', h1='칼럼', title='칼럼 | 바로드림치과의원 시화점 — 원장이 직접 쓰는 치과 이야기', description='바로드림치과의원 시화점 원장들이 직접 쓰는 치과 칼럼. 의식하진정법, 임플란트, 신경치료, 잇몸 관리에 대한 설명.', lead='원장들이 직접 씁니다. 진료실에서 자주 받는 질문부터 하나씩 답합니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('커뮤니티','notice.html'),('칼럼','column.html')]) + f'''
<section class="sec"><div class="wrap"><div class="list" style="max-width:820px">
<a href="sedation.html"><span class="tag">의식하진정법</span><span>수면치료라고 부르는 것의 정확한 이름</span><span class="date">이진학 원장</span></a>
<a href="immediate-loading.html"><span class="tag">임플란트</span><span>즉시로딩은 누구나 할 수 있는 방법이 아닙니다</span><span class="date">이진학 원장</span></a>
<a href="rootcanal.html"><span class="tag">신경치료</span><span>신경치료 후 꼭 크라운을 해야 하나요</span><span class="date">고수연 원장</span></a>
<a href="gum.html"><span class="tag">잇몸</span><span>잇몸질환은 가족끼리 닮습니다</span><span class="date">고수연 원장</span></a>
</div><p class="caption" style="margin-top:16px">새 칼럼은 글마다 별도 페이지로 추가됩니다. 지금은 진료 안내 페이지의 설명으로 연결됩니다.</p></div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('칼럼','column.html')])]; P.append(p)

    # FAQ
    p = dict(file='faq.html', h1='자주 묻는 질문', title='자주 묻는 질문 | 바로드림치과의원 시화점', description='바로드림치과의원 시화점 FAQ: 수면치료와 의식하진정법의 차이, 수요일 야간진료, 토요일·공휴일 진료, 첫 방문 순서, 전문의, 비급여, 주차.', lead='진료실과 전화로 가장 많이 받는 질문입니다.')
    p['body'] = page_hero(p, [('홈','index.html'),('커뮤니티','notice.html'),('자주 묻는 질문','faq.html')]) + f'''
<section class="sec"><div class="wrap"><div class="faq" style="max-width:820px">{''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q,a in FAQ_ALL)}</div></div></section>'''
    p['ld'] = [ld_breadcrumb([('홈','index.html'),('자주 묻는 질문','faq.html')]), ld_faq(FAQ_ALL)]; p['prio']='0.7'; P.append(p)

    # 개인정보처리방침
    p = dict(file='privacy.html', h1='개인정보처리방침', title='개인정보처리방침 | 바로드림치과의원 시화점', description='바로드림치과의원 시화점 홈페이지 개인정보처리방침.', noindex=True)
    p['body'] = page_hero(p, [('홈','index.html'),('개인정보처리방침','privacy.html')]) + f'''
<section class="sec"><div class="wrap prose">
<p>바로드림치과의원 시화점(이하 "의원")은 개인정보 보호법에 따라 이용자의 개인정보를 보호하고 관련 고충을 처리하기 위해 다음과 같이 개인정보처리방침을 둡니다.</p>
<h2>1. 홈페이지에서 수집하는 개인정보</h2><p>이 홈페이지는 회원가입이나 상담 신청 양식을 통해 개인정보를 수집하지 않습니다. 전화·카카오톡·네이버 예약은 각 서비스의 개인정보처리방침이 적용됩니다.</p>
<h2>2. 웹 분석 도구</h2><p>홈페이지 이용 통계를 위해 Google 태그 관리자와 Google 애널리틱스를 사용할 수 있으며, 이 과정에서 쿠키와 접속 기록(접속 페이지, 기기 종류 등)이 익명으로 수집될 수 있습니다. 브라우저 설정에서 쿠키를 거부할 수 있습니다.</p>
<h2>3. 진료 과정에서의 개인정보</h2><p>진료 예약과 진료 시 수집하는 개인정보(성명, 연락처, 진료기록 등)는 의료법과 개인정보 보호법에 따라 처리·보관하며, 법령에서 정한 기간 동안 보관 후 파기합니다.</p>
<h2>4. 개인정보 보호책임자</h2><p>성명: {esc(site.get('privacy_officer','이진학'))} · 전화: {tel}</p>
<h2>5. 시행일</h2><p>이 방침은 {TODAY}부터 적용됩니다.</p>
</div></section>'''
    P.append(p)

    # 404
    p = dict(file='404.html', h1='페이지를 찾을 수 없습니다', title='페이지를 찾을 수 없습니다 | 바로드림치과의원 시화점', description='요청하신 페이지가 없습니다.', noindex=True)
    p['body'] = f'''<section class="sec" style="padding-top:96px;padding-bottom:96px"><div class="wrap prose"><h1>페이지를 찾을 수 없습니다</h1><p style="margin-top:16px">주소가 바뀌었거나 잘못 입력되었을 수 있습니다. 아래에서 원하시는 페이지로 이동해 주세요.</p>
<div class="btns" style="margin-top:24px"><a class="btn btn-p" href="index.html">홈으로</a><a class="btn btn-s" href="location.html">진료시간·오시는 길</a><a class="btn btn-s" href="tel:{tel}" data-ev="contact_call">전화 {tel}</a></div></div></section>'''
    P.append(p)
    return P

def build_doctor_pages(site, page_hero, ld_breadcrumb, site_url):
    out = []
    for d in site['doctors']:
        slug = DOC_SLUG[d['name']]
        file = f'doctor-{slug}.html'
        p = dict(file=file, h1=f'{d["name"]} {d["title"]}', title=f'{d["name"]} {d["title"]} | {d["specialty"]} — 바로드림치과의원 시화점',
                 description=f'바로드림치과의원 시화점 {d["name"]} {d["title"]}({d["specialty"]})의 이력과 진료 철학.', lead=d['specialty'])
        story = ''
        if d['name']=='이진학':
            story = '<h2>저도 어렸을 때 치과 통증이 무서웠습니다</h2><p>그래서 어떻게 하면 덜 아프게 치료할 수 있을지 생각하며 의식하진정법을 시행하고 있습니다. 어린아이부터 할아버지, 할머니까지 가족이 함께 오시는 분들이 많아, 한 가족의 주치의가 되고 싶은 마음으로 진료합니다.</p>'
        elif d['name']=='고수연':
            story = f'<p class="q" style="font-size:18px">“{esc(d["quote"])}”</p><p>자연치아가 주는 편안함과 기능은 어떤 인공치아도 완전히 대체하기 어렵습니다. 통증이나 까다로운 신경치료 앞에서도 치아를 살릴 방법을 끝까지 찾기 위해 치과보존과의 길을 선택했습니다.</p><p>치과보존과 전문의는 충치치료·신경치료처럼 자연치아를 살리는 분야를 추가로 수련하고 보건복지부가 인정하는 자격을 받은 치과의사입니다.</p>'
        elif d['name']=='한지상':
            story = f'<p class="q" style="font-size:18px">“{esc(d["quote"])}”</p><p>통합치의학과 전문의로 안산대학교 겸임교수, 대한시니어치과학회 연자로 활동하며 고령 환자분의 임플란트와 의식하진정법 진료를 해 왔습니다. 바로드림치과의원 시화점에서도 같은 방식으로 진료합니다.</p>'
        cred = ''.join(f'<li>{esc(b)}</li>' for b in d['bio'])
        body = page_hero(p, [('홈','index.html'),('의료진','doctors.html'),(f'{d["name"]} {d["title"]}', file)]) + f'''
<section class="sec"><div class="wrap"><div class="grid g5-7" style="gap:64px;align-items:start">
  {img_or_ph(f'assets/img/dr-{slug}.jpg', f'{d["name"]} {d["title"]}', f'[{d["name"]} 원장 실제 사진]', 'aspect-ratio:3/4')}
  <div class="prose">{story}<h2>주요 경력 및 학력</h2><ul class="cred-list">{cred}</ul>
  <div class="btns" style="margin-top:32px"><a class="btn btn-s" href="doctors.html">의료진 전체 보기</a></div></div>
</div></div></section>'''
        ld_person = {"@context":"https://schema.org","@type":"Person","@id":f"{site_url}/{file}#person","name":d['name'],"jobTitle":d['title'],
                     "worksFor":{"@id":f"{site_url}/#clinic"},"url":f"{site_url}/{file}","image":f"{site_url}/assets/img/dr-{slug}.jpg",
                     "hasCredential":{"@type":"EducationalOccupationalCredential","credentialCategory":"전문의","name":d['specialty']},
                     "hasOccupation":{"@type":"Occupation","name":"치과의사"},"description":f"바로드림치과의원 시화점 {d['title']}. {d['specialty']}."}
        if d.get('same_person_as'): ld_person['sameAs'] = [d['same_person_as']]
        out.append(dict(**p, body=body, ld=[ld_breadcrumb([('홈','index.html'),('의료진','doctors.html'),(f'{d["name"]} {d["title"]}', file)]), ld_person]))
    return out
