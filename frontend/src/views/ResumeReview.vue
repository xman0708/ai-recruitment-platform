<template>
  <div class="review-page">
    <header class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="finishReview">← Back to Upload</button>
        <h1>Batch Review Parsed Resumes</h1>
      </div>
      <div class="header-actions">
        <button class="btn-secondary" @click="finishReview">Finish & Exit</button>
        <button class="btn-primary" @click="saveCandidate" :disabled="currentCandidate?.saved">
          {{ currentCandidate?.saved ? 'Saved' : 'Confirm & Save Current' }}
        </button>
      </div>
    </header>

    <div class="main-content grid">
      
      <!-- Candidate List Sidebar -->
      <aside class="sidebar-section glass-panel">
        <div class="sidebar-header">
          <h3>Candidates</h3>
          <span class="badge">{{ candidates.length }}</span>
        </div>
        <div class="candidate-list">
           <div v-for="(candidate, index) in candidates" :key="index" 
                class="candidate-item" 
                :class="{ active: activeIndex === index, saved: candidate.saved }"
                @click="activeIndex = index">
             <div class="item-icon">👤</div>
             <div class="item-details">
               <h4>{{ candidate.name || 'Unnamed Candidate' }}</h4>
               <p>{{ candidate.sourceFile || 'Unknown File' }}</p>
             </div>
             <div v-if="candidate.saved" class="status-check">✅</div>
           </div>
        </div>
      </aside>

      <!-- Original Document Preview Placeholder -->
      <section class="document-section glass-panel">
        <div class="doc-header">
          <h3>Original Document</h3>
          <span class="file-name">{{ currentCandidate?.sourceFile || 'candidate_resume.pdf' }}</span>
        </div>
        <div class="doc-viewer-placeholder">
          <div class="viewer-content">
            <span class="pdf-icon">📄</span>
            <p>PDF Viewer Component Load Here</p>
          </div>
        </div>
      </section>

      <!-- Extracted Data Form -->
      <section class="form-section glass-panel">
        <h3>Extracted Entities</h3>
        <p class="section-desc">Verify and correct the AI extraction below</p>
        
        <form @submit.prevent="saveCandidate" class="review-form" v-if="currentCandidate">
          <div class="form-group">
            <label>Full Name</label>
            <input type="text" v-model="currentCandidate.name" :disabled="currentCandidate.saved" />
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Phone Number</label>
              <input type="text" v-model="currentCandidate.phone" :disabled="currentCandidate.saved" />
            </div>
            <div class="form-group">
              <label>Email Address</label>
              <input type="email" v-model="currentCandidate.email" :disabled="currentCandidate.saved" />
            </div>
          </div>
          
          <div class="form-group">
            <label>Skills <span class="ai-badge">AI Confidence: 95%</span></label>
            <textarea v-model="currentCandidate.skills" rows="3" :disabled="currentCandidate.saved"></textarea>
          </div>

          <div class="form-group">
            <label>Education History</label>
            <textarea v-model="currentCandidate.education" rows="4" :disabled="currentCandidate.saved"></textarea>
          </div>

          <div class="form-group">
            <label>Work Experience</label>
            <textarea v-model="currentCandidate.experience" rows="6" :disabled="currentCandidate.saved"></textarea>
          </div>
        </form>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useResumeStore } from '../stores/resume';

const router = useRouter();
const resumeStore = useResumeStore();

const candidates = ref([]);
const activeIndex = ref(0);

onMounted(() => {
  // Use parsedResults array instead of parsedData
  if (resumeStore.parsedResults && resumeStore.parsedResults.length > 0) {
    // deep copy to allow local editing
    candidates.value = JSON.parse(JSON.stringify(resumeStore.parsedResults)).map(item => ({
      ...item,
      saved: false
    }));
  } else {
    // Show mock multiple candidates for layout testing
    candidates.value = [
      {
        sourceFile: 'frontend_engineer_resume.pdf',
        name: "Robin (Mock)",
        phone: "13800138000",
        email: "airobin@example.com",
        skills: "Vue 3, TypeScript, Pinia",
        education: "BS Computer Science",
        experience: "5 years of frontend engineering",
        saved: false
      },
      {
        sourceFile: 'backend_developer_cv.docx',
        name: "Chai (Mock)",
        phone: "13900139000",
        email: "chai@example.com",
        skills: "Python, FastAPI, MySQL",
        education: "MS Software Engineering",
        experience: "3 years of backend development",
        saved: false
      }
    ];
  }
});

const currentCandidate = computed(() => {
  return candidates.value[activeIndex.value] || null;
});

const saveCandidate = () => {
  if (!currentCandidate.value || currentCandidate.value.saved) return;
  // In a real flow, send `currentCandidate.value` to FastAPI
  
  // Mark as saved in UI
  currentCandidate.value.saved = true;
};

const finishReview = () => {
  resumeStore.clearData();
  router.push('/upload');
};
</script>

<style scoped>
.review-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.back-btn:hover {
  color: var(--primary);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

.page-header h1 {
  font-size: 1.8rem;
}

.grid {
  display: grid;
  grid-template-columns: 320px 1fr 1.2fr;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.sidebar-section, .document-section, .form-section {
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.badge {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.candidate-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding-right: 4px;
}

.candidate-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.candidate-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.candidate-item.active {
  background: rgba(99, 102, 241, 0.15);
  border-color: var(--primary);
}

.candidate-item.saved {
  opacity: 0.7;
}

.item-icon {
  font-size: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px;
  border-radius: 50%;
}

.item-details {
  flex: 1;
  overflow: hidden;
}

.item-details h4 {
  font-size: 1rem;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-details p {
  font-size: 0.75rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-check {
  font-size: 1.2rem;
}

.doc-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.file-name {
  color: var(--primary);
  font-weight: 500;
}

.doc-viewer-placeholder {
  flex: 1;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--surface-border);
}

.viewer-content {
  text-align: center;
  color: var(--text-secondary);
}

.pdf-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  display: block;
}

.section-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  padding-right: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-badge {
  background: rgba(16, 185, 129, 0.2);
  color: var(--success);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

input, textarea {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  padding: 12px;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: all 0.2s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary);
}

textarea {
  resize: vertical;
}

/* Custom scrollbar for form area */
.review-form::-webkit-scrollbar {
  width: 6px;
}
</style>
