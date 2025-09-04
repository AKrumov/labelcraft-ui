import { defineStore } from 'pinia'
import api from '../api'

interface User {
  id: number
  email: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null as User | null,
  }),
  actions: {
    async login(email: string, password: string) {
      const body = new URLSearchParams()
      body.append('username', email)
      body.append('password', password)
      const { data } = await api.post('/auth/login', body)
      this.token = data.access_token
      localStorage.setItem('token', this.token)
    },
    logout() {
      this.token = ''
      localStorage.removeItem('token')
    },
  },
})
