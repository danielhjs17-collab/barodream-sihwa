# -*- coding: utf-8 -*-
"""바로드림치과의원 시화점 — 정적 HTML 생성기.
사용: python3 scripts/build.py   → 저장소 루트에 *.html, sitemap.xml, robots.txt, llms.txt 생성.
모든 본문은 HTML에 직접 들어감(JS 렌더링 없음). 데이터는 data/site.json 하나가 기준.
"""
import json, os, re, html, datetime, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from content_pages import PAGES as STATIC_PAGES, HOME, build_doctor_pages
from content_treatments import TREATMENTS
from content_local import AREA, SYMPTOM, render_area, render_symptom, render_symptom_index
import content_dictionary as DICT

SITE = json.load(open(os.path.join(ROOT, 'data', 'site.json'), encoding='utf-8'))
SITE_URL = SITE.get('domain') or 'https://barodreamsihwa.kr'   # 도메인 확정 시 site.json "domain" 값으로 교체
SITE_URL = SITE_URL.rstrip('/')
TODAY = datetime.date.today().isoformat()
GTM_ID = SITE.get('gtm_id', 'GTM-XXXXXXX')
NAME = SITE['name']; TEL = SITE['phone_display']; TEL_E164 = SITE['phone_e164']
ADDR = SITE['address']['road']
LOGO = 'assets/img/logo.png'

NAV = [
  ('병원소개', 'about.html', [('인사말·소개','about.html'),('진료시간·오시는 길','location.html'),('병원 둘러보기','tour.html'),('비급여 안내','fees.html'),('다른 지점 안내','branches.html')]),
  ('임플란트', 'implant.html', [('임플란트','implant.html'),('풀아치 임플란트(All-on-X)','implant-all-on-x.html'),('네비게이션 임플란트','implant-navigation.html'),('즉시로딩','immediate-loading.html'),('틀니(오버덴처)','denture.html')]),
  ('의식하진정법', 'sedation.html', [('의식하진정법이란','sedation.html')]),
  ('보존·일반진료', 'cavity.html', [('충치치료','cavity.html'),('신경치료','rootcanal.html'),('잇몸치료','gum.html'),('사랑니 발치','wisdom.html'),('스케일링','scaling.html'),('레진','resin.html'),('인레이·온레이','inlay.html'),('크라운','crown.html'),('보철치료','prosthesis.html')]),
  ('심미·턱관절', 'whitening.html', [('치아미백','whitening.html'),('라미네이트','laminate.html'),('앞니 레진','resin-front.html'),('턱관절 치료','tmj.html')]),
  ('의료진', 'doctors.html', [('의료진 소개','doctors.html'),('이진학 원장','doctor-lee.html'),('한지상 원장','doctor-han.html'),('고수연 원장','doctor-ko.html')]),
  ('커뮤니티', 'notice.html', [('증상으로 찾기','symptoms.html'),('치과 용어사전','dictionary/index.html'),('공지사항','notice.html'),('칼럼','column.html'),('자주 묻는 질문','faq.html')]),
  ('오시는 길', 'location.html', []),
]
# 지역 안내 페이지 — 상단 메뉴에는 넣지 않고 푸터·오시는 길 하단에서만 연결
AREA_LINKS = [('시흥 치과','siheung-dental.html'),('정왕동 치과','jeongwang-dental.html'),('배곧에서 오시는 길','baegot-dental.html'),('시화 치과','sihwa-dental.html'),('시흥 임플란트','siheung-implant.html'),('시흥 야간진료 치과','siheung-night-dental.html')]

def esc(s): return html.escape(s, quote=True)

def nav_html(current):
    out = ['<ul class="nav">']
    for label, href, subs in NAV:
        active = ' class="is-active"' if (current == href or any(current == s[1] for s in subs)) else ''
        out.append(f'<li{active}><a href="{href}">{label}</a>')
        if subs and len(subs) > 1:
            out.append('<ul class="sub">' + ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in subs) + '</ul>')
        out.append('</li>')
    out.append('</ul>')
    return ''.join(out)

def drawer_html():
    out = ['<nav id="drawer" class="drawer" aria-label="전체 메뉴">']
    for label, href, subs in NAV:
        if subs and len(subs) > 1:
            out.append(f'<details><summary>{label}</summary>' + ''.join(f'<a href="{h}">{l}</a>' for l, h in subs) + '</details>')
        else:
            out.append(f'<details><summary>{label}</summary><a href="{href}">{label}</a></details>')
    out.append(f'<div class="d-foot">{esc(ADDR)}<br>수요일 야간진료 · 토요일 진료</div></nav>')
    return ''.join(out)

def footer_menu_html():
    out = ['<div class="ftr-menu">']
    for label, href, subs in NAV:
        items = subs if subs else [(label, href)]
        out.append(f'<div><h3>{label}</h3>' + ''.join(f'<a href="{h}">{l}</a>' for l, h in items) + '</div>')
    out.append('<div><h3>지역 안내</h3>' + ''.join(f'<a href="{h}">{l}</a>' for l, h in AREA_LINKS) + '</div>')
    out.append('</div>')
    return ''.join(out)

def hours_table():
    rows = []
    for h in SITE['hours']['_display']:
        if h.get('closed'):
            rows.append(f'<tr><th scope="row">{h["day"]}요일·공휴일</th><td>휴진</td></tr>')
            continue
    rows = [
      '<tr><th scope="row">월·화·목·금</th><td class="num">10:00 – 19:00</td></tr>',
      '<tr><th scope="row">수요일</th><td class="num"><span class="mark">10:00 – 21:00 야간진료</span></td></tr>',
      '<tr><th scope="row">토요일</th><td class="num">10:00 – 14:00</td></tr>',
      '<tr><th scope="row">점심시간</th><td class="num">13:00 – 14:00</td></tr>',
      '<tr><th scope="row">일요일·공휴일</th><td>휴진</td></tr>',
    ]
    return '<table class="hours"><caption class="caption" style="text-align:left;margin-bottom:8px">진료시간</caption><tbody>' + ''.join(rows) + '</tbody></table><p class="caption" style="margin-top:10px">접수 마감은 진료 종료 1시간 전입니다. 수요일은 17:30–18:00 휴게시간이 있습니다. 진료하는 공휴일은 공지로 안내합니다.</p>'

def hours_strip():
    return ('<div class="hours-strip"><div class="wrap num"><span><b>월·화·목·금</b> 10:00–19:00</span><span><b>수요일</b> <span class="mark">10:00–21:00 야간진료</span></span>'
            '<span><b>토요일</b> 10:00–14:00</span><span><b>점심</b> 13:00–14:00</span><span><b>일·공휴일</b> 휴진</span>'
            f'<span class="muted">접수 마감은 진료 종료 1시간 전 · {esc(ADDR)}</span></div></div>')

def ld_org():
    sameas = SITE.get('same_as', [])
    return {
      "@context":"https://schema.org","@type":["Dentist","MedicalClinic"],"@id":f"{SITE_URL}/#clinic",
      "name":NAME,"alternateName":[SITE['name_short'],SITE['legal_name']],"url":SITE_URL+"/","logo":f"{SITE_URL}/{LOGO}",
      "image":[f"{SITE_URL}/assets/img/og.jpg"],"telephone":TEL_E164,
      "description":"경기 시흥시 정왕동 성담스퀘어 5층 바로드림치과의원 시화점. 통합치의학과 전문의와 치과보존과 전문의가 진료하며, 임플란트·의식하진정법·충치·신경치료·잇몸치료 등을 진료합니다. 수요일 야간진료, 토요일 진료.",
      "address":{"@type":"PostalAddress","streetAddress":"정왕대로 210 성담스퀘어 5층 518호","addressLocality":"시흥시","addressRegion":"경기도","postalCode":SITE['address']['postal_code'],"addressCountry":"KR"},
      **({"geo":{"@type":"GeoCoordinates","latitude":SITE['geo']['lat'],"longitude":SITE['geo']['lng']}} if SITE['geo'].get('lat') else {}),
      "hasMap": SITE['naver_place'].get('url') or f"https://map.naver.com/p/search/{html.escape(NAME)}",
      "areaServed":[{"@type":"City","name":"시흥시"},{"@type":"Place","name":"정왕동"},{"@type":"Place","name":"시화"},{"@type":"City","name":"안산시"}],
      "openingHoursSpecification":SITE['hours']['schema_openingHoursSpecification'],
      "medicalSpecialty":["Dentistry"],
      "availableService":[{"@type":"MedicalProcedure","name":n} for n in ["임플란트","풀아치 임플란트","의식하진정법","충치치료","신경치료","잇몸치료","사랑니 발치","스케일링","치아미백","라미네이트","턱관절 치료","틀니"]],
      "employee":[{"@id":f"{SITE_URL}/doctor-{k}.html#person"} for k in ["lee","han","ko"]],
      "sameAs":sameas,
      "contactPoint":{"@type":"ContactPoint","telephone":TEL_E164,"contactType":"reservations","availableLanguage":["Korean"]},
    }

def ld_website():
    return {"@context":"https://schema.org","@type":"WebSite","@id":f"{SITE_URL}/#website","name":NAME,"url":SITE_URL+"/","inLanguage":"ko","publisher":{"@id":f"{SITE_URL}/#clinic"}}

def ld_breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":f"{SITE_URL}/{h}" if h!='index.html' else SITE_URL+"/"} for i,(n,h) in enumerate(items)]}

def ld_faq(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>','',a)}} for q,a in faqs]}

def ld_medpage(page, reviewer):
    d = {"@context":"https://schema.org","@type":"MedicalWebPage","@id":f"{SITE_URL}/{page['file']}#page","name":page['title'],"url":f"{SITE_URL}/{page['file']}","inLanguage":"ko",
         "lastReviewed":page.get('reviewed', TODAY),"dateModified":TODAY,"isPartOf":{"@id":f"{SITE_URL}/#website"},"about":{"@type":"MedicalProcedure","name":page.get('h1',page['title'])},
         "audience":{"@type":"MedicalAudience","audienceType":"환자","geographicArea":{"@type":"AdministrativeArea","name":"경기도 시흥시"}},
         "speakable":{"@type":"SpeakableSpecification","cssSelector":["h1",".page-hero .lead",".tx-summary"]}}
    if reviewer: d["reviewedBy"] = {"@id": f"{SITE_URL}/doctor-{reviewer}.html#person"}
    return d

def layout(page, body, extra_ld=None, current=None):
    file = page['file']; current = current or file
    pre = '../' if '/' in file else ''
    title = page['title'] if file!='index.html' else page['title']
    desc = page['description']
    canonical = SITE_URL + '/' if file=='index.html' else f"{SITE_URL}/{file}"
    og_img = f"{SITE_URL}/assets/img/og.jpg"
    lds = [ld_org(), ld_website()] + (extra_ld or [])
    ld_html = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    noindex = '<meta name="robots" content="noindex,follow">' if page.get('noindex') else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">'
    ai_summary = esc(page.get('ai_summary', desc))
    out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{noindex}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:alt" content="{esc(NAME)} — 시흥 정왕동 성담스퀘어 5층">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="KR-41">
<meta name="geo.placename" content="시흥시 정왕동, 경기도">
<meta name="ai-summary" content="{ai_summary}">
<meta name="medical-content" content="이 페이지의 의료 정보는 바로드림치과의원 시화점 전문의가 검토합니다. 치료 결과는 개인의 구강 상태에 따라 다를 수 있습니다.">
<meta name="theme-color" content="#454C56">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;600&display=swap">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/site.css">
{ld_html}
<!-- Google Tag Manager (컨테이너 ID 발급 후 교체) -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="hdr"><div class="topbar"><div class="wrap"><span>수요일 야간진료 21:00까지</span><span>토요일 진료</span><a href="tel:{TEL}" data-ev="contact_call">{TEL}</a></div></div><div class="wrap">
  <a class="logo" href="index.html" aria-label="{esc(NAME)} 홈"><img src="{LOGO}" alt="바로드림치과 로고" width="76" height="44" fetchpriority="high" decoding="async"><span>시화점</span></a>
  <nav aria-label="주요 메뉴">{nav_html(current)}</nav>
  <div style="display:flex;gap:8px;align-items:center">
    <a class="btn btn-p btn-sm hdr-tel" href="tel:{TEL}" data-ev="contact_call" aria-label="전화 {TEL}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8.1 9.7a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.6 2.6.7a2 2 0 0 1 1.9 2z"/></svg><span class="t" style="margin-left:6px">{TEL}</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" aria-label="메뉴 열기"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
  {drawer_html()}
</div></header>
<main id="main">
{body}
<section class="cta"><div class="wrap"><div><h2>상담 시 어떤 것부터 물어보고 싶으세요?</h2><p>전화로 물어보셔도 되고, 카카오톡으로 남겨 두셔도 됩니다. 설명만 듣고 돌아가셔도 괜찮습니다.</p></div><div class="btns"><a class="btn btn-p" href="tel:{TEL}" data-ev="contact_call">전화 {TEL}</a><a class="btn btn-s" href="{SITE.get('kakao_url','#')}" data-ev="contact_kakao" rel="noopener">카카오톡 상담</a><a class="btn btn-s" href="{SITE['naver_place'].get('url') or '#'}" data-ev="contact_naver" rel="noopener">네이버 예약</a></div></div></section>
</main>
<footer class="ftr"><div class="wrap">
{footer_menu_html()}
<div class="ftr-info"><b>{esc(NAME)}</b>{esc(ADDR)} · 전화 <a href="tel:{TEL}" style="color:#E6E8EB" data-ev="contact_call">{TEL}</a> · 대표 이진학 · 사업자등록번호 {esc(SITE.get('biz_no','[확인 후 기재]'))}<br>
<span class="legal">치료 결과는 개인의 구강 상태에 따라 다를 수 있습니다. 일부 설명 그림은 AI로 제작한 일러스트입니다. <a href="privacy.html">개인정보처리방침</a> · <a href="fees.html">비급여 안내</a> · <a href="sitemap.xml">사이트맵</a> · © {TODAY[:4]} {esc(NAME)}</span></div>
</div></footer>
<nav class="mbar" aria-label="빠른 연락"><a href="tel:{TEL}" data-ev="contact_call">전화</a><a href="{SITE.get('kakao_url','#')}" data-ev="contact_kakao" rel="noopener">카카오톡</a><a href="{SITE['naver_place'].get('url') or '#'}" data-ev="contact_naver" rel="noopener">네이버 예약</a></nav>
<script src="assets/js/site.js" defer></script>
</body>
</html>'''
    if pre:
        out = re.sub(r'(href|src)="(?!https?:|tel:|mailto:|#|\.\./)([A-Za-z0-9_\-]+\.(?:html|css|js|png|jpg|svg|xml|txt)|assets/|dictionary/)', lambda m: f'{m.group(1)}="{pre}{m.group(2)}', out)
    return out

def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(s)

def page_hero(page, crumbs):
    c = ' › '.join(f'<a href="{h}">{n}</a>' for n,h in crumbs[:-1]) + (' › ' if len(crumbs)>1 else '') + crumbs[-1][0]
    lead = f'<p class="lead">{page["lead"]}</p>' if page.get('lead') and page.get('lead')!=page.get('summary') else ''
    return f'<div class="page-hero"><div class="wrap"><div class="crumb">{c}</div><h1>{esc(page["h1"])}</h1>{lead}</div></div>'

def faq_html(faqs, h2='자주 묻는 질문'):
    if not faqs: return ''
    items = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q,a in faqs)
    return f'<section class="sec-alt sec"><div class="wrap"><h2 style="margin-bottom:20px">{h2}</h2><div class="faq" style="max-width:820px">{items}</div></div></section>'

DOCTOR_NAMES = {'lee':'이진학 원장(통합치의학과 전문의)','han':'한지상 원장(통합치의학과 전문의)','ko':'고수연 원장(치과보존과 전문의)'}

def render_treatment(t):
    crumbs = [('홈','index.html'),(t['category'], t['category_href']),(t['h1'], t['file'])]
    warn = f'<div class="notice notice-strong" style="margin-bottom:32px"><h2>{esc(t["warn"][0])}</h2><p>{t["warn"][1]}</p></div>' if t.get('warn') else ''
    who = ''.join(f'<li>{w}</li>' for w in t['who'])
    steps = ''.join(f'<li><b>{esc(s[0])}</b>{s[1]}</li>' for s in t['steps'])
    cautions = ''.join(f'<li>{c}</li>' for c in t['cautions'])
    related = ''.join(f'<a href="{h}">{l}</a>' for l,h in t.get('related',[]))
    body = page_hero(t, crumbs) + f'''
<section class="sec"><div class="wrap"><div class="grid g5-7">
  <div><figure>{t.get('figure','<div class="ph" style="aspect-ratio:4/3">[설명 일러스트 또는 실제 사진 자리]</div>')}</figure></div>
  <div class="prose">
    {warn}
    <p class="tx-summary" style="font-size:18px">{t['summary']}</p>
    <h2>어떤 치료인가요</h2>
    {''.join(f'<p>{p}</p>' for p in t['what'])}
    <h2>이런 분께 해당될 수 있습니다</h2>
    <ul>{who}</ul>
    <h2>치료 과정</h2>
    <ol class="steps">{steps}</ol>
    <h2>미리 알아 두실 점</h2>
    <ul>{cautions}</ul>
    <p class="small muted">치료 방법과 기간, 결과는 개인의 구강 상태와 전신 건강에 따라 다릅니다. 검사 후 설명을 들으신 뒤 결정하셔도 됩니다.</p>
    <div class="tx-meta"><span>작성 {esc(NAME)}</span><span>검토 {DOCTOR_NAMES[t['reviewer']]}</span><span>최종 확인 {t.get('reviewed', TODAY)}</span></div>
    {('<h3 style="margin-top:32px">함께 보면 좋은 페이지</h3><div class="related">'+related+'</div>') if related else ''}
  </div>
</div></div></section>
''' + faq_html(t['faq'], f'{esc(t["h1"])} 자주 묻는 질문')
    lds = [ld_breadcrumb(crumbs), ld_medpage(t, t['reviewer']), ld_faq(t['faq'])]
    return layout(t, body, lds)

def main():
    files = []
    # 홈
    home = HOME(SITE, hours_strip, hours_table)
    write('index.html', layout(home['page'], home['body'], [ld_faq(home['faq'])] , 'index.html')); files.append(('index.html', '1.0', 'weekly'))
    # 치료 페이지
    for t in TREATMENTS:
        write(t['file'], render_treatment(t)); files.append((t['file'], '0.8', 'monthly'))
    # 정적 페이지
    for p in STATIC_PAGES(SITE, hours_table, page_hero, faq_html, ld_breadcrumb, ld_faq):
        write(p['file'], layout(p, p['body'], p.get('ld', [])))
        if not p.get('noindex'): files.append((p['file'], p.get('prio','0.6'), 'monthly'))
    for p in build_doctor_pages(SITE, page_hero, ld_breadcrumb, SITE_URL):
        write(p['file'], layout(p, p['body'], p.get('ld', []))); files.append((p['file'], '0.7', 'monthly'))
    # 지역·증상 페이지
    for a in AREA:
        r = render_area(a, SITE, page_hero, hours_table, ld_breadcrumb, ld_faq, faq_html)
        write(a['file'], layout(r['page'], r['body'], r['ld'])); files.append((a['file'], r['prio'], 'monthly'))
    for sy in SYMPTOM:
        r = render_symptom(sy, SITE, page_hero, ld_breadcrumb, ld_faq, faq_html, ld_medpage, DOCTOR_NAMES)
        write(sy['file'], layout(r['page'], r['body'], r['ld'])); files.append((sy['file'], r['prio'], 'monthly'))
    r = render_symptom_index(SITE, page_hero, ld_breadcrumb)
    write('symptoms.html', layout(r['page'], r['body'], r['ld'])); files.append(('symptoms.html', r['prio'], 'monthly'))
    # 용어사전
    for t in DICT.TERMS:
        r = DICT.render_term(t, SITE, page_hero, ld_breadcrumb, ld_faq, faq_html, ld_medpage, DOCTOR_NAMES, SITE_URL)
        write(r['page']['file'], layout(r['page'], r['body'], r['ld'])); files.append((r['page']['file'], r['prio'], 'monthly'))
    r = DICT.render_index(SITE, page_hero, ld_breadcrumb)
    r['ld'][1] = json.loads(json.dumps(r['ld'][1], ensure_ascii=False).replace('{SITE_URL}', SITE_URL))
    write(r['page']['file'], layout(r['page'], r['body'], r['ld'])); files.append((r['page']['file'], r['prio'], 'weekly'))
    # sitemap / robots / llms
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{SITE_URL + "/" if f=="index.html" else SITE_URL+"/"+f}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n' for f,p,c in files) + '</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'''User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Yeti
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
''')
    docs = SITE['doctors']
    dict_lines = ''.join(f"- [{t['term']}]({SITE_URL}/dictionary/{t['slug']}.html): {t['one']}\n" for t in DICT.TERMS)
    area_lines = ''.join(f"- [{a['kw']}]({SITE_URL}/{a['file']})\n" for a in AREA)
    sym_lines = ''.join(f"- [{sy['h1']}]({SITE_URL}/{sy['file']}): {sy['q']}\n" for sy in SYMPTOM)
    tx_lines = ''.join(f"- [{t['h1']}]({SITE_URL}/{t['file']}): {re.sub(r'<[^>]+>','',t['summary'])}\n" for t in TREATMENTS)
    write('llms.txt', f'''# {NAME}

> 경기 시흥시 정왕동 성담스퀘어 5층 518호에 있는 치과의원. 통합치의학과 전문의 2인(이진학·한지상)과 치과보존과 전문의 1인(고수연)이 진료합니다. 임플란트, 의식하진정법(흔히 수면치료라 부름), 충치·신경·잇몸치료, 심미치료, 턱관절 치료를 진료합니다. 수요일 야간진료(21:00까지), 토요일 진료(14:00까지), 일요일·공휴일 휴진.

## 기본 정보
- 상호: {NAME} (법인명 {SITE['legal_name']})
- 주소: {ADDR} (지번 {SITE['address']['jibun']}, 우편번호 {SITE['address']['postal_code']})
- 전화: {TEL}
- 진료시간: 월·화·목·금 10:00–19:00 / 수 10:00–21:00(야간진료) / 토 10:00–14:00 / 점심 13:00–14:00 / 일·공휴일 휴진 / 접수 마감은 진료 종료 1시간 전
- 의료진: 이진학 대표원장(통합치의학과 전문의), 한지상 원장(통합치의학과 전문의), 고수연 원장(치과보존과 전문의)
- 같은 그룹의 다른 지점: 바로드림치과 안산점(barodreamdental.kr) — 별도 의료기관입니다. 이 사이트는 시화점만 다룹니다.

## 주요 페이지
- [홈]({SITE_URL}/)
- [병원 소개]({SITE_URL}/about.html)
- [의료진]({SITE_URL}/doctors.html)
- [진료시간·오시는 길]({SITE_URL}/location.html)
- [자주 묻는 질문]({SITE_URL}/faq.html)
- [비급여 안내]({SITE_URL}/fees.html)

## 진료 안내
{tx_lines}
## 지역 안내
{area_lines}
## 치과 용어사전 ({len(DICT.TERMS)}개)
- [용어사전 전체]({SITE_URL}/dictionary/index.html)
{dict_lines}
## 증상으로 찾기
{sym_lines}
## 용어
- 의식하진정법: 흔히 "수면치료", "수면임플란트"라고 부르지만 정확한 이름은 의식하진정법입니다. 적용 가능 여부는 건강 상태에 따라 상담에서 확인합니다.
- 즉시로딩: 임플란트를 심은 당일 또는 며칠 안에 임시 치아를 연결하는 방법으로, 모든 분께 적용되는 방법이 아닙니다.

## 주의
치료 결과는 개인의 구강 상태에 따라 다를 수 있습니다. 이 사이트는 치료 효과를 보장하지 않습니다.
''')
    print(f'built {len(files)} indexable pages → {SITE_URL}')

if __name__ == '__main__':
    main()
