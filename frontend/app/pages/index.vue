<template>
  <Navbar/>

  <div class="container">
    <div class="row">
      <div class="col-4 offset-4">
        <div class="mb-3">
          <input
            v-model="searchTerm"
            class="form-control"
            type="search"
            placeholder="Search title or description..."
            aria-label="Search posts"
          />
          <div class="mt-2">
            <button v-if="searchTerm" @click="clearSearch" class="btn btn-sm btn-outline-secondary">Clear</button>
          </div>
        </div>

        <div v-if="loading">Carregando posts...</div>
        <div v-else-if="error">Erro: {{ error }}</div>
        <div v-else>
          <div v-if="posts.length === 0">Nenhum post encontrado.</div>
          <div v-else>
            <div v-for="post in posts" :key="post.id" class="post-card">
              <h2 class="post-title">{{ post.title }}</h2>
              <div class="post-meta">{{ formatDate(post.created_at) }}</div>
              <p class="post-content">{{ post.description }}</p>
              <i class="fa-solid fa-user"></i>

              <div class="mt-2 d-flex gap-2" >
                <button
                  v-if="isLoggedIn"
                  class="btn btn-sm btn-outline-warning"
                  :disabled="favoritingIds.includes(post.id) || favorited.includes(post.id)"
                  @click="favoritePost(post.id)"
                  :title="favorited.includes(post.id) ? 'Favorited' : 'Favorite'"
                >
                  <span v-if="favorited.includes(post.id)">★ Favorited</span>
                  <span v-else-if="favoritingIds.includes(post.id)">...Favoriting</span>
                  <span v-else>☆ Favorite</span>
                </button>

                <div>
                  <button
                    v-if="canDelete(post.author)"
                    class="btn btn-sm btn-danger"
                    @click="confirmDelete(post.id)"
                  >Exclude</button>
                  <button
                    v-if="canEdit(post.author)"
                    class="btn btn-sm btn-primary"
                    @click="editPost(post.id)"
                  >Edit</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '~/components/Navbar.vue'
import { useAuth } from '~/stores/auth'
import { ref, onMounted, watch, computed } from 'vue'

const auth = useAuth()

const posts = ref([])
const loading = ref(true)
const error = ref(null)

const API_URL = 'http://127.0.0.1:8000/'

const fetchPosts = async (search = '') => {
  loading.value = true
  error.value = null
  try {
    const q = search ? `?search=${encodeURIComponent(search)}` : ''
    const res = await fetch(`${API_URL}contents/${q}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
      }
    })
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    const data = await res.json()

    posts.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch (err) {
    error.value = err?.message || String(err)
    posts.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPosts())

const searchTerm = ref('')
let searchTimer = null
watch(searchTerm, (val) => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchPosts(val.trim())
    searchTimer = null
  }, 300)
})

const clearSearch = () => {
  searchTerm.value = ''
  fetchPosts('')
}

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

const favoritingIds = ref([])
const favorited = ref([]) 

const favoritePost = async (id) => {
  if (favoritingIds.value.includes(id) || favorited.value.includes(id)) return
  favoritingIds.value.push(id)
  try {
    const res = await fetch(`${API_URL}/favorites/favorite/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
      },
      body: JSON.stringify({
        content_id: id 
      })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => null)
      throw new Error(txt || `${res.status} ${res.statusText}`)
    }

    if (!favorited.value.includes(id)) favorited.value.push(id)
  } catch (err) {
    alert('Favorite failed: ' + (err?.message || String(err)))
  } finally {
    favoritingIds.value = favoritingIds.value.filter(x => x !== id)
  }
}

const confirmDelete = async (id) => {
  if (!confirm('Confirm delete this post?')) return
  try {
    const res = await fetch(`${API_URL}contents/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
      }
    })
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    posts.value = posts.value.filter(p => p.id !== id)
    favorited.value = favorited.value.filter(x => x !== id)
  } catch (err) {
    alert('Delete failed: ' + (err?.message || String(err)))
  }
}

const isLoggedIn = computed(() => !!auth.token)

const editPost = (id) => {
  navigateTo(`/contents/create?id=${encodeURIComponent(id)}`)
}

const canEdit = ((author_id) => {
  if (!author_id) return false
  if (auth.user.id == author_id) return true
})

const canDelete = ((author_id) => {
  if (!author_id) return false
  if (auth.user && auth.user.id == author_id) return true
})


</script>