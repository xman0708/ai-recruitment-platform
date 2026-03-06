<template>
  <div class="upload-page">
    <header class="page-header">
      <h1>Resume Processing Center</h1>
      <p class="subtitle">Upload candidate resumes for automated AI parsing and matching</p>
    </header>

    <div class="split-view">
      <!-- Upload Section -->
      <section class="upload-section glass-panel">
        <div class="upload-card">
          <div class="dropzone" 
               @dragover.prevent="isDragging = true" 
               @dragleave.prevent="isDragging = false" 
               @drop.prevent="handleDrop"
               :class="{ 'is-dragging': isDragging }">
            
            <div class="upload-icon">
              <span class="cloud-icon" :class="{ 'bounce': isDragging }">☁️</span>
            </div>
            
            <h3>Drag & Drop Resumes Here</h3>
            <p>Support PDF, Word (.doc, .docx), and TXT formats</p>
            
            <div class="divider"><span>OR</span></div>
            
            <label class="btn-primary browse-btn">
              Browse Files
              <input type="file" multiple accept=".pdf,.doc,.docx,.txt" class="hidden-input" @change="handleFileSelect" />
            </label>
          </div>
        </div>
      </section>

      <!-- Processing Queue Section -->
      <section class="queue-section glass-panel">
        <div class="queue-header">
          <h3>Processing Queue</h3>
          <span class="badge">{{ files.length }} Files</span>
        </div>
        
        <div class="queue-list" v-if="files.length > 0">
          <transition-group name="list">
            <div v-for="(file, index) in files" :key="index" class="queue-item">
              <div class="file-info">
                <span class="file-icon">📄</span>
                <div class="file-details">
                  <p class="file-name">{{ file.name }}</p>
                  <p class="file-size">{{ formatSize(file.size) }}</p>
                </div>
              </div>
              <div class="status-indicator">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: file.progress + '%' }" :class="{ 'completed': file.progress === 100 }"></div>
                </div>
                <span class="status-text">{{ file.status }}</span>
              </div>
            </div>
          </transition-group>
        </div>
        
        <div class="empty-state" v-else>
          <div class="empty-icon">📂</div>
          <p>No files in queue.<br/>Upload resumes to start parsing.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useResumeStore } from '../stores/resume';

const router = useRouter();
const resumeStore = useResumeStore();

const isDragging = ref(false);
const files = ref([]);

const processFiles = async (newFiles) => {
  if (!newFiles || newFiles.length === 0) return;

  // Transform standard files into tracking objects
  const newFileObjs = Array.from(newFiles).map((file) => ({
    rawFile: file,
    name: file.name,
    size: file.size,
    progress: 0,
    status: 'Waiting...'
  }));
  
  // Append to existing file view
  files.value.push(...newFileObjs);
  
  // Execute upload and AI processing for all concurrently
  const uploadPromises = newFileObjs.map(async (fileObj) => {
    fileObj.status = 'Uploading & Parsing via AI...';
    
    const progressInterval = setInterval(() => {
      if (fileObj.progress < 90) {
        fileObj.progress += Math.floor(Math.random() * 10) + 5;
      }
    }, 400);

    const success = await resumeStore.uploadAndParse(fileObj.rawFile);
    
    clearInterval(progressInterval);
    
    if (success) {
      fileObj.progress = 100;
      fileObj.status = 'Parsed successfully';
    } else {
      fileObj.progress = 0;
      fileObj.status = 'Error: ' + (resumeStore.error || 'Parsing failed');
    }
  });

  // Wait for all to finish
  await Promise.all(uploadPromises);

  // If at least one resume parsed successfully, redirect to review after a short delay
  if (resumeStore.parsedResults.length > 0) {
    setTimeout(() => {
        router.push('/review');
    }, 1200);
  }
};

const handleDrop = (e) => {
  isDragging.value = false;
  if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    processFiles(e.dataTransfer.files);
  }
};

const handleFileSelect = (e) => {
  if (e.target.files && e.target.files.length > 0) {
    processFiles(e.target.files);
  }
};

const formatSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  gap: 32px;
  height: 100%;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.split-view {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0; 
}

.upload-section {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  padding: 32px;
}

.queue-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 32px;
}

.dropzone {
  flex: 1;
  border: 2px dashed rgba(99, 102, 241, 0.4);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 16px;
  transition: all 0.3s ease;
  background: rgba(15, 23, 42, 0.4);
  min-height: 400px;
}

.dropzone.is-dragging {
  border-color: var(--primary);
  background: rgba(99, 102, 241, 0.1);
  transform: scale(1.02);
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
}

.bounce {
  display: inline-block;
  animation: bounce 1s infinite alternate;
}

@keyframes bounce {
  from { transform: translateY(0); }
  to { transform: translateY(-15px); }
}

.dropzone h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
}

.dropzone p {
  color: var(--text-secondary);
}

.divider {
  display: flex;
  align-items: center;
  width: 60%;
  margin: 20px 0;
  color: var(--text-secondary);
}

.divider::before, .divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid var(--surface-border);
}

.divider span {
  padding: 0 10px;
  font-size: 0.85rem;
}

.hidden-input {
  display: none;
}

.browse-btn {
  display: inline-block;
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.badge {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  text-align: center;
  gap: 16px;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  padding-right: 8px;
}

.queue-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.3s ease;
}

.queue-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-icon {
  font-size: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px;
  border-radius: 8px;
}

.file-details {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 4px;
  word-break: break-all;
}

.file-size {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-fill.completed {
  background: var(--success);
}

.status-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
