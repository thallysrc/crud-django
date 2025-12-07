<template>
  <nav class="app-navbar">
    <div class="nav-inner container">
      <div class="brand">
        <NuxtLink to="/">Home</NuxtLink>
      </div>

      <div class="nav-links">
        <NuxtLink to="/favoritos" class="nav-link">Favoritos</NuxtLink>
        <NuxtLink v-if="canCreate" to="/create" class="nav-link">Criar</NuxtLink>
      </div>

      <div class="auth-area">
        <NuxtLink v-if="!auth.user" to="/login" class="nav-link auth-link">
          Login
        </NuxtLink>

        <button v-else @click="logout" class="auth-btn">
          Logout ({{ auth.user.username }})
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from '~/stores/auth'
const auth = useAuth()

const canCreate = computed(() => {
  return Array.isArray(auth.permissions) && auth.permissions.includes('add_content')
})

const logout = () => {
  auth.logout()
  navigateTo('/')
}
</script>