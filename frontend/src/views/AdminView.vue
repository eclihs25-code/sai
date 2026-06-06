<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">⚡ SAI</div>
      <nav>
        <RouterLink to="/main"     class="nav-item">🏠 홈</RouterLink>
        <RouterLink to="/worldcup" class="nav-item">❤️ 이상형 월드컵</RouterLink>
        <RouterLink to="/admin"    class="nav-item">⚙️ 관리자</RouterLink>
      </nav>
      <button class="logout-btn" @click="handleLogout">로그아웃</button>
    </aside>

    <main class="content">
      <header class="top-bar">
        <h2>⚙️ 관리자 패널</h2>
        <div class="user-badge">{{ auth.user?.username }} <span class="role-tag admin">ADMIN</span></div>
      </header>

      <div class="admin-body">
        <!-- 탭 -->
        <div class="tabs">
          <button v-for="t in tabs" :key="t.key"
            :class="['tab-btn', { active: activeTab === t.key }]"
            @click="activeTab = t.key">
            {{ t.label }}
          </button>
        </div>

        <!-- 사용자 관리 -->
        <div v-if="activeTab === 'users'" class="card">
          <div class="section-head">
            <h3>사용자 목록</h3>
            <button class="btn-primary" @click="showAddUser = true">+ 사용자 추가</button>
          </div>
          <table class="data-table">
            <thead><tr><th>ID</th><th>아이디</th><th>역할</th><th>가입일</th><th>액션</th></tr></thead>
            <tbody>
              <tr v-for="u in users" :key="u.id">
                <td>{{ u.id }}</td>
                <td>{{ u.username }}</td>
                <td><span :class="['badge', u.role]">{{ u.role }}</span></td>
                <td>{{ u.created_at }}</td>
                <td>
                  <button class="btn-danger small" @click="deleteUser(u.id)">삭제</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 이상형 월드컵 관리 -->
        <div v-if="activeTab === 'worldcup'" class="card">
          <div class="section-head">
            <h3>월드컵 카테고리</h3>
            <button class="btn-primary" @click="showAddCategory = true">+ 카테고리 추가</button>
          </div>
          <table class="data-table">
            <thead><tr><th>ID</th><th>카테고리명</th><th>항목 수</th><th>상태</th><th>액션</th></tr></thead>
            <tbody>
              <tr v-for="c in categories" :key="c.id">
                <td>{{ c.id }}</td>
                <td>{{ c.name }}</td>
                <td>{{ c.count }}</td>
                <td><span :class="['badge', c.active ? 'admin' : 'user']">{{ c.active ? '활성' : '비활성' }}</span></td>
                <td><button class="btn-danger small" @click="deleteCategory(c.id)">삭제</button></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 통계 -->
        <div v-if="activeTab === 'stats'" class="card">
          <h3>서비스 통계</h3>
          <div class="stats-grid">
            <div class="stat-item" v-for="s in statsData" :key="s.label">
              <span class="s-icon">{{ s.icon }}</span>
              <span class="s-val">{{ s.value }}</span>
              <span class="s-label">{{ s.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 사용자 추가 모달 -->
    <div v-if="showAddUser" class="modal-overlay" @click.self="showAddUser = false">
      <div class="modal card">
        <h3>사용자 추가</h3>
        <div class="field"><label>아이디</label><input v-model="newUser.username" /></div>
        <div class="field"><label>비밀번호</label><input v-model="newUser.password" type="password" /></div>
        <div class="field">
          <label>역할</label>
          <select v-model="newUser.role">
            <option value="user">user</option>
            <option value="admin">admin</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn-primary" @click="addUser">추가</button>
          <button class="btn-secondary" @click="showAddUser = false">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const activeTab = ref('users')
const tabs = [
  { key: 'users',   label: '👥 사용자 관리' },
  { key: 'worldcup',label: '❤️ 월드컵 관리' },
  { key: 'stats',   label: '📊 통계' }
]

const users = ref([
  { id: 1, username: 'admin',  role: 'admin', created_at: '2026-01-01' },
  { id: 2, username: 'user1',  role: 'user',  created_at: '2026-03-10' },
  { id: 3, username: 'user2',  role: 'user',  created_at: '2026-05-22' }
])

const categories = ref([
  { id: 1, name: '음식', count: 16, active: true },
  { id: 2, name: '여행지', count: 32, active: true },
  { id: 3, name: '연예인', count: 16, active: false }
])

const statsData = [
  { icon: '👥', value: '1,284', label: '총 가입자' },
  { icon: '🎮', value: '342',   label: '월드컵 참여' },
  { icon: '🏆', value: '3',     label: '카테고리 수' },
  { icon: '📅', value: '156',   label: '오늘 방문자' }
]

const showAddUser     = ref(false)
const showAddCategory = ref(false)
const newUser = ref({ username: '', password: '', role: 'user' })

function addUser() {
  const id = users.value.length + 1
  users.value.push({ ...newUser.value, id, created_at: new Date().toISOString().slice(0,10) })
  showAddUser.value = false
  newUser.value = { username: '', password: '', role: 'user' }
}

function deleteUser(id) {
  users.value = users.value.filter(u => u.id !== id)
}

function deleteCategory(id) {
  categories.value = categories.value.filter(c => c.id !== id)
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 220px; background: var(--primary);
  display: flex; flex-direction: column;
  padding: 1.5rem 1rem; gap: 2rem; flex-shrink: 0;
}
.brand { color: #fff; font-size: 1.4rem; font-weight: 800; padding: 0 .5rem; }
nav { display: flex; flex-direction: column; gap: .3rem; flex: 1; }
.nav-item { display: block; padding: .7rem 1rem; border-radius: 8px; color: rgba(255,255,255,.75); font-weight: 500; transition: all .2s; }
.nav-item:hover, .nav-item.router-link-active { background: rgba(255,255,255,.15); color: #fff; }
.logout-btn { background: rgba(255,255,255,.15); color: #fff; border-radius: 8px; padding: .6rem; }

.content { flex: 1; display: flex; flex-direction: column; }
.top-bar { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid var(--border); background: var(--surface); }
.user-badge { display: flex; align-items: center; gap: .5rem; font-weight: 600; }
.role-tag { background: var(--primary); color: #fff; border-radius: 20px; padding: .15rem .7rem; font-size: .75rem; }
.role-tag.admin { background: var(--danger); }

.admin-body { padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem; }

.tabs { display: flex; gap: .5rem; }
.tab-btn { background: var(--surface); border: 1.5px solid var(--border); color: var(--text-muted); border-radius: 8px; padding: .5rem 1.2rem; font-weight: 600; transition: all .2s; }
.tab-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }

.section-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }

.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: .75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }
.data-table th { background: var(--bg); font-weight: 700; font-size: .875rem; color: var(--text-muted); }

.badge { border-radius: 20px; padding: .2rem .7rem; font-size: .78rem; font-weight: 700; }
.badge.admin { background: #fee2e2; color: var(--danger); }
.badge.user  { background: #e0e7ff; color: var(--primary); }

.small { padding: .3rem .7rem; font-size: .8rem; }

.stats-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1.5rem; margin-top: 1rem; }
.stat-item { display: flex; flex-direction: column; align-items: center; background: var(--bg); border-radius: 12px; padding: 1.5rem; }
.s-icon { font-size: 2rem; }
.s-val  { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
.s-label{ color: var(--text-muted); font-size: .9rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { width: 400px; display: flex; flex-direction: column; gap: 1rem; }
.modal h3 { margin-bottom: .5rem; }
.field { display: flex; flex-direction: column; gap: .3rem; }
.field label { font-weight: 600; font-size: .9rem; }
.modal-actions { display: flex; gap: .8rem; margin-top: .5rem; }
</style>
