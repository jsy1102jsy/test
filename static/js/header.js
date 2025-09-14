function createHeader(isLogin) {
  const headerDiv = document.getElementById('header');
  headerDiv.innerHTML = ''; // 기존 내용 초기화

  // ===== 로고 (왼쪽) =====
  const logo = document.createElement('img');
  logo.src = '/static/images/Match_Ball.png';
  logo.alt = 'LOGO';
  logo.className = 'circle-img';

  // 로고를 클릭 가능한 링크로 만들기
  const logoLink = document.createElement('a');
  logoLink.href = '/';
  logoLink.appendChild(logo);

  const logoWrapper = document.createElement('div');
  logoWrapper.className = 'header-left';
  logoWrapper.appendChild(logoLink);

  // ===== 가운데 버튼들 =====
  const centerNav = document.createElement('div');
  centerNav.className = 'header-center';

  const makeButtonLink = (text, href) => {
    const a = document.createElement('a');
    a.href = href;
    const btn = document.createElement('button');
    btn.textContent = text;
    a.appendChild(btn);
    return a;
  };

  // 홈 버튼 제거
  centerNav.appendChild(makeButtonLink('팀', '/teamlist'));

  if (isLogin) {
    centerNav.appendChild(makeButtonLink('글쓰기', '/board'));
  }

  // ===== 오른쪽 버튼들 =====
  const rightNav = document.createElement('div');
  rightNav.className = 'header-right';

  if (isLogin) {
    rightNav.appendChild(makeButtonLink('내 정보', '/mypage'));
    rightNav.appendChild(makeButtonLink('로그아웃', '/logout'));
  } else {
    rightNav.appendChild(makeButtonLink('로그인', '/login'));
    rightNav.appendChild(makeButtonLink('회원가입', '/register'));
  }

  // ===== 최종 구조 추가 =====
  headerDiv.appendChild(logoWrapper);
  headerDiv.appendChild(centerNav);
  headerDiv.appendChild(rightNav);
}
