<template>
  <Navbar />

  <main class="container" style="max-width:700px; margin:24px auto;">
    <h1 style="margin-bottom:16px;">Criar Post</h1>

    <form @submit.prevent="createPost" class="post-card" style="background:#fff;">
      <div style="margin-bottom:12px;">
        <label for="title" style="display:block; font-weight:600; margin-bottom:6px;">Título</label>
        <input id="title" v-model="title" type="text" placeholder="Título do post"
               style="width:100%; padding:8px; border:1px solid #ccc; border-radius:6px;" />
      </div>

      <div style="margin-bottom:12px;">
        <label for="description" style="display:block; font-weight:600; margin-bottom:6px;">Descrição</label>
        <textarea id="description" v-model="description" rows="6" placeholder="Descrição"
                  style="width:100%; padding:8px; border:1px solid #ccc; border-radius:6px;"></textarea>
      </div>

      <div style="display:flex; gap:8px; align-items:center;">
        <button type="submit" :disabled="loading" style="padding:8px 14px; border-radius:6px; cursor:pointer;">
          {{ loading ? 'Enviando...' : 'Criar Post' }}
        </button>

        <button type="button" @click="reset" style="padding:8px 12px; border-radius:6px; background:#f2f2f2;">
          Reset
        </button>

        <div v-if="error" style="color:#b00020; margin-left:12px;">{{ error }}</div>
        <div v-if="success" style="color:green; margin-left:12px;">Post criado com sucesso!</div>
      </div>
    </form>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '~/components/Navbar.vue'
import { useAuth } from '~/stores/auth'

const title = ref('')
const description = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(false)

const API_URL = 'http://127.0.0.1:8000/contents/'

const router = useRouter()
const auth = useAuth()


onMounted(() => {
  if (!auth.user) {
    router.push('/login')
  }
})

const getAuthHeader = () => {
  if (!auth) return {}
  if (auth.token) return { Authorization: `Token ${auth.token}` }
  return {}
}

const createPost = async () => {
  error.value = null
  success.value = false

  if (!title.value.trim() || !description.value.trim()) {
    error.value = 'Preencha título e descrição.'
    return
  }

  loading.value = true
  try {
    const headers = {
      'Content-Type': 'application/json',
      ...getAuthHeader()
    }

    const res = await fetch(API_URL, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        title: title.value.trim(),
        description: description.value.trim()
      })
    })

    if (!res.ok) {
      const text = await res.text().catch(() => null)
      throw new Error(text || `${res.status} ${res.statusText}`)
    }

    success.value = true
    setTimeout(() => {
      router.push('/')
    }, 700)
  } catch (err) {
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}

const reset = () => {
  title.value = ''
  description.value = ''
  error.value = null
  success.value = false
}
</script>
