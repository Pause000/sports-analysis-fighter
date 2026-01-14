/* --- 전역 변수 및 데이터 --- */
let currentStep = 0;
const leagues = ["프리미어 리그", "K리그", "KBO", "F1"];
const teams = { "프리미어 리그": ["맨시티", "리버풀", "아스널"], "K리그": ["울산", "전북", "서울"], "KBO": ["LG", "삼성", "기아"], "F1": ["레드불", "페라리", "메르세데스"] };

const leagueDetailData = {
    /* --------------------------------- */
    /* --------- 정보 수정 필요 --------- */
    /* --------------------------------- */
    'EPL': {
        desc: '세계 최고의 축구 리그 프리미어리그',
        color: '#38003c',
        bgImg: '../images/리버플 vs 맨시티.png',
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
            // 커스텀 이미지가 있는지 확인
            const customImages = leagueDetailData[id].highlights || [];

            // 6개 카드 생성 (커스텀 이미지가 있으면 사용, 없으면 랜덤)
            for (let i = 1; i <= 6; i++) {
                let thumbUrl, videoTime;

                if (i <= customImages.length) {
                    // 로컬 이미지 사용 (web/images/Highlights or specific league folder)
                    // 데이터에 정의된 경로를 우선 사용
                    if (customImages[i - 1].file.startsWith('http') || customImages[i - 1].file.startsWith('..')) {
                        thumbUrl = customImages[i - 1].file;
                    } else {
                        // 하위 호환성: 파일명만 있는 경우 highlights 폴더로 가정
                        thumbUrl = `../images/highlights/${customImages[i - 1].file}`;
                    }
                    videoTime = customImages[i - 1].time || "03:00";
                } else {
                    // 랜덤 이미지 (부족한 경우 채우기)
                    thumbUrl = `https://picsum.photos/seed/${id}${i}/300/170`;
                    videoTime = `0${Math.floor(Math.random() * 5 + 3)}:${Math.floor(Math.random() * 50 + 10)}`;
                }

                row.innerHTML += `<div class="video-card"><div class="video-thumb" style="background-image: url('${thumbUrl}'); background-size: cover;"><div class="video-time">${videoTime}</div></div><p style="font-size:13px; margin-top:10px; color:#ccc;">${id} 하이라이트 #${i}</p></div>`;
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

    list.innerHTML = ''; // 비워주고 다시 채우기

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

    // 스크롤 맨 처음으로 초기화
    list.scrollTo({ left: 0, behavior: 'smooth' });
}

/* --- [3] 똑똑한 스크롤 함수 (상하단 독립) --- */
function scrollGrid(btn, direction) {
    const wrapper = btn.closest('.live-section-wrapper');
    const container = wrapper.querySelector('.carousel-track, .live-grid');
    if (!container) return;

    const isMain = container.classList.contains('carousel-track');

    if (isMain) {
        // [수정] 메인 카드는 정확히 중앙에 오도록 스크롤 계산
        const cards = Array.from(container.children);
        const centerPoint = container.scrollLeft + (container.clientWidth / 2);

        // 현재 중앙에 가장 가까운 카드의 인덱스 찾기
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

        // 방향에 따라 목표 인덱스 설정
        let targetIndex = direction === 'left' ? closestIndex - 1 : closestIndex + 1;

        // 범위 제한
        targetIndex = Math.max(0, Math.min(targetIndex, cards.length - 1));

        const targetCard = cards[targetIndex];

        // 목표 카드를 중앙에 위치시키기 위한 스크롤 값 계산
        // (카드 왼쪽 위치 + 카드 절반) - (컨테이너 절반)
        const scrollTarget = targetCard.offsetLeft + (targetCard.offsetWidth / 2) - (container.clientWidth / 2);

        container.scrollTo({ left: scrollTarget, behavior: 'smooth' });

    } else {
        // 하단 작은 리스트는 기존 방식 유지 (혹은 필요 시 동일 로직 적용 가능)
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

    // [상단 섹션] 리그 고유 컬러 틴트 + 배경 & 리그 정보
    // 배경 이미지 URL이 없다면 기본 이미지 사용 (예: unsplash)
    const bgImg = data.bgImg || 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=2000';

    detailView.innerHTML = `
        <button class="back-btn" onclick="goHome()">❮</button>
        <div id="detail-hero" class="detail-hero" style="background: linear-gradient(to bottom, ${data.color}CC, var(--bg)), url('${bgImg}'); background-size: cover; background-position: center;">
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
                <div class="section-header">
                    <h3>리그 순위표</h3>
                </div>
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
                                <td class="point-cell" style="color: ${data.color === '#FFFFFF' ? 'var(--primary)' : data.color}">${r[6] || r[3]}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>

            <div class="player-section">
                <div class="section-header">
                    <h3>주요 선수 명단</h3>
                </div>
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

// 홈페이지로 연결하는 함수
function goHome() {
    document.getElementById('home-view').classList.remove('hidden');
    document.getElementById('detail-view').classList.add('hidden');
    document.getElementById('about-view').classList.add('hidden'); // 추가

    // 탭 활성화 UI 처리
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    document.querySelector('.nav-links a:first-child').classList.add('active');
}

// 소개 페이지로 연결하는 함수
function goAbout() {
    document.getElementById('home-view').classList.add('hidden');
    document.getElementById('detail-view').classList.add('hidden');
    document.getElementById('about-view').classList.remove('hidden');

    // 탭 활성화 UI 처리
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    document.querySelector('a[href="#about"]').classList.add('active');

    // 소개 페이지 데이터 렌더링 (AboutPage.tsx 내용 기반)
    renderAbout();
    window.scrollTo(0, 0);
}

// goAbout 실행 시 정보를 채워줄 함수
function renderAbout() {
    const aboutView = document.getElementById('about-view');
    // 이미 렌더링 되어있다면 중복 방지
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

    // 팀원 소개도 비슷하게 render... (생략 가능)
}

function openModal(isSignUp) { document.getElementById('auth-modal').classList.remove('hidden'); if (isSignUp) toggleAuthMode(true); }
function closeModal() { document.getElementById('auth-modal').classList.add('hidden'); }
function toggleAuthMode(forceSignUp) {
    const isSignUp = forceSignUp || document.getElementById('auth-submit').innerText === '로그인';
    document.getElementById('auth-submit').innerText = isSignUp ? '회원가입' : '로그인';
    document.getElementById('name-field').classList.toggle('hidden', !isSignUp);
    document.getElementById('toggle-btn').innerText = isSignUp ? '로그인' : '회원가입';
}

/* --- [5] 챗봇 로직 --- */
function toggleChat() {
    const chat = document.getElementById('chat-window');
    chat.classList.toggle('hidden');
    if (!chat.classList.contains('hidden') && currentStep === 0) startBotLogic();
}
function addMsg(type, text) {
    const box = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `msg-bubble ${type}-msg`; div.innerText = text;
    box.appendChild(div); box.scrollTop = box.scrollHeight;
}
function showOpts(opts, callback) {
    const container = document.getElementById('chat-options');
    container.innerHTML = '';
    opts.forEach(opt => {
        const btn = document.createElement('button'); btn.className = 'opt-btn'; btn.innerText = opt;
        btn.onclick = () => { container.innerHTML = ''; callback(opt); };
        container.appendChild(btn);
    });
}

/* --- [데이터] Figma에서 가져온 리그 및 추천 정보 --- */
const chatData = {
    leagues: [
        { id: 'epl', name: '⚽ 프리미어 리그', emoji: '🏴󠁧󠁢󠁥󠁮󠁧󠁿' },
        { id: 'kleague', name: '⚽ K리그', emoji: '🇰🇷' },
        { id: 'kbo', name: '⚾ KBO 리그', emoji: '⚾' },
        { id: 'f1', name: '🏎️ 포뮬러 원', emoji: '🏁' }
    ],
    vibes: [
        { id: 'aggressive', name: '🔥 공격적인', description: '화끈한 공격 스타일' },
        { id: 'traditional', name: '🏛️ 전통적인', description: '역사와 전통 중시' },
        { id: 'star', name: '⭐ 스타 중심', description: '슈퍼스타 보유 팀' },
        { id: 'underdog', name: '💪 도전자', description: '약자의 반란' }
    ],
    // 성향별 추천 팀 데이터 (Figma 로직 반영)
    recommendations: {
        epl: {
            aggressive: { name: '리버풀 FC', slogan: "You'll Never Walk Alone", tags: ['헤비메탈', '압박'], passion: 95, strategy: 85, history: 90, star: 80, money: 75, logo: '🔴' },
            traditional: { name: '맨체스터 유나이티드', slogan: "Glory Glory Man United", tags: ['전통', '명가'], passion: 80, strategy: 70, history: 100, star: 85, money: 90, logo: '😈' },
            star: { name: '맨시티', slogan: "Blue Moon", tags: ['월드클래스', '전술'], passion: 75, strategy: 100, history: 60, star: 95, money: 100, logo: '🔵' },
            underdog: { name: '아스톤 빌라', slogan: "Prepared", tags: ['돌풍', '성장'], passion: 85, strategy: 80, history: 75, star: 65, money: 70, logo: '🦁' }
        },
        // (다른 리그 데이터도 유사하게 확장)
    }
};

let userSelections = { league: '', vibe: '' };

/* --- [로직] 챗봇 흐름 제어 --- */
function startBotLogic() {
    currentStep = 1;
    document.getElementById('chat-messages').innerHTML = ''; // 초기화
    addMsg('bot', '안녕하세요! 당신의 스포츠 소울메이트를 찾아주는 SBUNPA AI입니다. 🤖');
    setTimeout(() => {
        addMsg('bot', '먼저, 어떤 리그에 관심이 있으신가요?');
        const leagueOpts = chatData.leagues.map(l => l.name);
        showOpts(leagueOpts, (choice) => {
            const selected = chatData.leagues.find(l => l.name === choice);
            userSelections.league = selected.id;
            addMsg('user', `${choice}가 궁금해요!`);
            askVibe();
        });
    }, 800);
}

function askVibe() {
    setTimeout(() => {
        addMsg('bot', '좋은 선택입니다! 어떤 스타일의 팀을 좋아하시나요?');
        const vibeOpts = chatData.vibes.map(v => v.name);
        showOpts(vibeOpts, (choice) => {
            const selected = chatData.vibes.find(v => v.name === choice);
            userSelections.vibe = selected.id;
            addMsg('user', `${choice} 스타일이 끌리네요.`);
            processAnalysis();
        });
    }, 600);
}

function processAnalysis() {
    setTimeout(() => {
        addMsg('bot', '당신의 답변을 바탕으로 AI가 성향을 분석 중입니다...');
        // 분석 애니메이션 (점 3개)
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'msg-bubble bot-msg';
        loadingDiv.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        document.getElementById('chat-messages').appendChild(loadingDiv);

        setTimeout(() => {
            loadingDiv.remove();
            showDashboard();
        }, 2000);
    }, 800);
}

/* --- [결과] 대시보드 표시 (Figma RecommendationDashboard 반영) --- */
function showDashboard() {
    const leagueData = chatData.recommendations[userSelections.league] || chatData.recommendations['epl'];
    const team = leagueData[userSelections.vibe] || leagueData['aggressive'];

    // 챗봇 창을 대시보드 모드로 전환 (크기 확장)
    const chatWin = document.getElementById('chat-window');
    chatWin.style.width = '845px';
    chatWin.style.height = '700px';

    const container = document.getElementById('chat-messages');
    container.innerHTML = `
        <div class="dashboard-container animate-slide-up">
            <div class="dash-header">
                <h2>당신을 위한 추천 팀</h2>
                <div class="team-hero">
                    <div class="hero-row-top">
                        <div class="team-logo-circle">${team.logo || '⚽'}</div>
                        <h1 class="team-name">${team.name}</h1>
                    </div>
                    <div class="hero-row-bottom">
                        <p class="team-slogan">"${team.slogan}"</p>
                        <div class="tag-row">
                            ${team.tags.map(tag => `<span class="tag">#${tag}</span>`).join('')}
                        </div>
                    </div>
                </div>
                <div class="match-badge"><span>${team.match || 95}</span>% 일치</div>
            </div>

            <div class="dash-body">
                <div class="dash-left">
                    <div class="chart-wrapper">
                        <canvas id="radarChart"></canvas>
                    </div>
                    <div class="special-points">
                        <h3>⭐ 핵심 포인트</h3>
                        <ul>
                            <li>• 경쟁적 성향: 매우 높음 (상위 1위)</li>
                            <li>• 팬덤 규모: 세계적</li>
                            <li>• 최근 5년 평균 순위: 3위 이내</li>
                        </ul>
                    </div>
                </div>

                <div class="dash-right">
                    <div class="reason-section">
                        <h3>추천 이유</h3>
                        <div class="reason-cards">
                            <div class="r-card"><span>1</span> 강렬한 공격 축구</div>
                            <div class="r-card"><span>2</span> 전술적 유연함</div>
                            <div class="r-card"><span>3</span> 열정적인 서포터즈</div>
                        </div>
                    </div>
                    <div class="insight-box" style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; text-align: left; margin-bottom: 20px;">
                        <h4 style="color: var(--primary); margin-bottom: 10px;">💡 추천 인사이트</h4>
                        <p style="font-size: 14px; line-height: 1.6; color: #ccc;">${team.insight}</p>
                    </div>
                </div>
            </div>

            <div class="dash-footer">
                <button class="action-btn" onclick="resetChat()">다시 분석하기</button>
                <button class="action-btn primary" onclick="window.open('https://www.liverpoolfc.com')">
                    <img src="https://img.icons8.com/?size=100&id=742&format=png&color=ffffff" width="16"> 팀 홈페이지
                </button>
                <button class="action-btn">다가오는 경기 확인</button>
            </div>
        </div>
    `;
    // 4. 차트 그리기 로직 (Chart.js 사용)
    const ctx = document.getElementById('radarChart').getContext('2d');

    // 사용자 성향 데이터 (가상의 파란색 데이터)
    const userVibeData = [85, 65, 75, 90, 80];

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['열정', '자본', '전략', '역사', '스타성'],
            datasets: [
                {
                    label: '팀 능력치',
                    data: [team.passion, team.money, team.strategy, team.history, team.star],
                    borderColor: '#FFD700', // 노란색
                    backgroundColor: 'rgba(255, 215, 0, 0.2)',
                    borderWidth: 2
                },
                {
                    label: '내 성향',
                    data: userVibeData,
                    borderColor: '#3B82F6', // 파란색
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#fff', font: { size: 12 } },
                    ticks: { display: false, max: 100, min: 0, stepSize: 20 }
                }
            },
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });

    document.getElementById('chat-options').innerHTML = '';
}



function resetChat() {
    // 1. 챗봇 창 크기 원래대로 (메신저 모드)
    const chatWin = document.getElementById('chat-window');
    chatWin.style.width = '360px';
    chatWin.style.height = '520px';

    // 2. 변수 초기화
    currentStep = 0;
    userSelections = { league: '', vibe: '' };

    // 3. 다시 시작
    startBotLogic();
}

// html 로드 후 init 실행
document.addEventListener('DOMContentLoaded', init);