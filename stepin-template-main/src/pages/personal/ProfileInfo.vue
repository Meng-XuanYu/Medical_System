<script lang="ts" setup>
import { defineProps } from 'vue';

const props = defineProps<{
  user: {
    user_id: string;
    name: string;
    gender: string;
    birth: string;
    id_number: string;
    phone: string;
  };
}>();
</script>

<template>
  <div class="profile-info">
    <div class="info-item">
      <strong>用户名: </strong>{{ props.user.user_id }}
    </div>
    <div class="info-item">
      <strong>昵称: </strong>{{ props.user.name }}
    </div>
    <div class="info-item">
      <strong>性别: </strong>{{ props.user.gender }}
    </div>
    <div class="info-item">
      <strong>生日: </strong>{{ props.user.birth }}
    </div>
    <div class="info-item">
      <strong>身份证号: </strong>{{ props.user.id_number }}
    </div>
    <div class="info-item">
      <strong>手机号: </strong>{{ props.user.phone }}
    </div>
  </div>
</template>

<style scoped>
.profile-info {
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.info-item {
  margin-bottom: 12px;
  font-size: 16px;
}

strong {
  font-weight: 600;
}
</style>
