<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Sparkles, ArrowLeft, Download, Mail, Calendar, MapPin, CheckCircle, XCircle, AlertTriangle } from 'lucide-vue-next'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const chartRef = ref<HTMLElement | null>(null)

// Mock Data
const candidate = ref({
  id: route.params.id,
  name: '李晓明',
  jobActive: '高级前端开发工程师（Vue3）',
  status: 'AI_SCREENED',
  avatar: 'L',
  info: { exp: '5年', edu: '本科', age: 28, city: '北京' },
  aiScore: 92,
  aiSummary: '该候选人拥有扎实的 Vue3 和前端工程化经验，在性能调优和组件库搭建上也有实际产出，能够很好地胜任当前 JD。但其在 Node.js 和服务端架构方面略显薄弱。综合评定：强烈推荐进入面试。',
  strengths: ['丰富的 Vue3 实战经验', '良好的组件设计能力', '沟通逻辑清晰'],
  weaknesses: ['缺乏大型高并发服务端经验', '对最新的 AI WebGL 技术接触较少'],
})

onMounted(() => {
  nextTick(() => {
    if (chartRef.value) {
      const myChart = echarts.init(chartRef.value)
      myChart.setOption({
        radar: {
          indicator: [
            { name: 'Vue/React 熟练度', max: 100 },
            { name: '工程化/架构', max: 100 },
            { name: '算法/基础', max: 100 },
            { name: '业务逻辑解构', max: 100 },
            { name: '沟通与驱动力', max: 100 }
          ],
          splitArea: { areaStyle: { color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.02)'] } },
          axisName: { color: '#a1a1aa', fontSize: 12 },
          splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
          axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } }
        },
        series: [{
          name: 'AI 技能匹配雷达',
          type: 'radar',
          data: [{
            value: [95, 85, 75, 90, 88],
            name: '李晓明',
            itemStyle: { color: '#3b82f6' },
            areaStyle: { color: 'rgba(59, 130, 246, 0.4)' },
            lineStyle: { width: 2 }
          }]
        }]
      })
      window.addEventListener('resize', () => myChart.resize())
    }
  })
})
</script>

<template>
  <div class="h-full flex flex-col pt-2">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6 pb-6 border-b border-zinc-800">
      <div class="flex items-center gap-4">
        <button @click="router.back()" class="w-10 h-10 rounded-full bg-surface border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors">
          <ArrowLeft class="w-5 h-5" />
        </button>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
            {{ candidate.name }}
            <span class="text-xs font-medium px-2 py-1 rounded bg-zinc-800 text-zinc-300 border border-zinc-700 font-mono">
              {{ candidate.id }}
            </span>
          </h1>
          <p class="text-zinc-400 mt-1 flex items-center gap-2 text-sm">
            应聘：<span class="text-zinc-200">{{ candidate.jobActive }}</span>
          </p>
        </div>
      </div>
      <div class="flex gap-3">
        <el-button class="!bg-surface focus:!bg-surface !border-zinc-700 !text-white hover:!bg-zinc-800">
          <template #icon><el-icon><Download /></el-icon></template>原始简历
        </el-button>
        <el-button type="primary" class="!bg-primary-600 hover:!bg-primary-500 !border-none shadow-lg shadow-primary-500/20">
          <template #icon><el-icon><Calendar /></el-icon></template>安排面试
        </el-button>
      </div>
    </div>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column: AI Evaluation -->
      <div class="lg:col-span-2 space-y-6">
        
        <!-- Score Banner -->
        <div class="relative overflow-hidden bg-gradient-to-r from-primary-900/40 to-indigo-900/40 border border-primary-500/20 rounded-2xl p-6">
          <div class="absolute top-0 right-0 p-8 opacity-10">
            <Sparkles class="w-32 h-32 text-primary-400" />
          </div>
          <div class="relative z-10 flex items-start gap-6">
            <div class="flex flex-col items-center justify-center p-4 bg-background/50 rounded-xl border border-primary-500/30 backdrop-blur-sm min-w-[120px]">
              <span class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-br from-white to-primary-200">
                {{ candidate.aiScore }}
              </span>
              <span class="text-xs font-medium text-emerald-400 mt-1 uppercase tracking-widest hidden sm:block">极度匹配</span>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
                <Sparkles class="w-5 h-5 text-primary-400" /> 分阶段 AI 解析结论
              </h3>
              <p class="text-zinc-300 leading-relaxed text-sm">
                {{ candidate.aiSummary }}
              </p>
            </div>
          </div>
        </div>

        <!-- Details Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-surface rounded-xl border border-zinc-800 p-6">
            <h4 class="text-sm font-medium text-zinc-400 mb-4 flex items-center gap-2 uppercase tracking-wide">
              <CheckCircle class="w-4 h-4 text-emerald-500"/> 亮点优势
            </h4>
            <ul class="space-y-3">
              <li v-for="(str, i) in candidate.strengths" :key="i" class="flex items-start gap-2 text-sm text-zinc-300">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0"></span> {{ str }}
              </li>
            </ul>
          </div>
          <div class="bg-surface rounded-xl border border-zinc-800 p-6">
            <h4 class="text-sm font-medium text-zinc-400 mb-4 flex items-center gap-2 uppercase tracking-wide">
              <AlertTriangle class="w-4 h-4 text-amber-500"/> 潜在风险
            </h4>
            <ul class="space-y-3">
              <li v-for="(wk, i) in candidate.weaknesses" :key="i" class="flex items-start gap-2 text-sm text-zinc-300">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0"></span> {{ wk }}
              </li>
            </ul>
          </div>
        </div>

      </div>

      <!-- Right Column: Profile & Radar -->
      <div class="space-y-6">
        
        <!-- Basic Info -->
        <div class="bg-surface rounded-xl border border-zinc-800 p-6 flex flex-col items-center text-center">
          <div class="w-20 h-20 rounded-full bg-gradient-to-br from-zinc-700 to-zinc-900 border-4 border-background flex items-center justify-center text-2xl font-bold text-white shadow-xl mb-4">
            {{ candidate.avatar }}
          </div>
          <h2 class="text-lg font-bold text-white">{{ candidate.name }}</h2>
          <div class="flex items-center justify-center gap-4 mt-4 text-sm text-zinc-400 w-full divide-x divide-zinc-800">
            <span class="px-3"><MapPin class="w-4 h-4 inline mr-1"/>{{ candidate.info.city }}</span>
            <span class="px-3">{{ candidate.info.exp }}经验</span>
            <span class="px-3">{{ candidate.info.edu }}</span>
          </div>
          <div class="w-full mt-6 pt-6 border-t border-zinc-800 flex flex-col gap-3">
            <button class="flex items-center justify-center gap-2 w-full py-2 bg-zinc-800/50 hover:bg-zinc-800 text-zinc-300 rounded-lg text-sm transition-colors">
              <Mail class="w-4 h-4" /> 发送邮件联络
            </button>
          </div>
        </div>

        <!-- Radar Chart -->
        <div class="bg-surface rounded-xl border border-zinc-800 p-6">
          <h4 class="text-sm font-medium text-zinc-400 mb-2 uppercase tracking-wide">能力模型对比雷达</h4>
          <div ref="chartRef" class="w-full h-64"></div>
        </div>

      </div>

    </div>
  </div>
</template>
