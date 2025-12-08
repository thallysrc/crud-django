<template>
  <nav class="app-navbar">
    <div class="nav-inner container">
      <div class="brand">
        <NuxtLink to="/">Home</NuxtLink>
      </div>

      <div class="nav-links">
        <NuxtLink to="/favoritos" class="nav-link">Favoritos</NuxtLink>
        <NuxtLink v-if="canCreate" to="/contents/create" class="nav-link">Criar</NuxtLink>
      </div>

      <div class="auth-area">
        <!-- not logged in -->
        <NuxtLink v-if="!auth.user" to="/login" class="nav-link auth-link">
          Login
        </NuxtLink>

        <!-- logged in -->
        <button v-else @click="logout" class="auth-btn">
          Logout ({{ auth.user.username }})
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuth } from '~/stores/auth'
import { navigateTo } from '#app'

const auth = useAuth()


onMounted(() => {
  auth.loadFromStorage()
  console.log(auth.user)
})

const canCreate = computed(() => {
  if (!auth.user) return false

  return Array.isArray(auth.user.permissions) &&
    auth.user.permissions.includes('add_content')
})

const logout = () => {
  auth.logout()
  navigateTo('/')
}
</script>
