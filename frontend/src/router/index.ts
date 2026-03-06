import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/AppLayout.vue'),
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('@/views/Dashboard.vue'),
                meta: { title: '概览', icon: 'LayoutDashboard' }
            },
            {
                path: 'jobs',
                name: 'Jobs',
                component: () => import('@/views/jobs/JobList.vue'),
                meta: { title: 'JD 管理', icon: 'Briefcase' }
            },
            {
                path: 'upload',
                name: 'UploadResume',
                component: () => import('@/views/ResumeUpload.vue'),
                meta: { title: '简历解析', icon: 'Upload' }
            },
            {
                path: 'candidates',
                name: 'CandidatesPipeline',
                component: () => import('@/views/candidates/Pipeline.vue'),
                meta: { title: '候选人管理', icon: 'Users' }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
