/* --- 전역 변수 및 데이터 --- */
let currentStep = 0;

const leagues = ["EPL", "K 리그", "KBO", "F1"];
const teams = {
    "EPL": ["맨체스터 시티", "리버풀", "아스날", "뉴캐슬 유나이티드", "첼시", "맨체스터 유나이티드", "토트넘 홋스퍼", "아스톤 빌라", "브라이튼", "웨스트햄 유나이티드", "울버햄튼 원더러스", "크리스탈 팰리스"],
    "K리그": ["울산 HD FC", "전북 현대 모터스", "FC 서울", "포항 스틸러스", "광주FC", "인천 유나이티드", "수원 삼성 블루윙즈", "강원FC", "제주 유나이티드", "대전 하나 시티즌", "대구FC", "FC안양"],
    "KBO": ["LG 트윈즈", "삼성 라이온즈", "기아 타이거즈", "SSG 랜더스", "롯데 자이언츠", "NC 다이노스", "두산 베어스", "키움 히어로즈", "한화 이글스", "KT 위즈"],
    "F1": ["레드불", "페라리", "메르세데스", "맥라렌", "애스턴 마틴", "알파인", "윌리엄스", "레이싱 불스", "하스", "자우버"]
};

// ✅ 팀 로고 이미지 매핑 (데이터베이스 JSON의 team_name과 정확히 일치해야 합니다)
const TEAM_LOGO_MAP = {
    // EPL
    "리버풀": "../images/EPL/리버풀.png",
    "맨체스터 시티": "../images/EPL/맨체스터 시티.png",
    "맨체스터 유나이티드": "../images/EPL/맨체스터 유나이티드.png",
    "아스날": "../images/EPL/아스날.png",
    "아스톤 빌라": "../images/EPL/아스톤 빌라.png",
    "첼시": "../images/EPL/첼시.png",
    "토트넘 홋스퍼": "../images/EPL/토트넘 홋스퍼.png",
    "브라이튼": "../images/EPL/브라이튼.png",
    "웨스트햄 유나이티드": "../images/EPL/웨스트햄 유나이티드.png",
    "울버햄튼 원더러스": "../images/EPL/울버햄튼 원더러스.png",
    "크리스탈 팰리스": "../images/EPL/크리스탈 팰리스.png",
    "뉴캐슬 유나이티드": "../images/EPL/뉴캐슬 유나이티드.png",

    // K리그
    "울산 HD FC": "../images/kleague/울산 HD FC.png",
    "전북 현대 모터스": "../images/kleague/전북 현대 모터스.png",
    "FC 서울": "../images/kleague/FC 서울.png",
    "포항 스틸러스": "../images/kleague/포항 스틸러스.png",
    "광주FC": "../images/kleague/광주FC.png",
    "인천 유나이티드 FC": "../images/kleague/인천 유나이티드.png",
    "수원 삼성 블루윙즈": "../images/kleague/수원 삼성 블루윙즈.png",
    "강원 FC": "../images/kleague/강원FC.png",
    "제주 SK FC": "../images/kleague/제주 SK FC.png",
    "대전 하나 시티즌": "../images/kleague/대전 하나 시티즌.png",
    "대구FC": "../images/kleague/대구FC.png",
    "FC안양": "../images/kleague/FC안양.png",

    // KBO
    "LG 트윈즈": "../images/kbo/LG 트윈즈.png",
    "삼성 라이온즈": "../images/kbo/삼성 라이온즈.png",
    "기아 타이거즈": "../images/kbo/기아 타이거즈.png",
    "SSG 랜더스": "../images/kbo/SSG 랜더스.png",
    "롯데 자이언츠": "../images/kbo/롯데 자이언츠.png",
    "NC 다이노스": "../images/kbo/NC 다이노스.png",
    "두산 베어스": "../images/kbo/두산 베어스.png",
    "키움 히어로즈": "../images/kbo/키움 히어로즈.png",
    "한화 이글스": "../images/kbo/한화 이글스.png",
    "KT 위즈": "../images/kbo/KT 위즈.png",

    // F1
    "레드불": "../images/logos/f1/레드불.png",
    "메르세데스": "../images/logos/f1/메르세데스.png",
    "페라리": "../images/logos/f1/페라리.png",
    "맥라렌": "../images/logos/f1/맥라렌.png",
    "애스턴 마틴": "../images/logos/f1/애스턴 마틴.png",
    "알핀": "../images/logos/f1/알핀.png",
    "윌리엄스": "../images/logos/f1/윌리엄스.png",
    "레이싱 불스": "../images/logos/f1/레이싱 불스.png",
    "하스": "../images/logos/f1/하스.png",
    "자우버": "../images/logos/f1/자우버.png",
};

const leagueDetailData = {
    /* --------------------------------- */
    /* --------- 정보 수정 필요 --------- */
    /* --------------------------------- */
    'EPL': {
        desc: '세계 최고의 축구 리그 프리미어리그',
        color: '#38003c',
        bgImg: '../images/리버풀 vs 맨시티.png',
        stats: { teams: '20개 팀', progress: '20라운드 진행 중', avgFans: '38,124명' },
        rank: [
            ['1', '리버풀', '20', '14', '3', '3', '45'],
            ['2', '맨시티', '20', '13', '4', '3', '43'],
            ['3', '아스널', '20', '12', '4', '4', '40']
        ],
        players: [
            { name: '엘링 홀란', team: '맨시티', stats: '14골 4도움', img: '⚽' },
            { name: '모하메드 살라', team: '리버풀', stats: '12골 7도움', img: '⚽' },
            { name: '손흥민', team: '토트넘', stats: '11골 5도움', img: '⚽' }
        ],
        highlights: [
            { file: '../images/EPL/EPL 하이라이트 1.png', time: '04:54' },
            { file: '../images/EPL/EPL 하이라이트 2.png', time: '03:57' },
            { file: '../images/EPL/EPL 하이라이트 3.png', time: '03:33' },
            { file: '../images/EPL/EPL 하이라이트 4.png', time: '04:30' },
            { file: '../images/EPL/EPL 하이라이트 5.png', time: '03:26' },
            { file: '../images/EPL/EPL 하이라이트 6.png', time: '06:49' }
        ]
    },
    'K리그': {
        desc: '다이나믹한 한국 축구의 정수',
        color: '#02234b',
        bgImg: '../images/울산 vs 서울.png',
        stats: { teams: '12개 팀', progress: '시즌 종료', avgFans: '10,551명' },
        rank: [
            ['1', '울산', '38', '23', '7', '8', '76'],
            ['2', '포항', '38', '16', '16', '6', '64'],
            ['3', '광주', '38', '16', '11', '11', '59']
        ],
        players: [
            { name: '주민규', team: '울산', stats: '17골 2도움', img: '🇰🇷' },
            { name: '세징야', team: '대구', stats: '8골 5도움', img: '🇧🇷' },
            { name: '이승우', team: '전북', stats: '10골 3도움', img: '🇰🇷' }
        ],
        highlights: [
            { file: '../images/kleague/k리그 하이라이트 1.png', time: '04:54' },
            { file: '../images/kleague/k리그 하이라이트 2.png', time: '03:57' },
            { file: '../images/kleague/k리그 하이라이트 3.png', time: '03:33' },
            { file: '../images/kleague/k리그 하이라이트 4.png', time: '04:30' },
            { file: '../images/kleague/k리그 하이라이트 5.png', time: '03:26' },
            { file: '../images/kleague/k리그 하이라이트 6.png', time: '06:49' }
        ]
    },
    'KBO': {
        desc: '심장을 뛰게 하는 뜨거운 함성, KBO 리그',
        color: '#041e42',
        bgImg: '../images/SSG vs 롯데.png',
        stats: { teams: '10개 팀', progress: '정규 시즌 종료', avgFans: '15,000명' },
        rank: [
            ['1', '기아', '144', '87', '2', '55', '0.613'],
            ['2', '삼성', '144', '78', '2', '64', '0.549'],
            ['3', 'LG', '144', '76', '2', '66', '0.535']
        ],
        players: [
            { name: '김도영', team: '기아', stats: '38홈런 40도루', img: '⚾' },
            { name: '구자욱', team: '삼성', stats: '33홈런 115타점', img: '⚾' },
            { name: '양의지', team: '두산', stats: '17홈런 94타점', img: '⚾' }
        ],
        highlights: [
            { file: '../images/KBO/KBO 하이라이트 1.png', time: '04:54' },
            { file: '../images/KBO/KBO 하이라이트 2.png', time: '03:57' },
            { file: '../images/KBO/KBO 하이라이트 3.png', time: '03:33' },
            { file: '../images/KBO/KBO 하이라이트 4.png', time: '04:30' },
            { file: '../images/KBO/KBO 하이라이트 5.png', time: '03:26' },
            { file: '../images/KBO/KBO 하이라이트 6.png', time: '06:49' }
        ]
    },
    'F1': {
        desc: '지상 최고의 속도 전쟁, 포뮬러 원',
        color: '#e10600',
        bgImg: '../images/벤츠 vs 레드불.png',
        stats: { teams: '10개 팀', progress: '24개 그랑프리 진행', avgFans: '300,000명+' },
        rank: [
            ['1', '베르스타펜', '22', '15', '4', '2', '575'],
            ['2', '노리스', '22', '3', '12', '5', '331'],
            ['3', '르클레르', '22', '3', '11', '6', '307']
        ],
        players: [
            { name: '막스 베르스타펜', team: '레드불', stats: '챔피언 포인트 1위', img: '🏎️' },
            { name: '루이스 해밀턴', team: '메르세데스', stats: '통산 103승 기록', img: '🏎️' },
            { name: '샤를 르클레르', team: '페라리', stats: '모나코 GP 우승', img: '🏎️' }
        ],
        highlights: [
            { file: '../images/F1/F1 하이라이트 1.png', time: '04:54' },
            { file: '../images/F1/F1 하이라이트 2.png', time: '03:57' },
            { file: '../images/F1/F1 하이라이트 3.png', time: '03:33' },
            { file: '../images/F1/F1 하이라이트 4.png', time: '04:30' },
            { file: '../images/F1/F1 하이라이트 5.png', time: '03:26' },
            { file: '../images/F1/F1 하이라이트 6.png', time: '06:49' }
        ]
    }
};

/* --------------------------------- */
/* --------- 정보 수정 필요 --------- */
/* --------------------------------- */


/* --- [1] 초기화 (하이라이트 생성 및 초기 라이브 설정) --- */
function init() {
    // 하이라이트 생성
    const container = document.getElementById('highlights-container');
    if (container) {
        container.innerHTML = "";
        Object.keys(leagueDetailData).forEach(id => {
            const h3 = document.createElement('h3');
            h3.innerText = `${id} 하이라이트`;
            h3.style.margin = "40px 50px 20px";
            container.appendChild(h3);

            const row = document.createElement('div');
            row.className = 'highlight-row';

            const customImages = leagueDetailData[id].highlights || [];

            for (let i = 1; i <= 6; i++) {
                let thumbUrl, videoTime;

                if (i <= customImages.length) {
                    if (customImages[i - 1].file.startsWith('http') || customImages[i - 1].file.startsWith('..')) {
                        thumbUrl = customImages[i - 1].file;
                    } else {
                        thumbUrl = `../images/highlights/${customImages[i - 1].file}`;
                    }
                    videoTime = customImages[i - 1].time || "03:00";
                } else {
                    thumbUrl = `https://picsum.photos/seed/${id}${i}/300/170`;
                    videoTime = `0${Math.floor(Math.random() * 5 + 3)}:${Math.floor(Math.random() * 50 + 10)}`;
                }

                row.innerHTML += `
          <div class="video-card">
            <div class="video-thumb" style="background-image: url('${thumbUrl}'); background-size: cover;">
              <div class="video-time">${videoTime}</div>
            </div>
            <p style="font-size:13px; margin-top:10px; color:#ccc;">${id} 하이라이트 #${i}</p>
          </div>
        `;
            }
            container.appendChild(row);
        });
    }

    // 리그 라이브 목록 초기 실행 (ALL)
    const firstTab = document.querySelector('.tab-btn');
    if (firstTab) filterLive('ALL', firstTab);
}

/* --- [2] 라이브 필터 기능 (목록 사라짐 방지) --- */
function filterLive(league, btn) {
    if (!btn) return;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const list = document.getElementById('live-list');
    if (!list) return;

    list.innerHTML = '';

    if (league === 'ALL') {
        const allLeagues = ['EPL', 'K리그', 'KBO', 'F1'];
        allLeagues.forEach(l => {
            for (let i = 1; i <= 3; i++) {
                list.innerHTML += `<div class="live-item-mini">${l} LIVE 중계 ${i}</div>`;
            }
        });
    } else {
        for (let i = 1; i <= 8; i++) {
            list.innerHTML += `<div class="live-item-mini">${league} LIVE 중계 ${i}</div>`;
        }
    }

    list.scrollTo({ left: 0, behavior: 'smooth' });
}

/* --- [3] 똑똑한 스크롤 함수 (상하단 독립) --- */
function scrollGrid(btn, direction) {
    const wrapper = btn.closest('.live-section-wrapper');
    const container = wrapper.querySelector('.carousel-track, .live-grid');
    if (!container) return;

    const isMain = container.classList.contains('carousel-track');

    if (isMain) {
        const cards = Array.from(container.children);
        const centerPoint = container.scrollLeft + (container.clientWidth / 2);

        let closestIndex = 0;
        let minDiff = Infinity;

        cards.forEach((card, index) => {
            const cardCenter = card.offsetLeft + (card.offsetWidth / 2);
            const diff = Math.abs(cardCenter - centerPoint);
            if (diff < minDiff) {
                minDiff = diff;
                closestIndex = index;
            }
        });

        let targetIndex = direction === 'left' ? closestIndex - 1 : closestIndex + 1;
        targetIndex = Math.max(0, Math.min(targetIndex, cards.length - 1));

        const targetCard = cards[targetIndex];
        const scrollTarget = targetCard.offsetLeft + (targetCard.offsetWidth / 2) - (container.clientWidth / 2);

        container.scrollTo({ left: scrollTarget, behavior: 'smooth' });

    } else {
        const scrollAmount = 640;
        container.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    }
}

/* --- [4] 화면 전환 & 모달 --- */
function openLeague(id) {
    const data = leagueDetailData[id] || leagueDetailData['EPL'];

    document.getElementById('home-view').classList.add('hidden');
    document.getElementById('about-view').classList.add('hidden');

    const detailView = document.getElementById('detail-view');
    detailView.classList.remove('hidden');

    const bgImg = data.bgImg || 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=2000';

    detailView.innerHTML = `
    <button class="back-btn" onclick="goHome()">❮</button>
    <div id="detail-hero" class="detail-hero"
      style="background: linear-gradient(to bottom, ${data.color}CC, var(--bg)), url('${bgImg}');
      background-size: cover; background-position: center;">
      <h1 id="detail-title" class="shimmer">${id}</h1>
      <div id="detail-desc">
        <p>${data.desc}</p>
        <div class="league-info-chips">
          <span>🏟️ ${data.stats?.teams || '20개 팀'}</span>
          <span>📅 ${data.stats?.progress || '시즌 진행 중'}</span>
          <span>👥 평균 ${data.stats?.avgFans || '30,000명'}</span>
        </div>
      </div>
    </div>

    <div class="detail-bottom-section">
      <div class="standing-section">
        <div class="section-header"><h3>리그 순위표</h3></div>
        <table>
          <thead>
            <tr><th>순위</th><th>팀명</th><th>경기</th><th>승/무/패</th><th>승점</th></tr>
          </thead>
          <tbody id="standing-body">
            ${data.rank.map(r => `
              <tr>
                <td>${r[0]}</td>
                <td class="team-name-cell"><b>${r[1]}</b></td>
                <td>${r[2]}</td>
                <td>${r[3] || '0'}/${r[4] || '0'}/${r[5] || '0'}</td>
                <td class="point-cell" style="color: ${data.color === '#FFFFFF' ? 'var(--primary)' : data.color}">
                  ${r[6] || r[3]}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <div class="player-section">
        <div class="section-header"><h3>주요 선수 명단</h3></div>
        <div class="player-column-grid">
          ${(data.players || []).map(p => `
            <div class="player-mini-card">
              <div class="player-avatar">${p.img}</div>
              <div class="player-info">
                <h4>${p.name}</h4>
                <p>${p.team} | <span style="color: ${data.color}">${p.stats}</span></p>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;

    window.scrollTo(0, 0);
}

function goHome() {
    document.getElementById('home-view').classList.remove('hidden');
    document.getElementById('detail-view').classList.add('hidden');
    document.getElementById('about-view').classList.add('hidden');

    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    document.querySelector('.nav-links a:first-child').classList.add('active');
}

function goAbout() {
    document.getElementById('home-view').classList.add('hidden');
    document.getElementById('detail-view').classList.add('hidden');
    document.getElementById('about-view').classList.remove('hidden');

    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    document.querySelector('a[href="#about"]').classList.add('active');

    renderAbout();
    window.scrollTo(0, 0);
}

function renderAbout() {
    if (document.getElementById('about-features').innerHTML !== "") return;

    const features = [
        { icon: '✨', title: 'AI 기반 팀 추천', desc: '머신러닝 알고리즘으로 성향을 분석합니다.' },
        { icon: '📊', title: '실시간 데이터', desc: '최신 경기 통계를 실시간으로 제공합니다.' },
        { icon: '❤️', title: '개인화된 경험', desc: '관심사에 맞춘 맞춤형 콘텐츠를 제공합니다.' },
        { icon: '⚡', title: '라이브 스트리밍', desc: '주요 리그 경기를 실시간 시청하세요.' }
    ];

    document.getElementById('about-features').innerHTML = features.map(f => `
    <div class="feature-card">
      <div class="feature-icon">${f.icon}</div>
      <h3>${f.title}</h3>
      <p>${f.desc}</p>
    </div>
  `).join('');
}

function openModal(isSignUp) {
    document.getElementById('auth-modal').classList.remove('hidden');
    if (isSignUp) toggleAuthMode(true);
}
function closeModal() {
    document.getElementById('auth-modal').classList.add('hidden');
}
function toggleAuthMode(forceSignUp) {
    const isSignUp = forceSignUp || document.getElementById('auth-submit').innerText === '로그인';
    document.getElementById('auth-submit').innerText = isSignUp ? '회원가입' : '로그인';
    document.getElementById('name-field').classList.toggle('hidden', !isSignUp);
    document.getElementById('toggle-btn').innerText = isSignUp ? '로그인' : '회원가입';
}


/* =========================================================
   [B] ✅ 최신 챗봇 로직 (6문항 + 리그→팀 + 서버호환 + 자동 스크롤)
========================================================= */

/* --- [상태] --- */
let followIndex = 0;
let scrollAnimationId = null;
let _chatScrollRAF = null;
/* --- [B-0] ✅ 부드러운 스크롤 유틸 (자연스럽게) --- */
// ✅ 채팅앱 스타일: 목표(맨 아래)를 "따라가는" 자연스러운 스크롤
function scrollChatToBottom() {
    const box = document.getElementById('chat-messages');
    if (!box) return;

    // 이미 진행 중이면 중복 실행 방지
    if (_chatScrollRAF) return;

    const maxFrames = 60;          // 안전장치(최대 1초 정도)
    let frame = 0;

    function step() {
        frame += 1;

        // 목표는 "항상 최신" 맨 아래 (콘텐츠가 늘어나도 자연스럽게 따라감)
        const target = box.scrollHeight - box.clientHeight;
        const current = box.scrollTop;
        const diff = target - current;

        // 거의 도착하면 종료
        if (Math.abs(diff) < 1 || frame >= maxFrames) {
            box.scrollTop = target;    // 마지막은 정확히 붙여주기
            _chatScrollRAF = null;
            return;
        }

        // ✅ 스프링 느낌의 감쇠 이동 (0.18~0.28 사이가 자연스러움)
        // diff가 크면 더 빨리, 작으면 천천히 -> “사람 손으로 미는 느낌”
        const k = Math.min(0.28, Math.max(0.18, Math.abs(diff) / 800));
        box.scrollTop = current + diff * k;

        _chatScrollRAF = requestAnimationFrame(step);
    }

    _chatScrollRAF = requestAnimationFrame(step);
}


/* --- [B-1] 챗봇 UI 유틸 --- */
function toggleChat() {
    const chat = document.getElementById('chat-window');
    chat.classList.toggle('hidden');

    if (!chat.classList.contains('hidden') && currentStep === 0) {
        startBotLogic();
        scrollChatToBottom();
    }
}

function addMsg(type, text) {
    const box = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `msg-bubble ${type}-msg`;
    div.innerText = text;
    box.appendChild(div);
    scrollChatToBottom();
}

function showOpts(opts, callback) {
    const container = document.getElementById('chat-options');
    container.innerHTML = '';

    opts.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'opt-btn';
        btn.innerText = opt;
        btn.onclick = () => {
            container.innerHTML = '';
            callback(opt);
            scrollChatToBottom();
        };
        container.appendChild(btn);
    });

    scrollChatToBottom();
}

/* --- [B-2] 챗봇 데이터 --- */
const chatData = {
    leagues: [
        { id: 'epl', name: '⚽ EPL', emoji: '🏴' },
        { id: 'kleague', name: '⚽ K리그', emoji: '🇰🇷' },
        { id: 'kbo', name: '⚾ KBO', emoji: '⚾' },
        { id: 'f1', name: '🏎️ 포뮬러 원', emoji: '🏁' }
    ],
};

// ✅ 라벨(사용자 선택) → 토큰(최종 query용) 매핑
const intentMapKleague = {
    fandom: {
        "열정적인 팬덤": ["열정적인 팬덤"],
        "높은 관중 동원력": ["전국구 팬덤"],
        "지역색 강함": ["축구 수도"],
        "팬 소통 강화": ["팬_소통_강화"],
        "라이벌·더비 문화": ["슈퍼매치"]
    },
    star: {
        "스타 플레이어가 있는": ["스타_군단"],
        "공격적인 축구": ["닥공"],
        "탄탄한 수비": ["짠물수비"],
        "유스·육성 시스템": ["유스명가"],
        "감독·전술 역량": ["전술적_혁신"]
    },
    story: {
        "명문 구단": ["K 리그 왕조"],
        "오랜 역사·전통": ["역사와 전통"],
        "우승·트로피 경험": ["아시아 챔피언"],
        "언더독·생존 서사": ["언더독의반란"],
        "도전·재건 스토리": ["감동적인 스토리"]
    },
    visual: {
        "팀 컬러·상징이 멋진": ["파검의피니셔"],
        "스타 마케팅·이슈메이킹": ["슈퍼스타 마케팅"],
        "패스·전개 축구가 예쁜": ["패스축구"],
        "원샷 원킬": ["클릭축구"],
        "매진·현장 분위기": ["매진_신화"]
    },
    capital: {
        "강력한 자본력": ["압도적 자본력"],
        "이적시장에 적극적인": ["이적 시장 큰손"],
        "구단 운영·비즈니스 역량": ["기업구단의_변신"],
        "인프라·미래 투자": ["축구 전용구장 추진"],
        "재정 제약·현실성": ["재정_한계"]
    }
};

// ✅ EPL 라벨 → 토큰 매핑
const intentMapEpl = {
    fandom: {
        "열정적인 팬덤": ["훌리건"],
        "높은 팬 충성도": ["높은 팬 충성도"],
        "글로벌 인기": ["한국_선수_인연"],
        "지역색 강함": ["홀트엔드"],
        "라이벌 문화": ["맨체스터 더비"]
    },

    star: {
        "스타 플레이어가 많은": ["손흥민_효과"],
        "공격적인 축구": ["공격 축구"],
        "압도적 전력": ["압도적 전력"],
        "젊은 스쿼드": ["유스_성장_모델"],
        "유럽 대항전 강자": ["유럽 대항전 강자"]
    },

    story: {
        "명문 구단": ["명문 구단"],
        "오랜 역사": ["오랜 역사"],
        "트로피가 많은": ["트레블 경험"],
        "언더독 반란 스토리": ["언더독반란"],
        "전설적인 시대 보유": ["퍼거슨 유산"]
    },

    visual: {
        "유니폼이 예쁜": ["스카이 블루"],
        "엠블럼이 멋진": ["사자엠블럼"],
        "홈구장이 인상적인": ["최첨단_경기장"],
        "도시 이미지가 매력적인": ["해변도시"],
        "젊고 트렌디한 이미지": ["하이 리스크"]
    },

    capital: {
        "강력한 자본력": ["오일 머니"],
        "이적시장에 적극적인": ["역대급 지출"],
        "프리미어리그 빅클럽": ["EPL 거인"],
        "상업적으로 성공한": ["세계 최고 수입"],
        "장기적으로 안정적인 운영": ["가성비"]
    }
};

// ✅ KBO intentMap (질문 key와 맞추기 위해 소문자)
// Visual이 4개라서 "홈구장/응원문화" 한 개를 보강했어.
const intentMapKBO = {
    fandom: {
        "열정적인 팬덤": ["열광적인 팬덤"],
        "높은 팬 충성도": ["최다 관중 기록"],
        "전국구 인기": ["전국구 인기"],
        "지역색 강함": ["호남 연고"],
        "라이벌리 문화": ["잠실 라이벌"]
    },

    star: {
        "스타 플레이어가 많은": ["류현진 복귀"],
        "강력한 전력": ["꾸준한 성적"],
        "강한 마운드": ["투수왕국"],
        "폭발적인 타선": ["슬러거 군단"],
        "육성과 성장형 팀": ["육성형 구단"]
    },

    story: {
        "명문 구단": ["야구 명문"],
        "오랜 역사": ["KBO 원년팀"],
        "트로피가 많은": ["V12"],
        "언더독 반란 스토리": ["29년 암흑기 탈출"],
        "전설적인 시대 보유": ["좌완 왕조"]
    },

    visual: {
        "유니폼과 색감이 매력적인": ["하얀 응원 물결"],
        "공격적인 야구 스타일": ["화끈한 공격"],
        "젊고 역동적인 이미지": ["젊은 에너지"],
        "데이터·전략 야구": ["데이터 야구"],
        // ✅ 보강(없으면 UI 버튼 4개만 떠서 질문 5개 통일감이 깨짐)
        "홈구장·응원문화가 인상적인": ["잠실 라이벌"]
    },

    capital: {
        "강력한 자본력": ["대기업 자본"],
        "FA 시장에 적극적인": ["스토브리그 승자"],
        "구단 인프라가 뛰어난": ["고척돔"],
        "리빌딩·리툴링 전략": ["리빌딩"],
        "상업적·브랜드 경쟁력": ["유통라이벌전"]
    }
};

// ✅ F1 intentMap (질문 key와 맞추기 위해 소문자)
const intentMapF1 = {
    fandom: {
        "열정적인 팬덤": ["열정적인 티포시"],
        "높은 팬 충성도": ["팬 소통 우수"],
        "글로벌 인기": ["넷플릭스 스타"],
        "지역색 강함": ["이탈리아의 자부심"],
        "라이벌리 문화": ["라이벌 페라리"]
    },

    star: {
        "스타 드라이버가 있는": ["스타 드라이버"],
        "공격적인 레이싱 스타일": ["공격적인 드라이빙"],
        "압도적 전력": ["챔피언 왕조"],
        "젊은 재능 중심": ["신인 발굴"],
        "성장형 팀": ["일관된 성장"]
    },

    story: {
        "명문 팀": ["F1 명가"],
        "오랜 역사": ["F1 창립 멤버"],
        "트로피가 많은": ["최다 우승 기록"],
        "언더독 반란 스토리": ["서프라이즈 우승"],
        "전설적인 시대 보유": ["과거의 영광"]
    },

    visual: {
        "리버리가 멋진": ["은빛화살"],
        "브랜드 이미지가 강한": ["압도적 브랜드 가치"],
        "트렌디한 이미지": ["넷플릭스 스타"],
        "캐릭터성이 강한 팀": ["군터 슈타이너"],
        "극적인 레이스 감성": ["하이 리스크 하이 리턴"]
    },

    capital: {
        "강력한 자본력": ["막대한 자본력"],
        "기술력이 강한": ["기술적우위"],
        "엔진 파워 중심": ["메르세데스 파워"],
        "효율적 운영": ["짠물 운영"],
        "대형 프로젝트 팀": ["신축 공장"]
    }
};


function getIntentMapByLeague(leagueId) {
    const maps = {
        kleague: intentMapKleague,
        epl: intentMapEpl,
        f1: intentMapF1,
        kbo: intentMapKBO // ✅ 추가
    };
    return maps[leagueId] || null;
}

let queryTokenSet = new Set();

function addTokens(intentMap, categoryKey, selectedLabel) {
    const tokens = intentMap?.[categoryKey]?.[selectedLabel] || [];
    // 🔍 선택 전 상태
    console.log("➕ addTokens 호출", {
        category: categoryKey,
        selectedLabel,
        tokens,
        before: Array.from(queryTokenSet)
    });

    tokens.forEach(t => queryTokenSet.add(t));

    // 🔍 선택 후 상태
    console.log("✅ queryTokenSet 누적 결과", Array.from(queryTokenSet));
}

/**
 * 사용자의 모든 응답을 종합하여 학습 모델용 자연어 쿼리를 생성합니다.
 * 좋아하는 팀 유무에 따라 서로 다른 문장 템플릿을 사용합니다.
 * @returns {Object} - favorite_team 및 구조화된 full_query 문장
 */

function buildFinalQuery() {
    // 1) Set에 모인 토큰을 배열로 변환
    const tokens = Array.from(queryTokenSet);

    // 2) 자연어 문장 만들기 (좋아하는 팀 유무에 따라 문장 다르게)
    const hasFav = userSelections.favoriteTeamExists === "yes";
    const favTeam = userSelections.favoriteTeam;

    // 3) 토큰을 보기 좋게 연결
    const tokenText = tokens.length > 0 ? tokens.join(", ") : "다양한 특징";

    // 4) 최종 자연어 쿼리(모델 입력용)
    // ⚠️ 기존에 선언되지 않은 starToken, capitalToken 등을 사용하던 버그를 수정했습니다.
    const full_query = hasFav && favTeam && favTeam !== "none"
        ? `저는 ${favTeam} 팬이고, ${tokenText} 같은 팀 컬러와 운영 스타일을 선호해요.`
        : `저는 ${tokenText} 같은 팀 컬러와 운영 스타일을 선호해요.`;

    // 5) 객체 형태로 반환
    return {
        tokens,        // ["토큰1", "토큰2", ...]
        full_query     // "저는 ... 선호합니다."
    };
}

// [B-3] 사용자의 모든 선택지와 분석 결과(최종 쿼리 포함)를 저장하는 전역 객체
userSelections = {
    favoriteTeamExists: "",
    league: "",
    favoriteTeam: "",
    fandom: "",
    star: "",
    story: "",
    visual: "",
    capital: "",
    // 최종 쿼리는 이제 객체(Dictionary) 형태로 초기화 및 저장됨
    finalQuery: {}
};


/* --- [B-4] 리그별 팀 옵션 --- */
const teamOptionsByLeagueId = {
    epl: [
        "뉴캐슬 유나이티드",
        "리버풀",
        "맨체스터 시티",
        "맨체스터 유나이티드",
        "브라이튼",
        "아스날",
        "아스톤 빌라",
        "울버햄튼 원더러스",
        "웨스트햄 유나이티드",
        "첼시",
        "크리스탈 팰리스",
        "토트넘 홋스퍼"
    ],

    kleague: [
        "강원FC",
        "광주FC",
        "대구FC",
        "대전 하나 시티즌",
        "수원 삼성 블루윙즈",
        "울산 HD FC",
        "인천 유나이티드 FC",
        "전북 현대 모터스",
        "제주 SK FC",
        "포항 스틸러스",
        "FC서울",
        "FC안양"
    ],

    kbo: [
        "NC 다이노스",
        "KT 위즈",
        "LG 트윈즈",
        "SSG 랜더스",
        "기아 타이거즈",
        "두산 베어스",
        "롯데 자이언츠",
        "삼성 라이온즈",
        "키움 히어로즈",
        "한화 이글스"
    ],

    f1: [
        "레이싱 불스",
        "레드불",
        "메르세데스",
        "맥라렌",
        "알핀",
        "애스턴 마틴",
        "윌리엄스",
        "자우버",
        "페라리",
        "하스"
    ]
};


/* --- [B-5] 후속 4문항 --- */
const questions = [
    { key: "fandom", botText: "응원하는 팀을 고를 때, 팬덤과 소속감은 얼마나 중요한가요?" },
    { key: "star", botText: "팀을 볼 때, 스타 플레이어와 강함은 얼마나 중요한가요?" },
    { key: "story", botText: "어떤 팀의 스토리에 더 끌리시나요?" },
    { key: "visual", botText: "팀의 비주얼과 분위기(유니폼·플레이 스타일)는 중요하신가요?" },
    { key: "capital", botText: "자본력과 리그 지배력에 대해 어떻게 생각하시나요?" }
];


/* --- [B-6] 리그별 선택지 --- */
const optionsByLeague = {
    fandom: [
        { name: "stadion", botText: "🏟️ 매우 중요" },
        { name: "some", botText: "🙂 어느 정도 중요" },
        { name: "ignore", botText: "🤷 크게 상관없음" }
    ],
    star: [
        { name: "star", botText: "⭐ 압도적인 스타와 강팀" },
        { name: "team", botText: "💪 팀워크 중심의 강함" },
        { name: "grow", botText: "🌱 성장 가능성" }
    ],
    story: [
        { name: "tradition", botText: "🏛️ 전통의 명문" },
        { name: "miracle", botText: "✨ 기적의 서사" },
        { name: "both", botText: "⚖️ 둘 다 좋음" }
    ],
    visual: [
        { name: "important", botText: "🎨 매우 중요" },
        { name: "plus", botText: "🙂 있으면 플러스" },
        { name: "ignore", botText: "📊 전혀 중요하지 않음" }
    ],
    capital: [
        { name: "rich", botText: "💰 강한 자본 선호" },
        { name: "balance", botText: "⚖️ 균형이 중요" },
        { name: "underdog", botText: "💪 언더독 선호" }
    ]
};

/* --- [B-7] 시작 --- */
function startBotLogic() {
    currentStep = 1;
    followIndex = 0;

    // 챗봇 재시작 또는 초기화 시 사용자 선택 데이터를 초기 상태로 리셋
    userSelections = {
        favoriteTeamExists: "",
        league: "",
        favoriteTeam: "",
        fandom: "",
        star: "",
        story: "",
        visual: "",
        capital: "",
        // 쿼리 데이터 구조를 객체형으로 유지
        finalQuery: {}
    };

    queryTokenSet = new Set(); // ✅ 토큰 누적 초기화


    const chatWin = document.getElementById('chat-window');
    chatWin.style.width = '360px';
    chatWin.style.height = '520px';

    document.getElementById('chat-messages').innerHTML = '';
    document.getElementById('chat-options').innerHTML = '';

    addMsg('bot', '안녕하세요! 당신의 스포츠 소울메이트를 찾아주는 SBUNPA AI입니다. 🤖');
    scrollChatToBottom();

    setTimeout(() => askHasFavoriteTeam(), 700);
}


/* --- Q1: 좋아하는 팀 있나요? --- */
function askHasFavoriteTeam() {
    addMsg('bot', '좋아하는 팀이 있으신가요?');

    showOpts(['✅ 있어요', '❌ 없어요'], (choice) => {
        addMsg('user', choice);

        // 1) 좋아하는 팀 없음 → 관심 리그(4개)로 바로
        if (choice === '❌ 없어요') {
            userSelections.favoriteTeamExists = "no";
            userSelections.favoriteTeam = "none";
            userSelections.favoriteLeague = "";
            console.log("📍 좋아하는 팀 없음: userSelections.favoriteTeam =", userSelections.favoriteTeam);
            askLeagueInterestOnly();   // ✅ 이 함수가 반드시 있어야 함
            return;
        }

        // 2) 좋아하는 팀 있음 → 그 팀의 리그 → 팀 선택 → (이후 3개 리그만 보여주기)
        userSelections.favoriteTeamExists = "yes";
        askFavoriteTeamLeague();
    });
}

function askFavoriteTeamLeague() {
    addMsg('bot', '좋아하는 팀이 속한 리그는 어디인가요?');

    const leagueOpts = chatData.leagues.map(l => l.name);
    showOpts(leagueOpts, (choice) => {
        const selected = chatData.leagues.find(l => l.name === choice);
        const leagueId = selected?.id || 'epl';

        userSelections.favoriteLeague = leagueId;
        userSelections.league = leagueId;

        addMsg('user', choice);
        askTeamPickByLeague(leagueId); // 👉 바로 팀 선택
    });
}

function askLeagueInterestOnly() {
    addMsg('bot', '먼저, 어떤 리그에 관심이 있으신가요?');

    const leagueOpts = chatData.leagues.map(l => l.name);

    showOpts(leagueOpts, (choice) => {
        const selected = chatData.leagues.find(l => l.name === choice);
        const leagueId = selected?.id || 'epl';

        userSelections.league = leagueId;
        addMsg('user', `${choice} 선택!`);

        // 관심 리그를 골랐으니 바로 성향 질문 시작
        followIndex = 0;
        queryTokenSet = new Set();
        askNextFollowup();
    });
}

// (환경에 따라) 전역 바인딩 안전장치
window.askLeagueInterestOnly = askLeagueInterestOnly;



/* --- 리그 선택 --- */
function askLeagueInterestThenContinue(needTeamPick) {
    addMsg('bot', '먼저, 어떤 리그에 관심이 있으신가요?');

    const leagueOpts = chatData.leagues.map(l => l.name);
    showOpts(leagueOpts, (choice) => {
        const selected = chatData.leagues.find(l => l.name === choice);
        const leagueId = selected ? selected.id : 'epl';

        userSelections.league = leagueId;
        addMsg('user', `${choice} 선택!`);

        if (!needTeamPick) {
            askNextFollowup();
            return;
        }

        askTeamPickByLeague(leagueId);
    });
}

/* --- 팀 선택 --- */
function askTeamPickByLeague(leagueId) {
    addMsg('bot', '좋아하는 팀을 골라주세요!');

    const teamOpts = teamOptionsByLeagueId[leagueId] || [];
    if (teamOpts.length === 0) {
        userSelections.favoriteTeam = "none";
        addMsg('bot', '팀 목록 데이터가 없어서 팀 선택을 건너뛰었어요.');
        askNextFollowup();
        return;
    }

    showOpts(teamOpts, (teamName) => {
        userSelections.favoriteTeam = teamName;
        console.log("📍 좋아하는 팀 선택 완료: userSelections.favoriteTeam =", userSelections.favoriteTeam);
        addMsg('user', `${teamName} 좋아해요!`);

        askOtherLeagueInterest(); // ⭐ 새 단계
    });
}

/**
 * 좋아하는 팀 선택 후, 새롭게 분석을 진행할 관심 리그를 선택받습니다.
 */
function askOtherLeagueInterest() {
    addMsg('bot', '새롭게 관심 있는 리그는 어디인가요?');

    // 사용자가 방금 고른 좋아하는 팀의 리그 ID를 가져옵니다.
    const exclude = userSelections.favoriteLeague;
    console.log("🔍 [디버그] 제외할 좋아하는 팀의 리그:", exclude);

    // 전체 리그 목록에서 좋아하는 팀의 리그를 제외한 나머지를 필터링합니다.
    const filteredLeagues = chatData.leagues
        .filter(l => l.id !== exclude)
        .map(l => l.name);

    console.log("🔍 [디버그] 화면에 표시할 관심 리그 옵션:", filteredLeagues);

    showOpts(filteredLeagues, (choice) => {
        // 사용자가 선택한 리그 이름에 해당하는 리그 객체를 찾습니다.
        const selected = chatData.leagues.find(l => l.name === choice);
        const newLeagueId = selected?.id || "epl";

        // 📍 핵심 수정: 성향 테스트를 진행할 리그(userSelections.league)를 새 리그 ID로 업데이트합니다.
        userSelections.league = newLeagueId;
        console.log("✅ [디버그] 분석 대상 리그가 변경되었습니다:", userSelections.league);

        addMsg('user', choice);

        // 사용자가 혼란스럽지 않게 리그 전환 안내 메시지를 띄웁니다.
        setTimeout(() => {
            addMsg('bot', `좋습니다! 이제 ${choice}에 대한 성향 분석을 시작할게요. 🚀`);

            // 질문 순서를 처음(0번)부터 시작하도록 초기화합니다.
            followIndex = 0;

            // 다음 성향 질문으로 이동합니다.
            askNextFollowup();
        }, 500);
    });
}


/* --- 후속 4문항 --- */
function askNextFollowup() {
    if (followIndex >= questions.length) {
        // ✅ 모든 질문이 완료되면 최종 쿼리 객체를 생성하여 저장합니다.
        userSelections.finalQuery = buildFinalQuery();

        // 🔍 [디버그] 모델로 전송될 최종 데이터 구조 확인
        console.log("-----------------------------------------");
        console.log("🚀 [FINAL DATA]", userSelections);
        console.log("📝 [MODEL QUERY]", userSelections.finalQuery.full_query);
        console.log("-----------------------------------------");

        processAnalysis();
        return;
    }

    const q = questions[followIndex];
    const leagueId = userSelections.league;

    const intentMap = getIntentMapByLeague(leagueId);
    if (!intentMap) {
        addMsg("bot", "아직 이 리그는 준비 중이에요 🙏");
        return;
    }

    setTimeout(() => {
        addMsg("bot", q.botText);

        const opts = Object.keys(intentMap[q.key] || {});
        if (opts.length === 0) {
            addMsg("bot", "선택지 데이터가 없어요. intentMap 설정을 확인해주세요.");
            return;
        }

        showOpts(opts, (choiceLabel) => {
            userSelections[q.key] = choiceLabel;

            // ✅ 토큰 누적
            addTokens(intentMap, q.key, choiceLabel);

            // ✅ 매 질문마다 query 갱신
            userSelections.finalQuery = buildFinalQuery();

            addMsg("user", choiceLabel);
            followIndex += 1;
            askNextFollowup();
        });
    }, 550);
}



/* --- 분석 로딩 + 서버호환 --- */
function processAnalysis() {
    addMsg('bot', '당신의 답변을 바탕으로 AI가 성향을 분석 중입니다...');

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'msg-bubble bot-msg';
    loadingDiv.id = 'loading-bubble';
    loadingDiv.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    document.getElementById('chat-messages').appendChild(loadingDiv);
    scrollChatToBottom();

    // ✅ 서버 결과 사용 (JSON 데이터 전송)
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userSelections),
    })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            const loader = document.getElementById('loading-bubble');
            if (loader) loader.remove();

            if (data && data.error) {
                console.error("Server Logic Error:", data.error);
                addMsg('bot', `분석 중 오류가 발생했습니다: ${data.error}`);
            } else {
                showDashboard(data); // ✅ 서버 데이터 기반 대시보드 출력
            }
        })
        .catch((err) => {
            const loader = document.getElementById('loading-bubble');
            if (loader) loader.remove();

            console.error("Fetch/Network Error:", err);
            addMsg('bot', '죄송합니다. 서버와 통신 중 문제가 발생했습니다. 네트워크 상태를 확인하시거나 잠시 후 다시 시도해 주세요. 😢');
        });
}

/* --- [결과] 대시보드 표시 (서버 있으면 서버 기반, 없으면 로컬 기반) --- */
function showDashboard(resultData) {
    // ✅ 서버 응답이 정상인 경우에만 대시보드를 렌더링합니다.
    // 기존에 리버풀로 강제 설정하던 로컬 fallback 로직을 삭제했습니다.
    if (resultData && resultData.team_name && resultData.team_data && resultData.scores) {
        const team = {
            name: resultData.team_name,
            slogan: resultData.team_data.introduction
                ? resultData.team_data.introduction.substring(0, 30) + '...'
                : "최고의 파트너",
            tags: resultData.team_data.style_tags ? resultData.team_data.style_tags.slice(0, 2) : ['추천', '팀'],
            logo: '🏆',
            match: resultData.match_percent,
            passion: resultData.scores.passion,
            money: resultData.scores.money,
            strategy: resultData.scores.strategy,
            history: resultData.scores.history,
            star: resultData.scores.star,
            vibe: resultData.scores.vibe,
            insight: resultData.insight || "당신의 답변을 바탕으로 추천했어요!"
        };

        renderDashboardUI(team, userSelections.league);
    } else {
        // 데이터가 비정상적인 경우 사용자에게 알림
        addMsg('bot', '성향 분석 결과를 불러오는 데 실패했습니다. 다시 시도해 주세요.');
    }
}

/**
 * 프리미엄 스타일로 디자인된 결과 대시보드를 렌더링합니다.
 * @param {Object} team - 추천된 팀 데이터
 * @param {string} leagueId - 선택된 리그 ID
 */
function renderDashboardUI(team, leagueId) {
    const chatWin = document.getElementById('chat-window');
    // 결과창 크기를 더 콤팩트하게 줄여서 상단 헤더(닫기 버튼)가 잘 보이도록 합니다.
    chatWin.style.width = '720px';
    chatWin.style.height = '580px';

    const container = document.getElementById('chat-messages');

    // 로고 이미지 경로 재확인
    const logoSrc = TEAM_LOGO_MAP[team.name];

    container.style.padding = '0'; // 대시보드가 꽉 차도록 패딩 제거

    container.innerHTML = `
    <div class="dashboard-container animate-slide-up">
      <!-- 헤더: 타이틀과 매칭 배지 -->
      <header class="dash-header">
        <h2>Optimal Match Found</h2>
        <div class="match-badge">
          <span>${team.match || 95}</span>% 일치하는 클럽을 찾았어요
        </div>
      </header>

      <!-- 히어로: 로고와 팀명 -->
      <section class="team-hero">
        <div class="team-logo-circle">
          ${logoSrc
            ? `<img src="${logoSrc}" alt="${team.name} 로고" class="team-logo-img">`
            : `<span style="font-size: 40px;">⚽</span>`
        }
        </div>
        <div class="team-info-box">
          <h1 class="team-name">${team.name}</h1>
          <p class="team-slogan">"${team.slogan}"</p>
          <div class="tag-row">
            ${(team.tags || []).map(tag => `<span class="tag">#${tag}</span>`).join('')}
          </div>
        </div>
      </section>

      <!-- 바디: 차트와 인사이트 -->
      <div class="dash-body">
        <!-- 좌측 컬럼 -->
        <article class="chart-card">
          <div class="chart-wrapper">
            <canvas id="radarChart"></canvas>
          </div>
          <div class="points-list">
            <div class="point-item">
              <span class="point-label">추천 클럽</span>
              <span class="point-value">${team.name}</span>
            </div>
            <div class="point-item">
              <span class="point-label">분석 대상 리그</span>
              <span class="point-value">${leagueId.toUpperCase()}</span>
            </div>
            <div class="point-item">
              <span class="point-label">기존 선호 팀</span>
              <span class="point-value">${userSelections.favoriteTeam || '없음'}</span>
            </div>
          </div>
        </article>

        <!-- 우측 컬럼 -->
        <article class="insight-card">
          <div class="recommend-reason">
            <h3 class="section-title">왜 이 팀을 추천할까요?</h3>
            <div class="reason-list">
              <div class="reason-item" style="animation-delay: 0.1s;">✨ 사용자의 성향과 팀의 핵심 철학이 일치합니다.</div>
              <div class="reason-item" style="animation-delay: 0.2s;">🏆 선호하시는 전력 및 서사 구조를 가지고 있습니다.</div>
              <div class="reason-item" style="animation-delay: 0.3s;">📈 데이터 기반 분석 결과 가장 높은 만족도가 기대됩니다.</div>
            </div>
          </div>

          <div class="insight-box">
            <h3 class="section-title">전문가 인사이트</h3>
            <div class="insight-bubble">
              ${team.insight}
            </div>
          </div>
        </article>
      </div>

      <!-- 푸터: 액션 버튼 -->
      <footer class="dash-footer">
        <button class="btn-premium" onclick="resetChat()">다시 분석하기</button>
        <button class="btn-premium primary" onclick="handleTeamAction('${team.name}')">
          <img src="https://img.icons8.com/?size=100&id=742&format=png&color=ffffff" width="16">
          클럽 상세 정보 확인
        </button>
      </footer>
    </div>
    `;

    // 채팅창 하단으로 스크롤
    scrollChatToBottom();

    // 레이더 차트 생성 (데이터가 준비된 후 실행)
    setTimeout(() => {
        initRadarChart(team);
    }, 100);
}

function initRadarChart(team) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    // ✅ 기존 방식: userSelections(사용자의 답변)를 기반으로 차트를 그렸습니다.
    // ✅ 변경 방식: team(모델이 추천해준 팀)의 실제 스태츠 데이터를 기반으로 차트를 그립니다.
    // 이를 통해 추천된 팀의 비전과 실제 특징을 더 정확하게 확인할 수 있습니다.
    const teamStats = [
        team.passion || 70,  // 열정 (fan_passion)
        team.money || 70,    // 투자 (money)
        team.strategy || 70, // 전략 (attack_style)
        team.history || 70,  // 역사 (tradition)
        team.star || 70,     // 스타 (star_power)
        team.vibe || 70      // 감성 (underdog_feel)
    ];

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['열정', '투자', '전략', '역사', '스타', '감성'],
            datasets: [{
                label: '추천 팀 특징',
                data: teamStats,
                backgroundColor: 'rgba(59, 130, 246, 0.3)',
                borderColor: '#3B82F6',
                borderWidth: 2,
                pointBackgroundColor: '#3B82F6',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#3B82F6'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: { display: false, stepSize: 20 },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: { size: 10, weight: '600' }
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
    document.getElementById('chat-options').innerHTML = '';
}

/* --- 다시 시작 --- */
function resetChat() {
    const chatWin = document.getElementById('chat-window');
    chatWin.style.width = '360px';
    chatWin.style.height = '520px';

    currentStep = 0;
    followIndex = 0;

    userSelections = {
        favoriteTeamExists: "",
        league: "",
        favoriteTeam: "",
        fandom: "",
        star: "",
        story: "",
        visual: "",
        capital: "",
        // ✅ 쿼리 데이터 구조를 객체형으로 유지 (서버 전송용)
        finalQuery: {}
    };

    queryTokenSet = new Set(); // ✅ 토큰 누적 초기화

    startBotLogic();
}

/* html 로드 후 init 실행 */
document.addEventListener('DOMContentLoaded', init);
