<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <h2>EduAgent Register</h2>
      </template>
      <el-form :model="registerForm" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="Username" prop="username">
          <el-input v-model="registerForm.username" placeholder="Choose username" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="registerForm.email" placeholder="Enter email" />
        </el-form-item>
        <el-form-item label="Full Name" prop="full_name">
          <el-input v-model="registerForm.full_name" placeholder="Enter full name" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="Choose password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="userStore.loading" @click="handleRegister" style="width: 100%">
            Register
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-link">
        <span>Already have an account? </span>
        <router-link to="/login">Login</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()

const registerForm = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: 'Please enter username', trigger: 'blur' }],
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' },
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' },
  ],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  const success = await userStore.register(registerForm)
  if (success) {
    ElMessage.success('Registration successful - please login')
    router.push('/login')
  } else {
    ElMessage.error('Registration failed - username or email may already exist')
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  width: 400px;
}

.login-link {
  text-align: center;
  margin-top: 16px;
}
</style>
