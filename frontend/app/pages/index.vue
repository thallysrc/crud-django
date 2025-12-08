<template>
  <Navbar/>

  <div class="container">
    <div class="row">
      <div class="col-6 offset-3">
        <div class="toolbar">
          <input
            v-model="searchTerm"
            class="toolbar__search"
            type="search"
            placeholder="Pesquise por Titulo ou Descrição"
            aria-label="Search posts"
          />

          <div class="toolbar__actions">
            <button v-if="searchTerm" @click="clearSearch" class="btn btn--clear">Clear</button>
             <button v-if="isLoggedIn"
                    @click="toggleMyContent"
                    class="btn btn--my"
                    :class="{ 'btn--active': myContent }"
            >
              {{ myContent ? 'Meus conteúdos: ON' : 'Meus conteúdos: OFF' }}
            </button>

            <button @click="toggleOrdering"
                    class="btn btn--order"
                    :class="{ 'btn--active': ordering !== '-created_at' }"
            >
              {{ ordering === '-created_at' ? 'Data: Mais recentes' : 'Data: Mais antigos' }}
            </button>

           
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

              <div class="post-actions">
                <button
                  v-if="isLoggedIn"
                  class="btn btn-fav"
                  :disabled="favoritingIds.includes(post.id) || favorited.includes(post.id)"
                  @click="favoritePost(post.id)"
                >
                  <span v-if="favorited.includes(post.id)">★ Favoritado</span>
                  <span v-else-if="favoritingIds.includes(post.id)">...Favoritando</span>
                  <span v-else>☆ Favoritar</span>
                </button>

                <button v-if="canDelete(post.author)" class="btn btn-del" @click="confirmDelete(post.id)">Deletar</button>
                <button v-if="canEdit(post.author)" class="btn btn-edit" @click="editPost(post.id)">Editar</button>
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


const ordering = ref('-created_at')

const myContent = ref(false)

const toggleMyContent = () => {
  myContent.value = !myContent.value
  fetchPosts(searchTerm.value.trim(), ordering.value, myContent.value)
}

const toggleOrdering = () => {
  ordering.value = ordering.value === '-created_at' ? 'created_at' : '-created_at'
  fetchPosts(searchTerm.value.trim(), ordering.value, myContent.value)
}

const fetchPosts = async (search = '', orderingParam = ordering.value, myContentParam = myContent.value) => {
    loading.value = true
    error.value = null
    try {
    const parts = []
    if (search) parts.push(`search=${encodeURIComponent(search)}`)
    if (orderingParam) parts.push(`ordering=${encodeURIComponent(orderingParam)}`)
    if (myContentParam) parts.push(`my_content=true`)
     const q = parts.length ? `?${parts.join('&')}` : ''
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
 
onMounted(() => fetchPosts('', ordering.value, myContent.value))

const searchTerm = ref('')
let searchTimer = null
watch(searchTerm, (val) => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchPosts(val.trim(), ordering.value, myContent.value)
    searchTimer = null
  }, 300)
})

const clearSearch = () => {
  searchTerm.value = ''
  fetchPosts('', ordering.value, myContent.value)
}

watch(ordering, (val) => { fetchPosts(searchTerm.value.trim(), val, myContent.value) })
watch(myContent, (val) => { fetchPosts(searchTerm.value.trim(), ordering.value, val) })


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
  if (auth.user && (auth.user.id == author_id || auth.user.groups.includes('admin'))) return true
})

const canDelete = ((author_id) => {
  if (!author_id) return false
  if (auth.user && (auth.user.id == author_id || auth.user.groups.includes('admin'))) return true
})


</script>