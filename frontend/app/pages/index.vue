<template>
  <Navbar/>

  <div class="container">
    <div class="row">
      <div class="col-4 offset-4">
        <div v-if="loading">Carregando posts...</div>
        <div v-else-if="error">Erro: {{ error }}</div>
        <div v-else>
          <div v-for="post in posts" :key="post.id" class="post-card">
            <h2 class="post-title">{{ post.title }}</h2>
            <div class="post-meta">{{ formatDate(post.created_at) }} • ID: {{ post.id }}</div>
            <p class="post-content">{{ post.description }}</p>
            <i class="fa-solid fa-user"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import Navbar from '~/components/Navbar.vue'
import { useAuth } from '~/stores/auth'
import { ref, onMounted } from 'vue'

const auth = useAuth()

const posts = ref([])
const loading = ref(true)
const error = ref(null)

const API_URL = 'http://127.0.0.1:8000/contents/'

const fetchPosts = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(API_URL)
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    const data = await res.json()
    posts.value = data.results ?? []
  } catch (err) {
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchPosts)

const logout = () => {
  auth.logout()
  navigateTo('/login')
}

const formatDate = (iso) => {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}
</script>