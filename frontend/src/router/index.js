import { createRouter, createWebHistory } from 'vue-router'
import ResumeUpload from '../views/ResumeUpload.vue'
import ResumeReview from '../views/ResumeReview.vue'
import JobList from '../views/jobs/JobList.vue'
import NotificationCenter from '../views/NotificationCenter.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            redirect: '/upload' // For now, default to upload page
        },
        {
            path: '/upload',
            name: 'upload',
            component: ResumeUpload
        },
        {
            path: '/review',
            name: 'review',
            component: ResumeReview
        },
        {
            path: '/jobs',
            name: 'jobs',
            component: JobList
        },
        {
            path: '/notifications',
            name: 'notifications',
            component: NotificationCenter
        }
    ]
})

export default router
