// 알림 팝업 토글 함수
function toggleAlarmPopup() {
  const popup = document.getElementById('alarm-popup');
  if (popup) {
    popup.classList.toggle('visible');
  }
}

// 헤더 생성 함수
function createHeader(isLogin,) {
  const headerDiv = document.getElementById('header');
  headerDiv.innerHTML = ''; // 기존 내용 초기화

  // ===== 로고 (왼쪽) =====
  const logo = document.createElement('img');
  logo.src = '/static/images/Match_Ball.png';
  logo.alt = 'LOGO';
  logo.className = 'circle-img';

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

  centerNav.appendChild(makeButtonLink('팀', '/teamlist'));

  if (isLogin) {
    centerNav.appendChild(makeButtonLink('글쓰기', '/board'));
    centerNav.appendChild(makeButtonLink('경기목록', '/matchlist'));
  }

  // ===== 오른쪽 버튼들 =====
  const rightNav = document.createElement('div');
  rightNav.className = 'header-right';

  if (isLogin) {
    // 알림 버튼 (링크 제거하고 이벤트 처리)
    const alarmBtn = document.createElement('button');
    alarmBtn.textContent = '🔔';
    alarmBtn.addEventListener('click', toggleAlarmPopup);

    rightNav.appendChild(alarmBtn);
    rightNav.appendChild(makeButtonLink('내 정보', '/mypage'));
    const logoutBtn = document.createElement('button');
    logoutBtn.textContent = '로그아웃';
    logoutBtn.onclick = () => {
      window.location.href = '/logout';  // 로그아웃 요청
      setTimeout(() => window.location.reload(), 300); // 약간의 지연 후 새로고침
    };
    rightNav.appendChild(logoutBtn);
  } else {
    rightNav.appendChild(makeButtonLink('로그인', '/login'));
    rightNav.appendChild(makeButtonLink('회원가입', '/register'));
  }

  // ===== 최종 구조 조립 =====
  headerDiv.appendChild(logoWrapper);
  headerDiv.appendChild(centerNav);
  headerDiv.appendChild(rightNav);

  // ===== 알림 팝업이 없다면 body에 추가 =====
  if (!document.getElementById('alarm-popup')) {
    const popup = document.createElement('div');
    popup.id = 'alarm-popup';
    popup.className = 'alarm-popup';
    popup.innerHTML = `
      <p><strong>알림</strong></p>
      <ul>
        <li>⚽ 새 팀이 등록되었습니다!</li>
        <li>📢 새로운 게시글이 올라왔어요.</li>
      </ul>
      <button id="alarm-more-btn" style="width:100%;margin-top:10px;padding:8px 0;background:#333;color:#fff;border:none;border-radius:4px;cursor:pointer;">알림 더보기</button>
    `;
    document.body.appendChild(popup);
    // 알림 더보기 버튼 이벤트
    document.getElementById('alarm-more-btn').onclick = function() {
      window.location.href = '/alarm';
    };
  }
}
