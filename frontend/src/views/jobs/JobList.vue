<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search, Plus, MoreHorizontal, Clock, Users } from 'lucide-vue-next'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

interface Job {
  id: number
  title: string
  department: string
  status: 'open' | 'closed' | 'draft'
  candidates_count: number
  new_candidates_count: number
  created_at: string
}

const searchQuery = ref('')
const activeTab = ref('open')
const isLoading = ref(false)
const jobs = ref<Job[]>([])

const isCreateDialogVisible = ref(false)
const isSubmitting = ref(false)
const newJobForm = ref({
  title: '',
  department: '',
  requirements: '',
  description: ''
})

const fetchJobs = async () => {
    isLoading.value = true
    try {
        const data = await request.get('/jobs')
        jobs.value = data as unknown as Job[]
    } catch (e) {
        ElMessage.error('Failed to load jobs')
        console.error(e)
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchJobs()
})

const handleCreate = async () => {
  if (!newJobForm.value.title || !newJobForm.value.description) {
      ElMessage.warning('Title and Description are required')
      return
  }

  isSubmitting.value = true
  try {
      await request.post('/jobs', {
          title: newJobForm.value.title,
          department: newJobForm.value.department || '',
          description: newJobForm.value.description,
          requirements: newJobForm.value.requirements || '',
          status: 'open'
      })
      ElMessage.success('Job created successfully')
      isCreateDialogVisible.value = false
      newJobForm.value = { title: '', department: '', requirements: '', description: '' }
      fetchJobs() // refresh the list
  } catch (e) {
      ElMessage.error('Failed to create job')
      console.error(e)
  } finally {
      isSubmitting.value = false
  }
}

const formatDate = (isoString: string) => {
    if (!isoString) return ''
    return new Date(isoString).toISOString().split('T')[0]
}
</script>

<template>
  <div class="h-full flex flex-col space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white mb-1">职位管理</h1>
        <p class="text-zinc-400 text-sm">发布并管理所有的招聘需求，系统将基于 JD 自动评判候选人。</p>
      </div>
      <el-button color="#3b82f6" @click="isCreateDialogVisible = true" size="large" class="!font-medium transition hover:scale-105 active:scale-95 duration-200">
        <template #icon><el-icon><Plus /></el-icon></template>
        发布新职位
      </el-button>
    </div>

    <!-- Filters -->
    <div class="bg-surface rounded-xl border border-zinc-800 p-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
      <div class="flex space-x-1 p-1 bg-background rounded-lg whitespace-nowrap overflow-x-auto">
        <button 
          v-for="tab in [{id: 'active', label: '招聘中 (3)'}, {id: 'closed', label: '已关闭 (1)'}]" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-5 py-2 text-sm font-medium rounded-md transition-colors"
          :class="activeTab === tab.id ? 'bg-surface text-white shadow shadow-black/20' : 'text-zinc-400 hover:text-zinc-200'"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="relative w-full sm:w-80">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 w-4 h-4" />
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="搜索职位名称、编号或部门..." 
          class="w-full bg-background border border-zinc-800 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition shadow-inner"
        >
      </div>
    </div>

    <!-- Grid List -->
    <div class="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="job in jobs" :key="job.id" 
           class="group bg-surface rounded-xl border border-zinc-800 p-6 hover:border-primary-500/50 hover:shadow-[0_0_15px_rgba(59,130,246,0.1)] transition-all duration-300 relative cursor-pointer overflow-hidden flex flex-col justify-between">
        
        <!-- Hover Gradient -->
        <div class="absolute inset-0 bg-gradient-to-br from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        
        <div class="relative z-10 flex items-start justify-between mb-4">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xs font-medium px-2 py-0.5 rounded-full" 
                    :class="job.status === 'open' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-zinc-800 text-zinc-400 border border-zinc-700'">
                {{ job.status === 'open' ? '招聘中' : '已关闭' }}
              </span>
              <span class="text-xs text-zinc-500 font-mono">{{ job.id }}</span>
            </div>
            <h3 class="text-lg font-bold text-white leading-tight group-hover:text-primary-400 transition-colors">{{ job.title }}</h3>
            <p class="text-sm text-zinc-400 mt-1">{{ job.department }}</p>
          </div>
          
          <el-dropdown trigger="click">
            <button class="text-zinc-500 hover:text-white transition p-1 rounded hover:bg-zinc-800">
              <MoreHorizontal class="w-5 h-5" />
            </button>
            <template #dropdown>
              <el-dropdown-menu class="!bg-surface !border-zinc-800">
                <el-dropdown-item class="!text-zinc-200 hover:!bg-zinc-800 hover:!text-white">编辑JD</el-dropdown-item>
                <el-dropdown-item class="!text-zinc-200 hover:!bg-zinc-800 hover:!text-white">查看候选人</el-dropdown-item>
                <el-dropdown-item divided class="!text-red-400 hover:!bg-red-500/10 hover:!text-red-300">{{ job.status === 'open' ? '关闭职位' : '重新开启' }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>

        <div class="relative z-10 grid grid-cols-2 gap-4 mt-6 pt-5 border-t border-zinc-800/80">
          <div>
            <div class="text-xs font-medium text-zinc-500 mb-1 flex items-center gap-1.5"><Users class="w-3.5 h-3.5"/> 候选人数</div>
            <div class="text-2xl font-semibold text-white">
              {{ job.candidates_count }}
              <span v-if="job.new_candidates_count > 0" class="text-sm font-medium text-emerald-400 ml-1">+{{ job.new_candidates_count }}</span>
            </div>
          </div>
          <div>
            <div class="text-xs font-medium text-zinc-500 mb-1 flex items-center gap-1.5"><Clock class="w-3.5 h-3.5"/> 发布日期</div>
            <div class="text-base font-medium text-zinc-200 py-1">{{ formatDate(job.created_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create JD Drawer -->
    <el-drawer
      v-model="isCreateDialogVisible"
      title="发布新职位"
      size="600px"
      :show-close="true"
      class="!bg-surface !text-white !border-l !border-zinc-800 custom-drawer"
    >
      <template #header>
        <div class="font-bold text-xl text-white">发布新招聘描述 (JD)</div>
      </template>
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">职位名称</label>
          <input v-model="newJobForm.title" type="text" class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500" placeholder="例如：高级前端开发工程师">
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">所属部门</label>
          <input v-model="newJobForm.department" type="text" class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-500" placeholder="例如：研发中心">
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">工作职责</label>
          <textarea v-model="newJobForm.description" rows="4" class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-500 resize-none" placeholder="描述该岗位的日常工作..."></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">任职要求 (AI 将据此进行对比)</label>
          <textarea v-model="newJobForm.requirements" rows="4" class="w-full bg-background border border-zinc-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-500 resize-none" placeholder="明确所需掌握的技能、经验年限等关键指标..."></textarea>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end space-x-3 pt-6 border-t border-zinc-800">
          <el-button @click="isCreateDialogVisible = false" class="!bg-background !border-zinc-700 !text-zinc-300 hover:!bg-zinc-800 hover:!text-white">取消</el-button>
          <el-button type="primary" @click="handleCreate" :loading="isSubmitting" class="!bg-primary-600 hover:!bg-primary-500 !border-none">
            {{ isSubmitting ? '发布中...' : '发布JD并开启AI筛查' }}
          </el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<style>
/* Drawer Customization */
.custom-drawer .el-drawer__header {
  margin-bottom: 0;
  padding: 24px;
  border-bottom: 1px solid #27272a;
}
</style>
