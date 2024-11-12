<template>
  <ThemeProvider
      :color="themeColors[userRole]"
  >
    <div class="login-box rounded-sm">
      <div v-if="!roleSelected" class="head">
      <h2 class="text-2xl-me font-bold mb-4">
      登陆前，请选择您的身份
      </h2>
      </div>
      <div v-if="!roleSelected" class="role-selection text-center">
        <div class="flex flex-col space-y-4">
          <a-button type="primary" class="role-button" @click="selectRole('admin')">我是管理员</a-button>
          <a-button type="primary" class="role-button" @click="selectRole('doctor')">我是医生</a-button>
          <a-button type="primary" class="role-button" @click="selectRole('user')">我是教师/学生</a-button>
        </div>
      </div>
      <a-form
          v-else
          :model="form"
          :wrapperCol="{ span: 24 }"
          @finish="login"
          class="login-form w-[400px] p-lg xl:w-[440px] xl:p-xl h-fit text-text"
      >
        <h2 class="text-3xl-me">
          {{ roleNames[userRole] }}登录
        </h2>
        <a-divider></a-divider>
        <a-form-item :required="true" name="username" class="form-item">
          <a-input
              v-model:value="form.username"
              autocomplete="new-username"
              :placeholder="usernamePlaceholder"
              class="login-input h-[40px]"
          />
        </a-form-item>
        <a-form-item :required="true" name="password" class="form-item">
          <a-input
              v-model:value="form.password"
              autocomplete="new-password"
              placeholder="请输入登录密码"
              class="login-input h-[40px]"
              type="password"
          />
        </a-form-item>
        <a-button htmlType="submit" class="h-[40px] w-full" type="primary" :loading="loading">
          登录
        </a-button>
        <a-divider></a-divider>
        <div class="terms">
          登录即代表您同意我们的
          <span class="font-bold">用户条款</span>、<span class="font-bold">数据使用协议</span>、以及
          <span class="font-bold">Cookie使用协议</span>。
        </div>
        <div class="mt-4 text-center">
          <a-button type="link" @click="resetRole">返回选择身份</a-button>
        </div>
      </a-form>
    </div>
  </ThemeProvider>
</template>

<script lang="ts" setup>
import { reactive, ref, computed } from 'vue';
import { useAccountStore } from '@/store';
import { ThemeProvider } from 'stepin';

interface LoginFormProps {
  username: string;
  password: string;
  userType: string;
}

const loading = ref(false);
const roleSelected = ref(false);
const userRole = ref(''); // 'admin', 'doctor', 'user'
const form = reactive<LoginFormProps>({
  username: '',
  password: '',
  userType: '',
});

const roleNames = {
  admin: '管理员',
  doctor: '医生',
  user: '教师/学生',
};

const themeColors = {
  admin: { primary: { DEFAULT: '#FF4D4F' } }, // 红色
  doctor: { primary: { DEFAULT: '#52C41A' } }, // 绿色
  user: { primary: { DEFAULT: '#1890FF' } },   // 蓝色
};

const usernamePlaceholder = computed(() => {
  if (userRole.value === 'admin') {
    return '请输入管理员用户名';
  } else if (userRole.value === 'doctor') {
    return '请输入医生工号';
  } else {
    return '请输入学号或工号';
  }
});

const emit = defineEmits<{
  (e: 'success', fields: LoginFormProps): void;
  (e: 'failure', reason: string, fields: LoginFormProps): void;
}>();

const accountStore = useAccountStore();

function selectRole(role: string) {
  userRole.value = role;
  roleSelected.value = true;
}

function resetRole() {
  userRole.value = '';
  roleSelected.value = false;
  form.username = '';
  form.password = '';
}

function login() {
  loading.value = true;

  // 根据用户名长度确定userType
  if (userRole.value === 'user') {
    if (form.username.length === 8) {
      form.userType = 's'; // 学生
    } else if (form.username.length === 9) {
      form.userType = 't'; // 教师
    } else {
      loading.value = false;
      emit('failure', '用户名长度不正确', form);
      return;
    }
  } else if (userRole.value === 'admin') {
    form.userType = 'a'; // 管理员
  } else if (userRole.value === 'doctor') {
    form.userType = 'd'; // 医生
  }

  accountStore
      .login(form.username, form.password, form.userType)
      .then(() => {
        emit('success', form);
      })
      .catch((e) => {
        emit('failure', e.message, form);
      })
      .finally(() => (loading.value = false));
}
</script>

<style scoped>
.login-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 500px;
  min-height: 450px; /* Increased height */
  background-color: #f0f2f5;
  padding: 30px; /* Increased padding */
  border-radius: 8px;
}

.role-selection {
  width: 100%;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
}


 .login-input {
   background-color: #f0f0f0; /* Set background color to white */
   color: #000000; /* Set text color to black for better readability */
 }


.role-button {
  width: 100%;
  height: 50px;
  font-size: 18px;
}

.form-item {
  margin-bottom: 16px;
}

.login-form {
  background-color: #fff;
  padding: 40px; /* Increased padding */
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.terms {
  margin-top: 16px;
  font-size: 14px;
  color: #000; /* Changed color to black */
}

.text-2xl-me {
  font-size: 24px;
  color: #000; /* Changed color to black */
  /*在上方显示
   */
  margin-bottom: 50px;
}
.text-3xl-me {
  font-size: 24px;
  color: #000; /* Changed color to black */
  text-align: center;
  font-weight: bold;
}
.head {
  justify-content: center;
}


</style>
