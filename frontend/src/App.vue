<template>
  <div class="app-container">
    <nav class="sidebar glass-panel">
      <div class="logo">
        <div class="logo-icon">✨</div>
        <h2>AI Recruit</h2>
      </div>
      <ul class="nav-links">
        <li>
          <router-link to="/upload" class="nav-item">
            <span class="icon">📄</span> Resume Upload
          </router-link>
        </li>
        <li>
          <router-link to="/jobs" class="nav-item">
            <span class="icon">💼</span> Jobs
          </router-link>
        </li>
        <li>
          <router-link to="/notifications" class="nav-item">
            <span class="icon">🔔</span> Notifications
            <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
          </router-link>
        </li>
      </ul>
      <div class="user-profile">
        <div class="avatar">PM</div>
        <div class="info">
          <p class="name">airobin</p>
          <p class="role">Admin</p>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const unreadCount = ref(0)

const fetchUnreadCount = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/notifications')
    const unread = res.data.filter((n: any) => n.is_read === 0).length
    unreadCount.value = unread
  } catch (err) {
    console.error("Failed to fetch notifications unread count", err)
  }
}

onMounted(() => {
  fetchUnreadCount()
  
  // Simple periodic poll for unread count
  setInterval(fetchUnreadCount, 30000)
})
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  padding: 16px;
  gap: 24px;
}

.sidebar {
  width: 260px;
  display: flex;
  flex-direction: column;
  padding: 24px;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.logo h2 {
  font-size: 1.5rem;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.logo-icon {
  font-size: 1.8rem;
}

.nav-links {
  list-style: none;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-bottom: 8px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  transform: translateX(4px);
}

.nav-item.router-link-active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1));
  color: var(--primary);
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid var(--surface-border);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.info .name {
  font-weight: 600;
  font-size: 0.95rem;
}

.info .role {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 32px;
}

.unread-badge {
  background-color: #ef4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
  min-width: 20px;
  text-align: center;
}
</style>
