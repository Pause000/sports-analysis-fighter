/* --- 전역 변수 및 데이터 --- */
let currentStep = 0;
const leagues = ["프리미어 리그", "K리그", "KBO", "F1"];
const teams = { "프리미어 리그": ["맨시티", "리버풀", "아스널"], "K리그": ["울산", "전북", "서울"], "KBO": ["LG", "삼성", "기아"], "F1": ["레드불", "페라리", "메르세데스"] };

const leagueDetailData = {
    'EPL': { desc: '세계 최고의 축구 리그 프리미어리그', color: '#38003c', rank: [['1', '리버풀', '20', '45'], ['2', '맨시티', '20', '43']] },
    'K리그': { desc: '다이나믹한 한국 축구의 정수', color: '#02234b', rank: [['1', '울산', '38', '76'], ['2', '포항', '38', '64']] },
    'KBO': { desc: '심장을 뛰게 하는 열광의 야구', color: '#041e42', rank: [['1', 'LG', '144', '86'], ['2', 'KT', '144', '79']] },
    'F1': { desc: '지상 최고의 속도 경쟁', color: '#e10600', rank: [['1', '베르스타펜', '22', '575'], ['2', '페레즈', '22', '285']] }
};

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
            for (let i = 1; i <= 6; i++) {
                const randomThumb = `https://picsum.photos/seed/${id}${i}/300/170`;
                const randomTime = `0${Math.floor(Math.random() * 5 + 3)}:${Math.floor(Math.random() * 50 + 10)}`;
                row.innerHTML += `<div class="video-card"><div class="video-thumb" style="background-image: url('${randomThumb}'); background-size: cover;"><div class="video-time">${randomTime}</div></div><p style="font-size:13px; margin-top:10px; color:#ccc;">${id} 하이라이트 #${i}</p></div>`;
            }
            container.appendChild(row);
        });
    }

    // 리그 라이브 목록 초기 실행 (EPL)
    const firstTab = document.querySelector('.tab-btn');
    if (firstTab) filterLive('EPL', firstTab);
}

/* --- [2] 라이브 필터 기능 (목록 사라짐 방지) --- */
function filterLive(league, btn) {
    if (!btn) return;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const list = document.getElementById('live-list');
    if (!list) return;

    list.innerHTML = ''; // 비워주고 다시 채우기
    for (let i = 1; i <= 8; i++) {
        list.innerHTML += `<div class="live-item-mini">${league} LIVE 중계 ${i}</div>`;
    }
}

/* --- [3] 라이브 중계 옆으로 이동 (좌우) --- */
function scrollGrid(button, direction) {
    const track = document.getElementById("carousel-track");
    const cards = track.querySelectorAll(".live-card-large");

    // 현재 중앙 기준 위치
    const trackCenter = track.scrollLeft + track.offsetWidth / 2;

    // 각 카드의 중앙 위치 계산
    let targetIndex = 0;
    let minDistance = Infinity;

    cards.forEach((card, index) => {
        const cardCenter =
            card.offsetLeft + card.offsetWidth / 2;

        const distance = Math.abs(cardCenter - trackCenter);

        if (distance < minDistance) {
            minDistance = distance;
            targetIndex = index;
        }
    });

    // 이동할 카드 인덱스 계산
    if (direction === "right") {
        targetIndex = Math.min(targetIndex + 1, cards.length - 1);
    } else {
        targetIndex = Math.max(targetIndex - 1, 0);
    }

    // 목표 카드의 중앙으로 스크롤
    const targetCard = cards[targetIndex];
    const targetScroll =
        targetCard.offsetLeft +
        targetCard.offsetWidth / 2 -
        track.offsetWidth / 2;

    track.scrollTo({
        left: targetScroll,
        behavior: "smooth"
    });
}

/* --- [4] 화면 전환 & 모달 --- */
function openLeague(id) {
    document.getElementById('home-view').classList.add('hidden');
    document.getElementById('detail-view').classList.remove('hidden');
    const data = leagueDetailData[id];
    document.getElementById('detail-title').innerText = id;
    document.getElementById('detail-desc').innerText = data.desc;
    document.getElementById('detail-hero').style.background = `linear-gradient(to bottom, ${data.color}, var(--bg))`;
    let html = '';
    data.rank.forEach(r => html += `<tr><td>${r[0]}</td><td><b>${r[1]}</b></td><td>${r[2]}</td><td>${r[3]}</td></tr>`);
    document.getElementById('standing-body').innerHTML = html;
    window.scrollTo(0, 0);
}
function goHome() { document.getElementById('home-view').classList.remove('hidden'); document.getElementById('detail-view').classList.add('hidden'); }
function openModal(isSignUp) { document.getElementById('auth-modal').classList.remove('hidden'); if (isSignUp) toggleAuthMode(true); }
function closeModal() { document.getElementById('auth-modal').classList.add('hidden'); }
function toggleAuthMode(forceSignUp) {
    const isSignUp = forceSignUp || document.getElementById('auth-submit').innerText === '로그인';
    document.getElementById('auth-submit').innerText = isSignUp ? '회원가입' : '로그인';
    document.getElementById('name-field').classList.toggle('hidden', !isSignUp);
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
function startBotLogic() {
    currentStep = 1; addMsg('bot', '분석을 시작합니다!');
    setTimeout(() => {
        addMsg('bot', '리그를 선택해주세요.');
        showOpts(leagues, (L) => { addMsg('user', L); askFan(L); });
    }, 600);
}
function askFan(L) { addMsg('bot', '응원 팀이 있나요?'); showOpts(['없다', ...teams[L]], (c) => { addMsg('user', c); addMsg('bot', '분석 완료!'); }); }

/* --- 눈동자 추적 --- */
document.addEventListener('mousemove', (e) => {
    const pupils = [document.getElementById('pupil-l'), document.getElementById('pupil-r')];
    const btn = document.getElementById('float-btn');
    if (!btn || !pupils[0]) return;
    const rect = btn.getBoundingClientRect();
    const x = (e.clientX - (rect.left + rect.width / 2)) / 50;
    const y = (e.clientY - (rect.top + rect.height / 2)) / 50;
    const dist = Math.min(3, Math.hypot(x, y));
    const angle = Math.atan2(y, x);
    pupils.forEach(p => p && (p.style.transform = `translate(calc(-50% + ${Math.cos(angle) * dist}px), calc(-50% + ${Math.sin(angle) * dist}px))`));
});

// 실행!
document.addEventListener('DOMContentLoaded', init);


// EPL , K리그 , KBO , F1 라이브 리스트 조정
function scrollGrid2(button, direction) {
    // 옆으로 리스트 확인
    const track = document.getElementById("live-list");
    const cards = track.querySelectorAll(".live-item-mini");
    const trackCenter = track.scrollLeft + track.offsetWidth / 2;
    let targetIndex = 0;
    let minDistance = Infinity;
    cards.forEach((card, index) => {
        const cardCenter = card.offsetLeft + card.offsetWidth / 2;
        const distance = Math.abs(cardCenter - trackCenter);
        if (distance < minDistance) {
            minDistance = distance;
            targetIndex = index;
        }
    });
    // 이동할 카드 인덱스 계산
    if (direction === "right") {
        targetIndex = Math.min(targetIndex + 1, cards.length - 1);
    } else {
        targetIndex = Math.max(targetIndex - 1, 0);
    }
    // 목표 카드의 중앙으로 스크롤
    const targetCard = cards[targetIndex];
    const targetScroll = targetCard.offsetLeft + targetCard.offsetWidth / 2 - track.offsetWidth / 2;
    track.scrollTo({
        left: targetScroll,
        behavior: "smooth"
    });
}