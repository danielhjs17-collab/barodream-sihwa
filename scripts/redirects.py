"""data/redirects.csv → 호스팅별 리다이렉트 파일 생성.

  _redirects  : Cloudflare Pages / Netlify 용 (진짜 301)
  .htaccess   : 가비아·카페24 등 Apache 호스팅 용 (진짜 301)
  theme/hp005/page/*.html 는 만들지 않는다 — GitHub Pages 는 .php 경로에 301 을 줄 수 없음.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / 'data' / 'redirects.csv', encoding='utf-8')))

# 1) Cloudflare Pages / Netlify
lines = ['# 옛 공용 사이트(baro-dream.co.kr) 주소 → 지점별 새 페이지', '# 형식: 옛경로  목적지  상태코드', '']
for r in rows:
    if r['code'] == '410':
        tgt = r['old_path'] + ('*' if r['old_path'].endswith('/') else '')
        lines.append(f"{tgt}  /410.html  410")
    else:
        lines.append(f"{r['old_path']}  {r['destination']}  301")
# 옛 그누보드 쿼리형 접근(/?pid=...)과 /theme/ 하위 기타 파일은 홈으로
lines += ['', '/theme/*  /  301', '/page.php  /  301']
(ROOT / '_redirects').write_text('\n'.join(lines) + '\n', encoding='utf-8')

# 2) Apache .htaccess
ht = ['RewriteEngine On', '', '# 옛 공용 사이트 주소 → 지점별 새 페이지 (301)']
for r in rows:
    path = r['old_path'].lstrip('/').replace('.', r'\.')
    if r['code'] == '410':
        ht.append(f"RewriteRule ^{path} - [G,L]")
    else:
        ht.append(f"RewriteRule ^{path}$ {r['destination']} [R=301,L]")
ht += ['', '# 나머지 옛 테마 경로는 홈으로', r'RewriteRule ^theme/ / [R=301,L]', r'RewriteRule ^page\.php$ / [R=301,L]',
       '', 'ErrorDocument 404 /404.html', 'ErrorDocument 410 /410.html']
(ROOT / '.htaccess').write_text('\n'.join(ht) + '\n', encoding='utf-8')

# 3) 410 안내 페이지
(ROOT / '410.html').write_text('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>이 페이지는 더 이상 운영하지 않습니다 | 바로드림치과의원 시화점</title>
<style>body{font-family:Pretendard,system-ui,sans-serif;background:#F8F6F2;color:#2F343B;margin:0;display:grid;place-items:center;min-height:100vh;padding:24px}
main{max-width:520px}h1{font-size:22px;margin:0 0 12px}p{line-height:1.7;color:#5B616A}a{color:#8A5F05;font-weight:600}</style></head>
<body><main><h1>이 페이지는 더 이상 운영하지 않습니다</h1>
<p>회원 가입·로그인 기능은 종료되었습니다. 진료 문의는 전화 031-498-2282 로 주시면 됩니다.</p>
<p><a href="/">바로드림치과의원 시화점 첫 화면으로</a></p></main></body></html>
''', encoding='utf-8')

# 4) 사람이 읽는 표
by = {}
for r in rows: by.setdefault(r['branch'], []).append(r)
print('지점별 배분:', {k: len(v) for k, v in by.items()})
