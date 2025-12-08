<template>
  <Navbar />

  <main class="container">
    <div class="row">
      <div class="col-6 offset-3">
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


            <div class="mt-2">
              <button
                v-if="isLoggedIn"
                class="btn btn-sm btn-outline-danger"
                :disabled="unfavoritingIds.includes(post.id)"
                @click="unfavoritePost(post.id)"
              >
                <span v-if="unfavoritingIds.includes(post.id)">Removendo...</span>
                <span v-else>Remover favorito</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Navbar from '~/components/Navbar.vue'
import { useAuth } from '~/stores/auth'

const posts = ref([])
const loading = ref(true)
const error = ref(null)

const FAVORITES_URL = 'http://127.0.0.1:8000/favorites/'
const FAVORITES_UNFAVORITE_URL = 'http://127.0.0.1:8000/favorites/unfavorite/'
const auth = useAuth()

const unfavoritingIds = ref([]) // track in-progress removals

const fetchPosts = async () => {
  loading.value = true
  error.value = null
  try {
    // require login for favorites
    if (!auth?.token) {
      error.value = 'You must be logged in to view favorites.'
      posts.value = []
      loading.value = false
      return
    }
    const res = await fetch(FAVORITES_URL, {
      headers: {
        'Content-Type': 'application/json',
        ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
      }
    })
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    const data = await res.json()
    // API may return paginated results or a plain array
    posts.value = Array.isArray(data) ? data : (data.results ?? [])
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

const isLoggedIn = computed(() => !!auth.token)

const unfavoritePost = async (contentId) => {
  if (!isLoggedIn.value) {
    alert('You must be logged in to remove favorites.')
    return
  }
  if (unfavoritingIds.value.includes(contentId)) return

  unfavoritingIds.value.push(contentId)
  try {
    const res = await fetch(FAVORITES_UNFAVORITE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
      },
      body: JSON.stringify({ content_id: contentId })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => null)
      throw new Error(txt || `${res.status} ${res.statusText}`)
    }
    // remove from local list on success
    posts.value = posts.value.filter(p => p.id !== contentId)
  } catch (err) {
    alert('Failed to remove favorite: ' + (err?.message || String(err)))
  } finally {
    unfavoritingIds.value = unfavoritingIds.value.filter(id => id !== contentId)
  }
}
</script>