import { defineStore } from 'pinia'
import { ref } from 'vue'

const LOGIN_URL = 'http://127.0.0.1:8000/login/'
const ME_URL = 'http://127.0.0.1:8000/accounts/me/'

export const useAuth = defineStore('auth', () => {
  const user = ref<null | any>(null)
  const token = ref<string | null>(null)
  const permissions = ref<string[]>([])

  try {
    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('auth_user')
    const savedPerms = localStorage.getItem('auth_permissions')
    if (savedToken) token.value = savedToken
    if (savedUser) user.value = JSON.parse(savedUser)
    if (savedPerms) permissions.value = JSON.parse(savedPerms)
  } catch {
  }


  const getAuthHeader = () => {
    if (!token.value) return {}
    return { Authorization: `Token ${token.value}` }
  }


  const login = async (username: string, password: string) => {
    try {
      const res = await fetch(LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (!res.ok) {
        const text = await res.text().catch(() => null)
        console.error('Login failed:', res.status, text)
        return false
      }

      const data = await res.json().catch(() => null) ?? {}

  
      if (data.token) {
        token.value = data.token
        try {
          localStorage.setItem('auth_token', token.value)
        } catch {
        }
      } else {
        console.error('Login response did not include token', data)
        return false
      }

      try {
        const meRes = await fetch(ME_URL, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...getAuthHeader()
          }
        })

        if (meRes.ok) {
          const meData = await meRes.json().catch(() => null) ?? {}
          user.value = meData

          permissions.value = Array.isArray(meData.permissions) ? meData.permissions : []
          try {
            localStorage.setItem('auth_permissions', JSON.stringify(permissions.value))
          } catch {
          }
        } else {

          console.warn('Could not fetch /accounts/me/:', meRes.status)
          user.value = { username }
          permissions.value = []
        }
      } catch (err) {
        console.warn('Error fetching /accounts/me/:', err)
        user.value = { username }
        permissions.value = []
      }

      try {
        localStorage.setItem('auth_user', JSON.stringify(user.value))
      } catch {
      }

      return true
    } catch (err) {
      console.error('Login error', err)
      return false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    permissions.value = []
    try {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      localStorage.removeItem('auth_permissions')
    } catch {
    }
  }

  return { user, token, permissions, login, logout, getAuthHeader }
})