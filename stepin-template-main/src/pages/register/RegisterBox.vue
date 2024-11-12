<template>
  <ThemeProvider :color="{ middle: { 'bg-base': '#fff' }, primary: { DEFAULT: '#1896ff' } }">

    <div class="Register-box rounded-sm">
      <p v-if="!showSecondPart" class="text-3xl-me font-bold">
        新用户注册
      </p>
      <a-form
          v-if="!showSecondPart"
          :model="form"
          :wrapperCol="{ span: 24 }"
          @finish="handleFirstPart"
          class="Register-form w-[400px] p-lg xl:w-[440px] xl:p-xl h-fit text-text"
      >
        <a-form-item :required="true" name="username" class="form-item">
          <a-input
              v-model:value="form.username"
              autocomplete="new-username"
              placeholder="请输入学工号，学号默认8位，工号默认9位"
              class="Register-input h-[40px]"
          />
        </a-form-item>
        <a-form-item :required="true" name="password" class="form-item">
          <div class="password-container">
            <a-input
                v-model:value="form.password"
                autocomplete="new-password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入混合密码，不超过25位"
                class="Register-input h-[40px]"
            />
            <button type="button" @click="togglePasswordVisibility" class="show-password-button">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </a-form-item>
        <a-button htmlType="submit" class="h-[40px] w-full" type="primary"> 下一步 </a-button>
      </a-form>

      <a-form
          v-if="showSecondPart"
          :model="form"
          :wrapperCol="{ span: 24 }"
          @finish="Register"
          class="Register-form w-[400px] p-lg xl:w-[440px] xl:p-xl h-fit text-text"
      >
        <div class="custom-text">
          为了让医生更好的了解您，请务必填写真实的信息。
        </div>
        <a-divider></a-divider>
        <a-form-item :required="true" name="name" class="form-item">
          <a-input
              v-model:value="form.name"
              autocomplete="new-name"
              placeholder="请输入姓名"
              class="Register-input h-[40px]"
          />
        </a-form-item>
        <a-form-item :required="true" name="gender" class="form-item">
          <a-input
              v-model:value="form.gender"
              autocomplete="new-gender"
              placeholder="请输入性别"
              class="Register-input h-[40px]"
          />
        </a-form-item>
        <a-form-item :required="true" name="phone" class="form-item">
          <a-input
              v-model:value="form.phone"
              autocomplete="new-phone"
              placeholder="请输入手机号"
              class="Register-input h-[40px]"
          />
        </a-form-item>
        <a-form-item :required="false" name="borndate" class="form-item">
          <div class="date-select-container">
            <span class="date-s">生日:</span>
            <a-select v-model:value="form.year" placeholder="年" class="date-select" :get-popup-container="(triggerNode) =>triggerNode.parentNode">
              <a-select-option v-for="year in years" :key="year" :value="year">{{ year }}</a-select-option>
            </a-select>
            <a-select v-model:value="form.month" placeholder="月" class="date-select" :get-popup-container="(triggerNode) =>triggerNode.parentNode">
              <a-select-option v-for="month in months" :key="month" :value="month">{{ month }}</a-select-option>
            </a-select>
            <a-select v-model:value="form.day" placeholder="日" class="date-select" :get-popup-container="(triggerNode) =>triggerNode.parentNode">
              <a-select-option v-for="day in days" :key="day" :value="day">{{ day }}</a-select-option>
            </a-select>
          </div>
        </a-form-item>
        <a-form-item :required="true" name="identity" class="form-item">
          <a-input
              v-model:value="form.identity"
              autocomplete="new-identity"
              placeholder="请输入身份证号"
              class="Register-input h-[40px]"
          />
        </a-form-item>

        <a-button htmlType="submit" class="h-[40px] w-full" type="primary" :loading="loading"> 注册 </a-button>
        <a-button type="default" class="h-[40px] w-full mt-2" @click="goBack"> 上一步 </a-button>
      </a-form>
      <p class="foot-me">
        仅限<span class="font-bold">用户</span>注册，当前身份不支持<span class="font-bold">医生、管理员</span>注册
      </p>
    </div>
  </ThemeProvider>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { AccountParams, useAccountStore } from '@/store';
import { ThemeProvider } from 'stepin';
import { useRouter } from 'vue-router';
import { Button } from 'ant-design-vue';

const loading = ref(false);
const showPassword = ref(false);
const showSecondPart = ref(false);

const form = reactive({
  username: undefined,
  password: undefined,
  name: undefined,
  gender: undefined,
  borndate: undefined,
  phone: undefined,
  identity: undefined,
  year: undefined,
  month: undefined,
  day: undefined,
});

const years = Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i);
const months = Array.from({ length: 12 }, (_, i) => i + 1);
const days = Array.from({ length: 31 }, (_, i) => i + 1);

const router = useRouter();
const accountStore = useAccountStore();

function handleFirstPart() {
  if (form.username && form.password) {
    showSecondPart.value = true;
  }
}

function goBack() {
  showSecondPart.value = false;
}

function Register() {
  loading.value = true;
  const params: AccountParams = {
    username: form.username.toString(),
    password: form.password.toString(),
    name: form.name.toString(),
    gender: form.gender.toString(),
    borndate: `${form.year}-${form.month}-${form.day}`.toString(),
    phone: form.phone.toString(),
    identity: form.identity.toString(),
    usertype: form.username.toString().length === 8 ? 's' : 't',
  };
  accountStore
      .Register(params)
      .finally(() => (loading.value = false));
}
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}
</script>

<style scoped lang="less">
.password-container {
  position: relative;
}

.Register-box {
  border-radius: 8px;
}

.form-item {
  margin-bottom: 16px;
}

.show-password-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #1896ff;
}
.foot-me {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 30px;
}

.date-select-container {
  display: flex;
  gap: 10px;
}

.text-3xl-me {
  font-size: 24px;
  color: #000; /* Changed color to black */
  /*在上方显示
   */
  margin-top: 30px;
  margin-bottom: 0;
  text-align: center;
}

.date-select {
  width: 100px;

}
.date-s {
  width: 35px;
  margin-top: 5px;
  color: #b9b7b7; /* Set the font color to gray */
}
</style>

<style scoped>
.custom-text {
  color: #1896ff; /* Custom font color */
  font-size: 15px; /* Custom font size */
}
</style>