import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest, RegisterRequest } from '@/types'
import apiClient from '@/api/axios'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<User | null>(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => !!token.value)

  async function login(data: LoginRequest) {
    loading.value = true
    try {
      const formData = new FormData()
      formData.append('username', data.username)
      formData.append('password', data.password)

      const response = await apiClient.post('/user/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      await fetchUserInfo()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterRequest) {
    loading.value = true
    try {
      await apiClient.post('/user/register', data)
      return true
    } catch (error) {
      console.error('Register failed:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUserInfo() {
    if (!token.value) return
    try {
      const response = await apiClient.get('/user/me')
      userInfo.value = response.data
    } catch (error) {
      console.error('Fetch user info failed:', error)
      logout()
    }
  }

  function logout() {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    userInfo,
    loading,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    logout,
  }
})
