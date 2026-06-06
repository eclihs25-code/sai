import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user  = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(username, password) {
    const form = new URLSearchParams({ username, password })
    const { data } = await api.post('/auth/token', form)
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchMe()
  }

  async function fetchMe() {
    const { data } = await api.get('/auth/me')
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isAdmin, login, logout, fetchMe }
})
