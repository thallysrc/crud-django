<template>
  <Navbar />

  <main class="posts-container container">
    <h1 style="margin:16px 0; color:#fff;">Favoritos / Posts</h1>

    <div v-if="loading" class="post-card">
      Carregando posts...
    </div>

    <div v-else-if="error" class="post-card">
      Erro ao carregar posts: {{ error }}
    </div>

    <div v-else>
      <div v-if="posts.length === 0" class="post-card">
        Nenhum post encontrado.
      </div>

      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <div>
            <div class="post-title">{{ post.title }}</div>
            <div class="post-meta">ID: {{ post.id }} • {{ formatDate(post.created_at) }}</div>
          </div>
        </div>

        <div class="post-content">{{ post.description }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '~/components/Navbar.vue'

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

const formatDate = (iso) => {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}
</script>