<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Bell, CheckCircle2, UserPlus, CalendarDays, Briefcase, Info } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

interface Notification {
  id: number
  title: string
  message: string
  type: 'system' | 'new_candidate' | 'interview_scheduled' | 'job_created'
  is_read: number
  created_at: string
}

const notifications = ref<Notification[]>([])
const isLoading = ref(false)

const fetchNotifications = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/v1/notifications')
    notifications.value = res.data
  } catch (error) {
    console.error("Failed to load notifications", error)
    ElMessage.error("获取通知失败")
  } finally {
    isLoading.value = false
  }
}

const markAsRead = async (id: number) => {
  try {
    await axios.put(`http://localhost:8000/api/v1/notifications/${id}/read`)
    const target = notifications.value.find(n => n.id === id)
    if (target) target.is_read = 1
  } catch (err) {
    console.error(err)
  }
}

const markAllRead = async () => {
  try {
    await axios.post('http://localhost:8000/api/v1/notifications/mark-all-read')
    notifications.value.forEach(n => n.is_read = 1)
    ElMessage.success("全部标记为已读")
  } catch (err) {
    console.error(err)
  }
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN', { 
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
  })
}

const getIcon = (type: string) => {
  switch (type) {
    case 'new_candidate': return UserPlus
    case 'interview_scheduled': return CalendarDays
    case 'job_created': return Briefcase
    default: return Info
  }
}

const getIconColor = (type: string) => {
  switch (type) {
    case 'new_candidate': return 'text-emerald-400 bg-emerald-500/10'
    case 'interview_scheduled': return 'text-amber-400 bg-amber-500/10'
    case 'job_created': return 'text-blue-400 bg-blue-500/10'
    default: return 'text-zinc-400 bg-zinc-500/10'
  }
}

onMounted(() => {
  fetchNotifications()
})
</script>

<template>
  <div class="h-full flex flex-col space-y-6 max-w-4xl mx-auto w-full">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white mb-1">消息中心</h1>
        <p class="text-zinc-400 text-sm">在这里查看所有的系统提醒与关键进度通知。</p>
      </div>
      <el-button @click="markAllRead" class="!bg-surface !border-zinc-700 !text-zinc-300 hover:!text-white" size="large">
        <template #icon><el-icon><CheckCircle2 /></el-icon></template>
        全部标为已读
      </el-button>
    </div>

    <div v-if="isLoading" class="text-center py-12 text-zinc-500">
      加载中...
    </div>
    
    <div v-else-if="notifications.length === 0" class="bg-surface rounded-xl border border-zinc-800 p-12 text-center flex flex-col items-center justify-center">
      <Bell class="w-12 h-12 text-zinc-700 mb-4" />
      <h3 class="text-lg font-medium text-white mb-1">暂无通知</h3>
      <p class="text-zinc-500 text-sm">当有新职位发布或候选人投递时，这里会有提示。</p>
    </div>

    <div v-else class="space-y-3 pb-8">
      <div v-for="notice in notifications" :key="notice.id"
           class="group bg-surface rounded-xl border p-4 flex gap-4 transition-all duration-300 relative overflow-hidden cursor-pointer hover:bg-zinc-800/50"
           :class="notice.is_read ? 'border-zinc-800/40 opacity-70' : 'border-primary-500/30 bg-primary-500/5'"
           @click="markAsRead(notice.id)">
        
        <div class="shrink-0 rounded-full p-2.5 h-fit" :class="getIconColor(notice.type)">
          <component :is="getIcon(notice.type)" class="w-5 h-5" />
        </div>
        
        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-4 mb-1">
            <h4 class="text-base font-medium truncate" :class="notice.is_read ? 'text-zinc-300' : 'text-primary-100 font-semibold'">
              {{ notice.title }}
            </h4>
            <span class="text-xs shrink-0" :class="notice.is_read ? 'text-zinc-500' : 'text-primary-400 font-medium'">
              {{ formatDate(notice.created_at) }}
            </span>
          </div>
          <p class="text-sm text-zinc-400 line-clamp-2">{{ notice.message }}</p>
        </div>
        
        <!-- Unread Indicator Dot -->
        <div v-if="!notice.is_read" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary-500 rounded-r-full"></div>
      </div>
    </div>
  </div>
</template>
