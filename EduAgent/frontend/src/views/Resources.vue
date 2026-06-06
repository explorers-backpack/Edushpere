<template>
  <div class="resources-view">
    <el-card>
      <template #header>
        <span>Learning Resources</span>
      </template>

      <el-space wrap>
        <el-card v-for="resource in resources" :key="resource.id" class="resource-card" style="width: 300px">
          <template #header>
            <div class="resource-header">
              <span>{{ resource.title }}</span>
              <el-tag size="small" :type="getResourceTypeColor(resource.resource_type)">
                {{ resource.resource_type }}
              </el-tag>
            </div>
          </template>
          <p class="resource-desc">{{ resource.description || 'No description' }}</p>
          <div class="resource-meta">
            <el-tag size="small">{{ resource.difficulty_level || 'N/A' }}</el-tag>
            <span v-if="resource.estimated_minutes">{{ resource.estimated_minutes }} min</span>
          </div>
        </el-card>
      </el-space>

      <el-empty v-if="resources.length === 0" description="No resources found." />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'
import type { Resource } from '@/types'

const resources = ref<Resource[]>([])

onMounted(async () => {
  await fetchResources()
})

async function fetchResources() {
  try {
    const response = await apiClient.get('/resource/list')
    resources.value = response.data
  } catch {
    // Handle silently
  }
}

function getResourceTypeColor(type: string) {
  switch (type) {
    case 'video': return 'danger'
    case 'article': return 'primary'
    case 'exercise': return 'success'
    case 'quiz': return 'warning'
    case 'project': return 'info'
    default: return ''
  }
}
</script>

<style scoped>
.resources-view {
  padding: 20px;
}

.resource-card {
  margin-bottom: 16px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.resource-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #999;
}
</style>
