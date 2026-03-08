<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { UploadCloud, MoreHorizontal, Sparkles, Filter, CalendarPlus } from 'lucide-vue-next'
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

const showScheduleDialog = ref(false)
const scheduleForm = ref({
  candidate_id: 0,
  candidate_name: '',
  interviewer_id: 1, // Defaulting to HR mock user 1
  type: '视频面试',
  scheduled_time: '',
  location_or_link: ''
})
const isScheduling = ref(false)

const openScheduleInterview = (c: any, event: Event) => {
  event.stopPropagation() // Prevent triggering viewCandidate
  scheduleForm.value = {
    candidate_id: c.id,
    candidate_name: c.name,
    interviewer_id: 1,
    type: '视频面试',
    scheduled_time: '',
    location_or_link: ''
  }
  showScheduleDialog.value = true
}

const submitSchedule = async () => {
  if (!scheduleForm.value.scheduled_time) {
    ElMessage.warning('请填写面试时间')
    return
  }
  isScheduling.value = true
  try {
    await request.post('/interviews/', {
      ...scheduleForm.value
    })
    ElMessage.success('面试安排成功')
    showScheduleDialog.value = false
    fetchCandidates() // Refresh pipeline
  } catch (e) {
    ElMessage.error('安排面试失败')
    console.error(e)
  } finally {
    isScheduling.value = false
  }
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

              <div v-if="c.ai_score" class="mb-3 flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <div class="text-xs px-2 py-1 rounded bg-gradient-to-r from-primary-600 to-indigo-600 text-white font-medium shadow-sm flex items-center gap-1">
                    <Sparkles class="w-3 h-3 text-primary-200" />
                    AI 匹配度 {{ c.ai_score }}
                  </div>
                  <span class="text-xs" :class="c.ai_score >= 90 ? 'text-emerald-400' : (c.ai_score >= 80 ? 'text-blue-400' : 'text-amber-400')">
                    {{ c.ai_reasoning || '匹配' }}
                  </span>
                </div>
                <div v-if="c.status === 'screening'" class="mt-1">
                  <el-button size="small" type="primary" class="w-full !bg-primary-600/20 hover:!bg-primary-600/30 !border-primary-500/30 !text-primary-400 font-medium" @click="openScheduleInterview(c, $event)">
                    <template #icon><el-icon><CalendarPlus /></el-icon></template>
                    安排面试
                  </el-button>
                </div>
              </div>
              
              <div v-else class="mb-3 text-xs px-2 py-1 rounded bg-zinc-800/80 text-zinc-400 font-medium inline-block border border-zinc-700 border-dashed">
                <span class="flex items-center gap-1"><Sparkles class="w-3 h-3 text-zinc-500" /> 正在生成分析模型...</span>
              </div>

              <div class="flex items-center justify-between text-xs text-zinc-500 pt-3 border-t border-zinc-800/80">
                <span class="flex items-center gap-1.5"><span class="w-1 h-1 rounded-full bg-zinc-600"></span>{{ c.experience }}</span>
                <span class="flex items-center gap-1.5"><span class="w-1 h-1 rounded-full bg-zinc-600"></span>{{ c.education }}</span>
                <span class="font-mono">{{ c.id }}</span>
              </div>

            </div>
          </div>
        
        </div>
      </div>
    </div>

    <!-- Schedule Dialog -->
    <el-dialog 
      v-model="showScheduleDialog" 
      :title="`为 ${scheduleForm.candidate_name} 安排面试`" 
      width="500px"
      class="!bg-surface custom-dialog"
    >
      <div class="space-y-5 pt-2">
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">面试方式</label>
          <div class="flex gap-4">
            <el-radio-group v-model="scheduleForm.type">
              <el-radio label="视频面试" class="!text-zinc-300">视频会议</el-radio>
              <el-radio label="线下面试" class="!text-zinc-300">现场面试</el-radio>
            </el-radio-group>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">面试时间安排</label>
          <input type="text" v-model="scheduleForm.scheduled_time" 
                 class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-primary-500 text-sm placeholder-zinc-600" 
                 placeholder="例如: 明天 14:00 - 15:00">
        </div>

        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">
            {{ scheduleForm.type === '视频面试' ? '会议链接' : '面试地点' }}
          </label>
          <input type="text" v-model="scheduleForm.location_or_link" 
                 class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-primary-500 text-sm placeholder-zinc-600" 
                 :placeholder="scheduleForm.type === '视频面试' ? 'https://meeting.tencent.com/...' : '如: 总部大楼 A 座 302 会议室'">
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showScheduleDialog = false" class="!bg-background !border-zinc-700 !text-zinc-300 hover:!bg-zinc-800 hover:!text-white">取消</el-button>
          <el-button type="primary" :loading="isScheduling" @click="submitSchedule" class="!bg-primary-600 hover:!bg-primary-500 !border-none">确认安排</el-button>
        </span>
      </template>
    </el-dialog>
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
