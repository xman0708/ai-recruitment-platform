<script setup lang="ts">
import { ref } from 'vue'
import { Video, MapPin, Clock, Calendar as CalendarIcon, MessageSquare, CheckCircle, Search } from 'lucide-vue-next'

const interviews = ref([
  { 
    id: 'INT-001', 
    candidate: '李晓明', 
    job: '高级前端开发工程师（Vue3）',
    type: '视频面试',
    time: '今天 14:00 - 15:00',
    interviewer: '张技术总监',
    status: 'SCHEDULED', // SCHEDULED, COMPLETED
    link: 'https://meeting.tencent.com/p/123456789'
  },
  { 
    id: 'INT-002', 
    candidate: '王梦琪', 
    job: 'Python 后端架构师',
    type: '线下面试',
    time: '明天 10:30 - 11:30',
    interviewer: '刘架构师',
    status: 'SCHEDULED',
    link: '总部大楼 A 座 302 会议室'
  },
  { 
    id: 'INT-003', 
    candidate: '陈思宇', 
    job: '高级前端开发工程师（Vue3）',
    type: '视频面试',
    time: '昨天 16:00 - 17:00',
    interviewer: '王前端组长',
    status: 'COMPLETED',
    link: '-'
  }
])

const showFeedbackDialog = ref(false)
const feedbackForm = ref({
  score: 0,
  content: '',
  recommendation: 'HIRE' // HIRE, HOLD, REJECT
})
const activeInterviewId = ref('')

const openFeedback = (id: string) => {
  activeInterviewId.value = id
  showFeedbackDialog.value = true
}

const submitFeedback = () => {
  const intw = interviews.value.find(i => i.id === activeInterviewId.value)
  if (intw) intw.status = 'COMPLETED'
  showFeedbackDialog.value = false
  feedbackForm.value = { score: 0, content: '', recommendation: 'HIRE' }
}
</script>

<template>
  <div class="h-full flex flex-col space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white mb-1">面试行程</h1>
        <p class="text-zinc-400 text-sm">管理即将到来的面试，快速填写面评记录。</p>
      </div>
      <div class="relative w-64">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 w-4 h-4" />
        <input 
          type="text" 
          placeholder="搜索候选人或职位..." 
          class="w-full bg-surface border border-zinc-800 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 placeholder-zinc-500 shadow-sm"
        >
      </div>
    </div>

    <!-- Interview List -->
    <div class="flex-1 space-y-4 overflow-y-auto pr-2 pb-4 kanban-scroll">
      <div v-for="item in interviews" :key="item.id" 
           class="bg-surface border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-colors shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 group">
        
        <div class="flex items-start gap-4 flex-1">
          <div :class="[
            'w-12 h-12 rounded-full flex items-center justify-center border-4 shrink-0',
            item.status === 'COMPLETED' ? 'bg-zinc-800 text-zinc-400 border-background' : 'bg-primary-500/20 text-primary-400 border-primary-500/10'
          ]">
            <CalendarIcon class="w-5 h-5" />
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h3 class="text-lg font-bold text-white group-hover:text-primary-400 transition-colors">{{ item.candidate }}</h3>
              <span class="text-xs font-medium px-2 py-0.5 rounded-full"
                    :class="item.status === 'COMPLETED' ? 'bg-zinc-800 text-zinc-400' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'">
                {{ item.status === 'COMPLETED' ? '已完成' : '待面试' }}
              </span>
            </div>
            <p class="text-sm text-zinc-400 font-medium">{{ item.job }}</p>
            
            <div class="mt-4 flex flex-wrap items-center gap-4 text-xs text-zinc-500">
              <span class="flex items-center gap-1.5 bg-zinc-800/50 px-2 py-1 rounded">
                <Clock class="w-3.5 h-3.5" /> {{ item.time }}
              </span>
              <span class="flex items-center gap-1.5">
                <component :is="item.type === '视频面试' ? Video : MapPin" class="w-3.5 h-3.5" />
                {{ item.link }}
              </span>
              <span class="flex items-center gap-1.5">
                <Users class="w-3.5 h-3.5" /> 面试官：{{ item.interviewer }}
              </span>
            </div>
          </div>
        </div>

        <div class="shrink-0 flex items-center gap-3 self-end md:self-center">
          <el-button v-if="item.status === 'SCHEDULED' && item.type === '视频面试'" 
                     type="primary" class="!bg-primary-600 hover:!bg-primary-500 !border-none">
            进入会议
          </el-button>
          
          <el-button v-if="item.status === 'SCHEDULED'" 
                     @click="openFeedback(item.id)"
                     class="!bg-surface !border-zinc-700 !text-white hover:!bg-zinc-800">
            <template #icon><el-icon><MessageSquare /></el-icon></template>填写面评
          </el-button>
          
          <div v-if="item.status === 'COMPLETED'" class="flex items-center gap-2 text-sm font-medium text-emerald-500">
            <CheckCircle class="w-4 h-4" /> 面评已归档
          </div>
        </div>
      </div>
    </div>

    <!-- Feedback Dialog -->
    <el-dialog 
      v-model="showFeedbackDialog" 
      title="填写面试评价" 
      width="500px"
      class="!bg-surface custom-dialog"
    >
      <div class="space-y-6 pt-2">
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-3">综合打分</label>
          <el-rate v-model="feedbackForm.score" allow-half class="!flex" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">录用建议</label>
          <div class="flex gap-3">
            <button @click="feedbackForm.recommendation = 'HIRE'" 
                    class="flex-1 py-2 rounded-lg border text-sm font-medium transition-colors"
                    :class="feedbackForm.recommendation === 'HIRE' ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.1)]' : 'bg-background border-zinc-700 text-zinc-400'">
              推荐录用 (Hire)
            </button>
            <button @click="feedbackForm.recommendation = 'HOLD'" 
                    class="flex-1 py-2 rounded-lg border text-sm font-medium transition-colors"
                    :class="feedbackForm.recommendation === 'HOLD' ? 'bg-amber-500/10 border-amber-500 text-amber-400 shadow-[0_0_10px_rgba(245,158,11,0.1)]' : 'bg-background border-zinc-700 text-zinc-400'">
              待定 (Hold)
            </button>
            <button @click="feedbackForm.recommendation = 'REJECT'" 
                    class="flex-1 py-2 rounded-lg border text-sm font-medium transition-colors"
                    :class="feedbackForm.recommendation === 'REJECT' ? 'bg-red-500/10 border-red-500 text-red-400 shadow-[0_0_10px_rgba(239,68,68,0.1)]' : 'bg-background border-zinc-700 text-zinc-400'">
              淘汰 (Reject)
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">详细评语</label>
          <textarea v-model="feedbackForm.content" rows="4" 
                    class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary-500 resize-none text-sm placeholder-zinc-600" 
                    placeholder="记录候选人在技术广度、深度及沟通能力的具体表现..."></textarea>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showFeedbackDialog = false" class="!bg-background !border-zinc-700 !text-zinc-300 hover:!bg-zinc-800 hover:!text-white">取消</el-button>
          <el-button type="primary" @click="submitFeedback" class="!bg-primary-600 hover:!bg-primary-500 !border-none">确认提交评价</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style>
/* Scoped Dialog Overrides */
.custom-dialog .el-dialog__title {
  color: white !important;
  font-weight: 600;
}
.custom-dialog .el-dialog__header {
  border-bottom: 1px solid #27272a;
  margin-right: 0;
  padding-bottom: 20px;
}
</style>
