<template>
  <div class="login-wrap">
    <div class="login-card card">
      <div class="logo">
        <span class="logo-icon">⚡</span>
        <h1>SAI</h1>
      </div>
      <p class="subtitle">서비스에 오신 것을 환영합니다</p>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>아이디</label>
          <input v-model="form.username" type="text" placeholder="아이디를 입력하세요" required />
        </div>
        <div class="field">
          <label>비밀번호</label>
          <input v-model="form.password" type="password" placeholder="비밀번호를 입력하세요" required />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button class="btn-primary submit-btn" type="submit" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const form  = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    router.push('/main')
  } catch (e) {
    error.value = e.response?.data?.detail || '로그인에 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: .6rem;
  margin-bottom: .4rem;
}

.logo-icon { font-size: 2rem; }
.logo h1 { font-size: 2rem; font-weight: 800; color: var(--primary); }

.subtitle { color: var(--text-muted); margin-bottom: 2rem; }

.field { margin-bottom: 1.2rem; }
.field label { display: block; font-weight: 600; margin-bottom: .4rem; font-size: .9rem; }

.error-msg { color: var(--danger); font-size: .875rem; margin-bottom: .8rem; }

.submit-btn { width: 100%; padding: .85rem; margin-top: .5rem; font-size: 1rem; }
.submit-btn:disabled { opacity: .6; cursor: not-allowed; }
</style>
