<template>
  <div class="profile-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Learning Profile</span>
          <el-button type="primary" @click="showGenerateDialog = true">
            Generate Profile
          </el-button>
        </div>
      </template>

      <div v-if="profile">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Knowledge Level">
            <el-tag v-for="(level, topic) in profile.knowledge_level" :key="topic" size="small" style="margin-right: 4px">
              {{ topic }}: {{ level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Available Time">
            {{ profile.available_time_per_week }} hours/week
          </el-descriptions-item>
          <el-descriptions-item label="Learning Goals" :span="2">
            <el-tag v-for="goal in profile.learning_goals" :key="goal" size="small" style="margin-right: 4px">
              {{ goal }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Interests" :span="2">
            <el-tag v-for="interest in profile.interests" :key="interest" size="small" style="margin-right: 4px">
              {{ interest }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <el-empty v-else description="No profile found. Generate one to get started." />
    </el-card>

    <!-- Generate Profile Dialog -->
    <el-dialog v-model="showGenerateDialog" title="Generate Learning Profile" width="600px">
      <el-form :model="generateForm" label-width="120px">
        <el-form-item label="Your Goals">
          <el-input v-model="generateForm.user_input" type="textarea" :rows="6"
            placeholder="Describe your learning goals, current knowledge level, available time, and any preferences..." />
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/api/axios'
import type { LearningProfile } from '@/types'

const profile = ref<LearningProfile | null>(null)
const showGenerateDialog = ref(false)
const generating = ref(false)

const generateForm = ref({
  user_input: '',
})

onMounted(async () => {
  await fetchProfile()
})

async function fetchProfile() {
  try {
    const response = await apiClient.get('/profile/current')
    profile.value = response.data
  } catch {
    // Profile not found - normal for new users
  }
}

async function handleGenerate() {
  if (!generateForm.value.user_input.trim()) {
    ElMessage.warning('Please describe your learning goals')
    return
  }

  generating.value = true
  try {
    const response = await apiClient.post('/profile/generate', {
      user_input: generateForm.value.user_input,
    })
    profile.value = response.data.profile
    showGenerateDialog.value = false
    generateForm.value.user_input = ''
    ElMessage.success('Profile generated successfully')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || 'Failed to generate profile')
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.profile-view {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
