<template>
  <Navbar />

  <div class="container">
    <div class="row">
      <div class="col-6 offset-3">
        <h3>{{ isEdit ? 'Editar conteúdo' : 'Criar conteúdo' }}</h3>

        <div v-if="loading" class="loading">Carregando...</div>
        <div v-else>
          <div class="mb-3">
            <label class="form-label">Titulo</label>
            <input v-model="title" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Descrição</label>
            <textarea v-model="description" class="form-control" rows="6"></textarea>
          </div>

          <div v-if="error" class="alert-danger">{{ error }}</div>

          <div class="d-flex-gap-2">
            <button class="btn btn-primary" @click="save" :disabled="saving">
              {{ saving ? 'Salvando...' : (isEdit ? 'Atualizar' : 'Criar') }}
            </button>
            <button class="btn btn-secondary" @click="cancel" :disabled="saving">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '~/components/Navbar.vue'
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '~/stores/auth'

const auth = useAuth()
const route = useRoute()

const API_URL = 'http://127.0.0.1:8000/contents/'

const idRaw = route.query.id
const id = idRaw ? String(idRaw) : null
const isEdit = computed(() => !!id)

const title = ref('')
const description = ref('')

const loading = ref(false)
const saving = ref(false)
const removing = ref(false)
const error = ref(null)

const getHeaders = () => ({
  'Content-Type': 'application/json',
  ...(typeof auth.getAuthHeader === 'function' ? auth.getAuthHeader() : {})
})

onMounted(async () => {
  if (!id) return
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_URL}${id}/`, {
      headers: getHeaders()
    })
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    const data = await res.json()
    title.value = data.title ?? ''
    description.value = data.description ?? ''
  } catch (err) {
    error.value = err?.message || String(err)
  } finally {
    loading.value = false
  }
})

const save = async () => {
  saving.value = true
  error.value = null
  try {
    const body = JSON.stringify({ title: title.value, description: description.value })
    const url = isEdit.value ? `${API_URL}${id}/` : API_URL
    const method = isEdit.value ? 'PUT' : 'POST'
    const res = await fetch(url, {
      method,
      headers: getHeaders(),
      body
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => null)
      throw new Error(txt || `${res.status} ${res.statusText}`)
    }
    navigateTo('/')
  } catch (err) {
    error.value = err?.message || String(err)
  } finally {
    saving.value = false
  }
}

const cancel = () => {
  navigateTo('/')
}
</script>