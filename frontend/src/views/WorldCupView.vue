<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">⚡ SAI</div>
      <nav>
        <RouterLink to="/main"     class="nav-item">🏠 홈</RouterLink>
        <RouterLink to="/worldcup" class="nav-item">❤️ 이상형 월드컵</RouterLink>
        <RouterLink v-if="auth.isAdmin" to="/admin" class="nav-item">⚙️ 관리자</RouterLink>
      </nav>
      <button class="logout-btn" @click="handleLogout">로그아웃</button>
    </aside>

    <main class="content">
      <header class="top-bar">
        <h2>❤️ 이상형 월드컵</h2>
      </header>

      <!-- 카테고리 선택 -->
      <div v-if="phase === 'select'" class="phase-wrap">
        <h3 class="phase-title">카테고리를 선택하세요</h3>
        <div class="category-grid">
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="cat-card card"
            @click="startGame(cat)">
            <div class="cat-emoji">{{ cat.emoji }}</div>
            <div class="cat-name">{{ cat.name }}</div>
            <div class="cat-count">{{ cat.count }}강</div>
          </button>
        </div>
      </div>

      <!-- 대결 -->
      <div v-else-if="phase === 'battle'" class="phase-wrap">
        <div class="round-info">
          <span class="round-badge">{{ roundLabel }}</span>
          <span class="progress-text">{{ currentMatch + 1 }} / {{ totalMatches }} 경기</span>
        </div>

        <div class="battle-arena">
          <button class="candidate card" @click="pick(0)">
            <div class="cand-emoji">{{ current[0].emoji }}</div>
            <div class="cand-name">{{ current[0].name }}</div>
            <div class="vs-hint">클릭해서 선택!</div>
          </button>

          <div class="vs-circle">VS</div>

          <button class="candidate card" @click="pick(1)">
            <div class="cand-emoji">{{ current[1].emoji }}</div>
            <div class="cand-name">{{ current[1].name }}</div>
            <div class="vs-hint">클릭해서 선택!</div>
          </button>
        </div>

        <div class="progress-bar-wrap">
          <div class="progress-bar" :style="{ width: progressPct + '%' }"></div>
        </div>
      </div>

      <!-- 결과 -->
      <div v-else class="phase-wrap result-wrap">
        <div class="trophy">🏆</div>
        <h2>나의 이상형!</h2>
        <div class="winner card">
          <div class="winner-emoji">{{ winner.emoji }}</div>
          <div class="winner-name">{{ winner.name }}</div>
        </div>
        <div class="result-actions">
          <button class="btn-primary" @click="phase = 'select'">다시 하기</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const phase        = ref('select')
const categories   = [
  { id: 1, name: '음식',    emoji: '🍔', count: 16, items: [
    { name: '피자',       emoji: '🍕' }, { name: '치킨',    emoji: '🍗' },
    { name: '햄버거',     emoji: '🍔' }, { name: '삼겹살',  emoji: '🥩' },
    { name: '라면',       emoji: '🍜' }, { name: '초밥',    emoji: '🍣' },
    { name: '떡볶이',     emoji: '🌶️' }, { name: '파스타',  emoji: '🍝' },
    { name: '스테이크',   emoji: '🥩' }, { name: '샐러드',  emoji: '🥗' },
    { name: '짜장면',     emoji: '🍲' }, { name: '김치찌개',emoji: '🫕' },
    { name: '아이스크림', emoji: '🍦' }, { name: '케이크',  emoji: '🎂' },
    { name: '마라탕',     emoji: '🌶️' }, { name: '갈비',    emoji: '🍖' }
  ]},
  { id: 2, name: '여행지', emoji: '✈️', count: 8, items: [
    { name: '제주도',  emoji: '🏝️' }, { name: '도쿄',   emoji: '🗼' },
    { name: '파리',   emoji: '🗼' }, { name: '뉴욕',   emoji: '🗽' },
    { name: '발리',   emoji: '🌴' }, { name: '런던',   emoji: '🎡' },
    { name: '방콕',   emoji: '🛕' }, { name: '시드니', emoji: '🦘' }
  ]},
  { id: 3, name: '취미',  emoji: '🎮', count: 8, items: [
    { name: '게임',   emoji: '🎮' }, { name: '독서',   emoji: '📚' },
    { name: '영화',   emoji: '🎬' }, { name: '음악',   emoji: '🎵' },
    { name: '운동',   emoji: '🏋️' }, { name: '요리',   emoji: '👨‍🍳' },
    { name: '그림',   emoji: '🎨' }, { name: '등산',   emoji: '🏔️' }
  ]}
]

const pool         = ref([])
const winners      = ref([])
const currentMatch = ref(0)
const totalMatches = ref(0)
const roundSize    = ref(0)
const winner       = ref(null)

const current = computed(() => [pool.value[currentMatch.value * 2], pool.value[currentMatch.value * 2 + 1]])

const roundLabel = computed(() => {
  const n = roundSize.value
  if (n === 2)  return '결승'
  if (n === 4)  return '준결승'
  return `${n}강`
})

const progressPct = computed(() =>
  Math.round((currentMatch.value / totalMatches.value) * 100)
)

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function startGame(cat) {
  pool.value      = shuffle(cat.items)
  winners.value   = []
  currentMatch.value = 0
  roundSize.value = pool.value.length
  totalMatches.value = Math.floor(pool.value.length / 2)
  phase.value     = 'battle'
}

function pick(idx) {
  winners.value.push(current.value[idx])
  if (currentMatch.value + 1 < totalMatches.value) {
    currentMatch.value++
  } else {
    if (winners.value.length === 1) {
      winner.value = winners.value[0]
      phase.value  = 'result'
    } else {
      pool.value         = shuffle(winners.value)
      winners.value      = []
      currentMatch.value = 0
      roundSize.value    = pool.value.length
      totalMatches.value = Math.floor(pool.value.length / 2)
    }
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; min-height: 100vh; }
.sidebar { width: 220px; background: var(--primary); display: flex; flex-direction: column; padding: 1.5rem 1rem; gap: 2rem; flex-shrink: 0; }
.brand { color: #fff; font-size: 1.4rem; font-weight: 800; padding: 0 .5rem; }
nav { display: flex; flex-direction: column; gap: .3rem; flex: 1; }
.nav-item { display: block; padding: .7rem 1rem; border-radius: 8px; color: rgba(255,255,255,.75); font-weight: 500; transition: all .2s; }
.nav-item:hover, .nav-item.router-link-active { background: rgba(255,255,255,.15); color: #fff; }
.logout-btn { background: rgba(255,255,255,.15); color: #fff; border-radius: 8px; padding: .6rem; }

.content { flex: 1; display: flex; flex-direction: column; }
.top-bar { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid var(--border); background: var(--surface); }

.phase-wrap { padding: 2.5rem 2rem; display: flex; flex-direction: column; align-items: center; gap: 2rem; }
.phase-title { font-size: 1.4rem; font-weight: 700; }

.category-grid { display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: center; }
.cat-card { border: 2px solid transparent; cursor: pointer; text-align: center; padding: 2rem; width: 160px; transition: all .2s; }
.cat-card:hover { border-color: var(--primary); transform: translateY(-4px); }
.cat-emoji { font-size: 3rem; }
.cat-name  { font-size: 1.1rem; font-weight: 700; margin-top: .5rem; }
.cat-count { color: var(--text-muted); font-size: .9rem; }

.round-info { display: flex; gap: 1rem; align-items: center; }
.round-badge { background: var(--primary); color: #fff; border-radius: 20px; padding: .3rem 1rem; font-weight: 700; }
.progress-text { color: var(--text-muted); }

.battle-arena { display: flex; align-items: center; gap: 2rem; width: 100%; max-width: 800px; }
.candidate { flex: 1; cursor: pointer; text-align: center; padding: 3rem 2rem; border: 3px solid transparent; transition: all .25s; }
.candidate:hover { border-color: var(--primary); transform: scale(1.04); background: linear-gradient(135deg, #f0f4ff, #e8f4ff); }
.cand-emoji { font-size: 4rem; }
.cand-name  { font-size: 1.5rem; font-weight: 800; margin-top: .8rem; }
.vs-hint    { color: var(--text-muted); font-size: .85rem; margin-top: .5rem; }

.vs-circle { width: 64px; height: 64px; border-radius: 50%; background: var(--primary); color: #fff; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }

.progress-bar-wrap { width: 100%; max-width: 600px; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
.progress-bar { height: 100%; background: var(--primary); transition: width .4s; }

.result-wrap { text-align: center; }
.trophy { font-size: 5rem; }
.result-wrap h2 { font-size: 2rem; font-weight: 800; }
.winner { display: inline-flex; flex-direction: column; align-items: center; padding: 2.5rem 4rem; }
.winner-emoji { font-size: 5rem; }
.winner-name  { font-size: 1.8rem; font-weight: 800; margin-top: .8rem; }
.result-actions { display: flex; gap: 1rem; }
</style>
