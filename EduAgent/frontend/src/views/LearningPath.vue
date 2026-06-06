<template>
  <div class="learning-path-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Learning Paths</span>
          <el-button type="primary" @click="showGenerateDialog = true">
            Generate New Path
          </el-button>
        </div>
      </template>

      <div v-if="paths.length > 0">
        <el-timeline>
          <el-timeline-item v-for="path in paths" :key="path.id" :color="getStatusColor(path.status)">
            <el-card>
              <h3>{{ path.title }}</h3>
              <p>{{ path.description }}</p>
              <div class="path-meta">
                <el-tag :type="path.status === 'active' ? 'success' : 'info'">{{ path.status }}</el-tag>
                <span class="progress">Progress: {{ path.progress }}%</span>
              </div>
              <el-progress :percentage="path.progress" style="margin-top: 8px" />
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>

      <el-empty v-else description="No learning paths found. Generate one to get started." />
    </el-card>

    <!-- Generate Path Dialog -->
    <el-dialog v-model="showGenerateDialog" title="Generate Learning Path" width="600px">
      <el-form :model="generateForm" label-width="140px">
        <el-form-item label="Target Skill">
          <el-input v-model="generateForm.target_skill" placeholder="e.g., Python Programming" />
        </el-form-item>
        <el-form-item label="Current Knowledge">
          <el-input v-model="knowledgeInput" type="textarea" placeholder='{"python": "beginner", "algorithms": "none"}' />
        </el-form-item>
        <el-form-item label="Hours per Week">
          <el-input-number v-model="generateForm.time_available" :min="1" :max="40" />
        </el-form-item>
        <el-form-item label="Learning Goals">
          <el-input v-model="goalsInput" type="textarea" placeholder="Goal 1&#10;Goal 2&#10;Goal 3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGenerateDialog = false">Cancel</el-button>
        <el-button type="primary" :loading="generating" @click="handleGenerate">Generate</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/api/axios'
import type { LearningPath } from '@/types'

const paths = ref<LearningPath[]>([])
const showGenerateDialog = ref(false)
const generating = ref(false)

const generateForm = ref({
  target_skill: '',
  current_knowledge: {} as Record<string, string>,
  time_available: 10,
  goals: [] as string[],
})

const knowledgeInput = ref('')
const goalsInput = ref('')

onMounted(async () => {
  await fetchPaths()
})

async function fetchPaths() {
  try {
    const response = await apiClient.get('/path/')
    paths.value = response.data
  } catch {
    // Handle error silently
  }
}

function getStatusColor(status: string) {
  switch (status) {
    case 'active': return '#67c23a'
    case 'completed': return '#409eff'
    case 'paused': return '#e6a23c'
    default: return '#909399'
  }
}

async function handleGenerate() {
  if (!generateForm.value.target_skill.trim()) {
    ElMessage.warning('Please enter target skill')
    return
  }

  generating.value = true
  try {
    // Parse inputs
    generateForm.value.current_knowledge = JSON.parse(knowledgeInput.value || '{}')
    generateForm.value.goals = goalsInput.value.split('\n').filter(g => g.trim())

    const response = await apiClient.post('/path/generate', generateForm.value)
    paths.value.unshift(response.data.learning_path)
    showGenerateDialog.value = false
    ElMessage.success('Learning path generated successfully')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || 'Failed to generate learning path')
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.learning-path-view {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.path-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.progress {
  font-size: 14px;
  color: #666;
}
</style>
