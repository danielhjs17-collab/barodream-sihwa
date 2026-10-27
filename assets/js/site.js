// 바로드림치과의원 시화점 — 보조 스크립트 (본문 내용은 모두 HTML에 있음; 이 파일은 메뉴 열기와 클릭 이벤트만 담당)
(function () {
  var btn = document.querySelector('.menu-btn');
  var drawer = document.getElementById('drawer');
  if (btn && drawer) {
    btn.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) { drawer.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
  }
  // GA4/GTM 전환 이벤트: 전화·카카오·네이버 클릭 (안산점과 같은 이벤트 이름)
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-ev]');
    if (!a) return;
    window.dataLayer.push({ event: a.getAttribute('data-ev'), link_url: a.getAttribute('href') || '', page_path: location.pathname });
  });
})();
