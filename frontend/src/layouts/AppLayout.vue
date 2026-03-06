<script setup lang="ts">
import { RouterView } from 'vue-router'
import { LayoutDashboard, Briefcase, Users, CalendarDays, Settings } from 'lucide-vue-next'

const menuItems = [
  { name: '概览', icon: LayoutDashboard, path: '/dashboard' },
  { name: '职位管理', icon: Briefcase, path: '/jobs' },
  { name: '候选人池', icon: Users, path: '/candidates' },
  { name: '面试安排', icon: CalendarDays, path: '/interviews' },
  { name: '设置', icon: Settings, path: '/settings' },
]
</script>

<template>
  <div class="h-screen w-full flex bg-background text-zinc-100 overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 flex flex-col border-r border-zinc-800 bg-surface transition-all duration-300">
      <div class="h-16 flex items-center px-6 border-b border-zinc-800">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-primary-500/20">
            AI
          </div>
          <span class="font-semibold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-zinc-100 to-zinc-400">
            智谱招聘
          </span>
        </div>
      </div>
      
      <nav class="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 text-sm font-medium group"
          active-class="bg-primary-500/10 text-primary-400"
          :class="[$route.path.startsWith(item.path) ? 'bg-primary-500/10 text-primary-400' : 'text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200']"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 transition-colors"
            :class="[$route.path.startsWith(item.path) ? 'text-primary-500' : 'text-zinc-500 group-hover:text-zinc-400']"
          />
          {{ item.name }}
        </router-link>
      </nav>
      
      <div class="p-4 border-t border-zinc-800">
        <div class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-zinc-800/50 transition-colors cursor-pointer">
          <div class="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center text-sm font-medium text-zinc-300">
            HR
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-medium text-zinc-200">王专员</span>
            <span class="text-xs text-zinc-500">人力资源部</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-16 flex items-center justify-between px-8 border-b border-zinc-800 bg-surface/50 backdrop-blur-sm z-10 sticky top-0">
        <h2 class="text-lg font-medium text-zinc-100">{{ $route.meta.title || '概览' }}</h2>
        <div class="flex items-center gap-4">
          <el-button circle class="!bg-zinc-800 !border-zinc-700 hover:!bg-zinc-700 hover:!border-zinc-600">
            <template #icon><el-icon><bell /></el-icon></template>
          </el-button>
        </div>
      </header>
      
      <main class="flex-1 overflow-y-auto p-8 relative">
        <div class="max-w-7xl mx-auto h-full">
          <!-- Page transitions -->
          <router-view v-slot="{ Component }">
            <transition name="fade-slide" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<style>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Customize Element-Plus Dark Theme slightly for premium feel */
.el-button {
  --el-button-bg-color: transparent !important;
}
</style>
