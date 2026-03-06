<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { UploadCloud, MoreHorizontal, Sparkles, Filter } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

const router = useRouter()

const columns = ref([
  { id: 'new', title: '新投递 / 解析中', color: 'border-blue-500', bg: 'bg-blue-500/10' },
  { id: 'screening', title: 'AI 初筛完成', color: 'border-emerald-500', bg: 'bg-emerald-500/10' },
  { id: 'interview', title: '面试中', color: 'border-purple-500', bg: 'bg-purple-500/10' },
  { id: 'offer', title: '录用待入职', color: 'border-pink-500', bg: 'bg-pink-500/10' },
  { id: 'rejected', title: '已淘汰', color: 'border-zinc-500', bg: 'bg-zinc-500/10' },
])

const candidates = ref<any[]>([])
const isLoading = ref(false)

const fetchCandidates = async () => {
    isLoading.value = true
    try {
        const data = await request.get('/candidates/')
        candidates.value = data as unknown as any[]
    } catch(e) {
        ElMessage.error('Failed to fetch candidates pipeline')
        console.error(e)
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchCandidates()
})

const getCandidatesByStatus = (status: string) => {
  return candidates.value.filter(c => c.status === status)
}

const onFileDrop = () => {
  router.push('/upload')
}

const viewCandidate = (id: number) => {
  // Navigation to detail
  // router.push(`/candidates/${id}`)
  ElMessage.info(`Coming soon: View details for candidate ID ${id}`)
}
</script>

<template>
  <div class="h-full flex flex-col space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white mb-1">候选人流水线 (Pipeline)</h1>
        <p class="text-zinc-400 text-sm">拖拽卡片流转状态。平台会自动解析新简历并提供 AI 打分推荐。</p>
      </div>
      <div class="flex items-center gap-3">
        <el-button class="!bg-surface !border-zinc-700 !text-white hover:!bg-zinc-800">
          <template #icon><el-icon><Filter /></el-icon></template>
          全部职位
        </el-button>
        <el-button type="primary" class="!bg-primary-600 hover:!bg-primary-500 !border-none" @click="onFileDrop">
          <template #icon><el-icon><UploadCloud /></el-icon></template>
          批量上传简历
        </el-button>
      </div>
    </div>

    <!-- Kanban Board -->
    <div class="flex-1 overflow-x-auto pb-4">
      <div class="flex gap-6 h-full min-w-max">
        
        <!-- Column -->
        <div v-for="col in columns" :key="col.id" class="w-80 flex flex-col bg-background/50 rounded-xl border border-zinc-800/80 overflow-hidden shrink-0 filter drop-shadow-sm">
          
          <div class="p-4 border-b border-zinc-800/80 flex items-center justify-between bg-surface/30 backdrop-blur-sm">
            <div class="flex items-center gap-2">
              <div :class="['w-2.5 h-2.5 rounded-full border-2', col.color, col.bg]"></div>
              <h3 class="font-medium text-white text-sm">{{ col.title }}</h3>
            </div>
            <span class="text-xs font-medium text-zinc-500 bg-zinc-800/50 px-2 py-0.5 rounded-full">
              {{ getCandidatesByStatus(col.id).length }}
            </span>
          </div>

          <!-- Cards Area -->
          <div class="flex-1 overflow-y-auto p-3 space-y-3 kanban-scroll">
            <div v-for="c in getCandidatesByStatus(col.id)" :key="c.id" 
                 @click="viewCandidate(c.id)"
                 class="bg-surface border border-zinc-800 hover:border-zinc-600 rounded-lg p-4 cursor-pointer transition-all hover:-translate-y-0.5 shadow-sm group relative">
              
              <div class="flex justify-between items-start mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded bg-zinc-800 flex items-center justify-center text-sm font-medium text-zinc-300">
                    {{ c.name.substring(0, 1) }}
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-white group-hover:text-primary-400 transition-colors">{{ c.name }}</h4>
                    <p class="text-xs text-zinc-500 mt-0.5 max-w-[140px] truncate" :title="c.job">{{ c.job }}</p>
                  </div>
                </div>
                <button class="text-zinc-600 hover:text-zinc-300 opacity-0 group-hover:opacity-100 transition"><MoreHorizontal class="w-4 h-4"/></button>
              </div>

              <!-- AI Score badge -->
              <div v-if="c.score" class="mb-3 flex items-center gap-2">
                <div class="text-xs px-2 py-1 rounded bg-gradient-to-r from-primary-600 to-indigo-600 text-white font-medium shadow-sm flex items-center gap-1">
                  <Sparkles class="w-3 h-3 text-primary-200" />
                  AI 匹配度 {{ c.score }}
                </div>
                <span class="text-xs" :class="c.score >= 90 ? 'text-emerald-400' : (c.score >= 80 ? 'text-blue-400' : 'text-amber-400')">
                  {{ c.match }}
                </span>
              </div>
              
              <div v-else class="mb-3 text-xs px-2 py-1 rounded bg-zinc-800/80 text-zinc-400 font-medium inline-block border border-zinc-700 border-dashed">
                <span class="flex items-center gap-1"><Sparkles class="w-3 h-3 text-zinc-500" /> 正在生成分析模型...</span>
              </div>

              <div class="flex items-center justify-between text-xs text-zinc-500 pt-3 border-t border-zinc-800/80">
                <span class="flex items-center gap-1.5"><span class="w-1 h-1 rounded-full bg-zinc-600"></span>{{ c.exp }}经验</span>
                <span class="flex items-center gap-1.5"><span class="w-1 h-1 rounded-full bg-zinc-600"></span>{{ c.edu }}</span>
                <span class="font-mono">{{ c.id }}</span>
              </div>

            </div>
          </div>
        
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kanban-scroll::-webkit-scrollbar {
  width: 4px;
}
.kanban-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.kanban-scroll::-webkit-scrollbar-thumb {
  background: #27272a;
  border-radius: 4px;
}
.kanban-scroll::-webkit-scrollbar-thumb:hover {
  background: #3f3f46;
}
</style>
