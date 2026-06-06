<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">⚡ SAI</div>
      <nav>
        <RouterLink to="/main"     class="nav-item active">🏠 홈</RouterLink>
        <RouterLink to="/worldcup" class="nav-item">❤️ 이상형 월드컵</RouterLink>
        <RouterLink v-if="auth.isAdmin" to="/admin" class="nav-item">⚙️ 관리자</RouterLink>
      </nav>
      <button class="logout-btn" @click="handleLogout">로그아웃</button>
    </aside>

    <main class="content">
      <header class="top-bar">
        <h2>대시보드</h2>
        <div class="user-badge">{{ auth.user?.username }} <span class="role-tag">{{ auth.user?.role }}</span></div>
      </header>

      <div class="stats-grid">
        <div class="stat-card card" v-for="s in stats" :key="s.label">
          <div class="stat-icon">{{ s.icon }}</div>
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>

      <div class="card notice-card">
        <h3>📢 공지사항</h3>
        <ul class="notice-list">
          <li v-for="n in notices" :key="n.id">
            <span class="notice-date">{{ n.date }}</span>
            <span>{{ n.title }}</span>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const stats = [
  { icon: '👥', value: '1,284', label: '전체 사용자' },
  { icon: '❤️', value: '342',   label: '이상형 월드컵 참여' },
  { icon: '🏆', value: '56',    label: '오늘 완료' },
  { icon: '📊', value: '98%',   label: '서버 가동률' }
]

const notices = ref([
  { id: 1, date: '2026-06-06', title: '시스템 점검 안내 (06/10 02:00 ~ 04:00)' },
  { id: 2, date: '2026-06-01', title: '이상형 월드컵 신규 카테고리가 추가되었습니다.' },
  { id: 3, date: '2026-05-20', title: 'SAI 서비스 오픈을 환영합니다!' }
])

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 220px;
  background: var(--primary);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  gap: 2rem;
  flex-shrink: 0;
}

.brand { color: #fff; font-size: 1.4rem; font-weight: 800; padding: 0 .5rem; }

nav { display: flex; flex-direction: column; gap: .3rem; flex: 1; }

.nav-item {
  display: block;
  padding: .7rem 1rem;
  border-radius: 8px;
  color: rgba(255,255,255,.75);
  font-weight: 500;
  transition: all .2s;
}
.nav-item:hover, .nav-item.router-link-active {
  background: rgba(255,255,255,.15);
  color: #fff;
}

.logout-btn {
  background: rgba(255,255,255,.15);
  color: #fff;
  border-radius: 8px;
  padding: .6rem;
}
.logout-btn:hover { background: rgba(255,255,255,.3); }

.content { flex: 1; display: flex; flex-direction: column; }

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}
.top-bar h2 { font-size: 1.3rem; }

.user-badge { display: flex; align-items: center; gap: .5rem; font-weight: 600; }
.role-tag {
  background: var(--primary);
  color: #fff;
  border-radius: 20px;
  padding: .15rem .7rem;
  font-size: .75rem;
  text-transform: uppercase;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.2rem;
  padding: 2rem;
}

.stat-card { text-align: center; }
.stat-icon { font-size: 2rem; margin-bottom: .5rem; }
.stat-value { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
.stat-label { color: var(--text-muted); font-size: .9rem; margin-top: .2rem; }

.notice-card { margin: 0 2rem 2rem; }
.notice-card h3 { margin-bottom: 1rem; }
.notice-list { list-style: none; display: flex; flex-direction: column; gap: .8rem; }
.notice-list li { display: flex; gap: 1rem; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: .8rem; }
.notice-list li:last-child { border: none; padding: 0; }
.notice-date { color: var(--text-muted); font-size: .85rem; white-space: nowrap; }
</style>
