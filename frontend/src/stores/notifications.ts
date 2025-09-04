import { defineStore } from 'pinia'

export interface Notification {
  id: number
  message: string
  type: 'success' | 'error'
}

let counter = 0

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    items: [] as Notification[],
  }),
  actions: {
    notify(message: string, type: 'success' | 'error' = 'success', duration = 3000) {
      const id = ++counter
      this.items.push({ id, message, type })
      setTimeout(() => this.remove(id), duration)
    },
    remove(id: number) {
      this.items = this.items.filter((n) => n.id !== id)
    },
  },
})
