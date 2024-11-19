<script lang="ts" setup>
  import { ref } from 'vue';
  import ProfileInfo from './ProfileInfo.vue';
  import AlterRole from "@/pages/personal/AlterRole.vue";
  const select = ref('overview');
</script>
<template>
  <div class="personal">
    <div class="banner w-full rounded-xl p-base items-baseline">
      <a-breadcrumb class="navi">
        <a-breadcrumb-item class="text-text-inverse">Home</a-breadcrumb-item>
        <a-breadcrumb-item>Personal</a-breadcrumb-item>
      </a-breadcrumb>
      <div class="mt-0.5 text-text-inverse text-xl font-semibold">Overview</div>
      <div
        class="profile flex items-center justify-between p-base bg-container rounded-2xl absolute -bottom-16 left-6 shadow-lg"
      >
        <div class="info flex items-center">
          <img class="w-20 rounded-lg" src="@/assets/avatar/face-1.jpg" />
          <div class="flex flex-col justify-around ml-4">
            <span class="text-title text-xl font-bold">Sarah Jacob</span>
            <span class="text-subtext font-semibold">CEO / Co-Founder</span>
          </div>
        </div>
        <a-radio-group v-model:value="select">
          <a-radio-button value="overview">OVERVIEW</a-radio-button>
        </a-radio-group>
      </div>
    </div>
    <div class="mypersonal">

      <ProfileInfo class="flex-1 ml-lg" />
      <AlterRole />
    </div>
    <a-divider class="my-10" />

  </div>
</template>
<style lang="less" scoped>
  .personal {
    .banner {
      height: 240px;
      background-image: url('@/assets/personal-bg.png');
      background-position: 50% 10%;
      background-size: cover;
      position: relative;

      .profile {
        width: calc(~'100% - 48px');
      }

      :deep(.navi) {
        .ant-breadcrumb-link,
        .ant-breadcrumb-separator {
          color: rgba(255, 255, 255, 0.65);
        }

        & > span:last-child .ant-breadcrumb-link {
          @apply text-text-inverse;
        }
      }
    }
  }
  .mypersonal {
    margin-top: 24px;
    display: flex;
    justify-content: space-evenly;
    flex-direction: column;
  }
</style>
