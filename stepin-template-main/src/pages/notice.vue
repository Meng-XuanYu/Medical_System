<template>
  <div class="notification-page">
    <h1>通知中心</h1>
    <a-tabs v-model:activeKey="activeTab" @change="handleTabChange">
      <a-tab-pane key="all" tab="所有通知"></a-tab-pane>
      <a-tab-pane key="system" tab="系统通知"></a-tab-pane>
      <a-tab-pane key="appointment" tab="预约提醒"></a-tab-pane>
      <a-tab-pane key="evaluation" tab="评价反馈"></a-tab-pane>
    </a-tabs>
    <a-list
        class="notification-list"
        :data-source="filteredNotifications"
        :renderItem="renderNotificationItem"
        :locale="{ emptyText: '暂无通知' }"
    >
    </a-list>
    <!-- 通知详情模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="currentNotification.title"
        footer={null}
        @cancel="handleModalCancel"
    >
      <p>{{ currentNotification.content }}</p>
      <div class="modal-footer">
        <span>{{ formatDateTime(currentNotification.send_time) }}</span>
        <a-button type="primary" @click="markAsRead(currentNotification.notification_id)">
          标记已读
        </a-button>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const activeTab = ref('all');
const notifications = ref([]);
const currentNotification = ref({});
const isModalVisible = ref(false);

// 模拟当前登录用户的信息，实际应从登录状态中获取
const currentUser = {
  id: 'U1234567',
  type: 'U', // 'D' 表示医生，'U' 表示用户
};

// 通知类型映射
const notificationTypes = {
  system: '系统通知',
  appointment: '预约提醒',
  evaluation: '评价反馈',
};

// 获取通知列表
function fetchNotifications() {
  // 调用后端API获取通知信息
  // 示例API调用：
  // axios.get(`/api/notifications?receiver_id=${currentUser.id}&receiver_type=${currentUser.type}`)
  //   .then(response => {
  //     notifications.value = response.data;
  //   });

  // 模拟数据
  notifications.value = [
    {
      notification_id: 'N0001',
      title: '系统升级通知',
      content: '系统将于今晚12点进行升级，届时可能会短暂影响服务，请知悉。',
      type: 'system',
      send_time: '2023-10-01 18:00:00',
      is_read: false,
    },
    {
      notification_id: 'N0002',
      title: '预约成功提醒',
      content: '您已成功预约2023-10-05上午的专家门诊，请准时就诊。',
      type: 'appointment',
      send_time: '2023-10-02 09:00:00',
      is_read: false,
    },
    {
      notification_id: 'N0003',
      title: '评价反馈',
      content: '患者张三对您的服务进行了评价：非常满意，医生很专业。',
      type: 'evaluation',
      send_time: '2023-10-03 14:30:00',
      is_read: true,
    },
  ];
}

// 根据选中的标签过滤通知
const filteredNotifications = computed(() => {
  if (activeTab.value === 'all') {
    return notifications.value;
  } else {
    return notifications.value.filter(notice => notice.type === activeTab.value);
  }
});

// 处理标签页切换
function handleTabChange(key) {
  activeTab.value = key;
}

// 渲染通知列表项
function renderNotificationItem({ item, index }) {
  return (
      <a-list-item
          key={item.notification_id}
          class={['notification-item', { 'notification-item-unread': !item.is_read }]}
          onClick={() => openNotification(item)}
      >
        <a-list-item-meta
            title={
              <span>
            {item.title}
                {!item.is_read && (
                    <a-badge
                        status="processing"
                        text="未读"
                        style="margin-left: 8px;"
                    />
                )}
          </span>
            }
            description={
              item.content.length > 50 ? item.content.substring(0, 50) + '...' : item.content
            }
        />
        <div class="notification-time">{formatDateTime(item.send_time)}</div>
      </a-list-item>
  );
}

// 打开通知详情模态框
function openNotification(item) {
  currentNotification.value = item;
  isModalVisible.value = true;

  // 标记为已读
  if (!item.is_read) {
    markAsRead(item.notification_id);
  }
}

// 关闭模态框
function handleModalCancel() {
  isModalVisible.value = false;
}

// 标记通知为已读
function markAsRead(notification_id) {
  // 调用后端API标记已读
  // axios.post(`/api/notifications/markAsRead`, { notification_id })
  //   .then(() => {
  //     message.success('已标记为已读');
  //     fetchNotifications();
  //   });

  // 模拟操作
  const notice = notifications.value.find(n => n.notification_id === notification_id);
  if (notice) {
    notice.is_read = true;
    message.success('已标记为已读');
  }
}

// 格式化日期时间
function formatDateTime(dateTime) {
  return new Date(dateTime).toLocaleString();
}

onMounted(() => {
  fetchNotifications();
});
</script>

<style scoped>
.notification-page {
  padding: 24px;
}

.notification-list {
  margin-top: 16px;
}

.notification-item {
  cursor: pointer;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f5f5f5;
}

.notification-item-unread {
  background-color: #e6f7ff;
}

.notification-time {
  color: #999;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
}

.modal-footer span {
  color: #999;
}
</style>
