<template>
  <div class="dashboard-layout">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>EduAgent</h1>
          <div class="user-info">
            <span>{{ userStore.userInfo?.username }}</span>
            <el-button @click="handleLogout" size="small">Logout</el-button>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu :default-active="$route.path" router>
            <el-menu-item index="/dashboard">
              <el-icon><House /></el-icon>
              <span>Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/profile">
              <el-icon><User /></el-icon>
              <span>My Profile</span>
            </el-menu-item>
            <el-menu-item index="/learning-path">
              <el-icon><RoadMap /></el-icon>
              <span>Learning Path</span>
            </el-menu-item>
            <el-menu-item index="/resources">
              <el-icon><Document /></el-icon>
              <span>Resources</span>
            </el-menu-item>
            <el-menu-item index="/tutor">
              <el-icon><ChatDotRound /></el-icon>
              <span>Tutor</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { House, User, RoadMap, Document, ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
  if (userStore.isLoggedIn && !userStore.userInfo) {
    userStore.fetchUserInfo()
  }
})

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-layout {
  height: 100vh;
}

.header {
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  font-size: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar {
  background: #f5f5f5;
}
</style>
