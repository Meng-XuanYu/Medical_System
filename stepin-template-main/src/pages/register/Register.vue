<template>
  <div class="Register flex items-center justify-center">
    <Register-box class="shadow-lg" @success="onRegisterSuccess" />
  </div>
</template>
<script lang="ts" setup>
  import RegisterBox from './RegisterBox.vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  function onRegisterSuccess() {
    router.push('/admin');
  }
</script>
<style scoped lang="less">
  .Register {
    min-height: max(100vh, 720px);
    margin-top: -78px;
  }
</style>
