<script setup lang="ts">
import { Users, Briefcase, ChartBar, CheckCircle } from 'lucide-vue-next'

const stats = [
  { name: '活跃职位', value: '12', icon: Briefcase, color: 'text-blue-400', bg: 'bg-blue-400/10' },
  { name: '待初筛简历', value: '48', icon: Users, color: 'text-indigo-400', bg: 'bg-indigo-400/10' },
  { name: '待安排面试', value: '16', icon: ChartBar, color: 'text-amber-400', bg: 'bg-amber-400/10' },
  { name: '本周发放 Offer', value: '5', icon: CheckCircle, color: 'text-emerald-400', bg: 'bg-emerald-400/10' }
]
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white">欢迎回来，王专员 👋</h1>
        <p class="text-zinc-400 mt-1">这里是今日招聘工作概览。AI 已经处理了 12 份新投递的简历。</p>
      </div>
      <el-button type="primary" class="!bg-primary-600 !border-primary-600 hover:!bg-primary-500 focus:!ring-primary-500/50">
        上传新简历
      </el-button>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in stats" :key="stat.name" 
           class="bg-surface border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-colors shadow-sm">
        <div class="flex items-center gap-4">
          <div :class="['w-12 h-12 rounded-lg flex items-center justify-center', stat.bg]">
            <component :is="stat.icon" :class="['w-6 h-6', stat.color]" />
          </div>
          <div>
            <div class="text-3xl font-bold text-white">{{ stat.value }}</div>
            <div class="text-sm font-medium text-zinc-400 mt-0.5">{{ stat.name }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Empty State / Welcome area for further UI building -->
    <div class="bg-surface border border-zinc-800 rounded-xl p-8 flex flex-col items-center justify-center min-h-[400px] text-center">
      <div class="w-16 h-16 rounded-full bg-primary-500/10 flex items-center justify-center mb-4">
        <Sparkles class="w-8 h-8 text-primary-500" />
      </div>
      <h3 class="text-xl font-medium text-white mb-2">AI 智能分析正在运行中</h3>
      <p class="text-zinc-400 max-w-md">前往「候选人池」查看 AI 自动解析并匹配的候选人列表，或者「职位管理」发布新需求开启自动筛选流程。</p>
    </div>
  </div>
</template>
