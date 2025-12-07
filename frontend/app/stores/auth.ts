import { defineStore } from 'pinia'
import { ref } from 'vue'

const LOGIN_URL = 'http://127.0.0.1:8000/login/'
const ME_URL = 'http://127.0.0.1:8000/accounts/me/'

export const useAuth = defineStore('auth', () => {
  const user = ref<any | null>(null)
  const token = ref<string | null>(null)
  const isInitialized = ref(false)

  const saveToStorage = () => {
    if (process.server) return
    try {
      if (token.value) localStorage.setItem('auth_token', token.value)
      if (user.value) localStorage.setItem('auth_user', JSON.stringify(user.value))
    } catch {}
  }

  const loadFromStorage = () => {
    if (process.server) return
    try {
      const savedToken = localStorage.getItem('auth_token')
      const savedUser = localStorage.getItem('auth_user')

      if (savedToken) token.value = savedToken
      if (savedUser) user.value = JSON.parse(savedUser)
    } finally {
      isInitialized.value = true
    }
  }

  const getAuthHeader = () =>
    token.value ? { Authorization: `Token ${token.value}` } : {}

  const login = async (username: string, password: string) => {
    try {
      const res = await fetch(LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (!res.ok) return false

      const data = await res.json().catch(() => null)
      if (!data?.token) return false

      token.value = data.token

      const meRes = await fetch(ME_URL, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', ...getAuthHeader() }
      })

      if (meRes.ok) {
        user.value = await meRes.json().catch(() => null)
      }

      saveToStorage()
      return true
    } catch {
      return false
    }
  }

  const logout = () => {
    if (!process.server) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    }
    user.value = null
    token.value = null
  }

  if (process.client) loadFromStorage()

  return {
    user,
    token,
    isInitialized,
    login,
    logout,
    getAuthHeader,
    loadFromStorage
  }
})
