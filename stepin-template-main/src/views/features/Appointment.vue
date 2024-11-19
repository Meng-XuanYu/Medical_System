<!-- 文件路径：src/views/features/Appointment.vue -->
<template>
  <div class="feature-detail px-10 py-8">
    <h1 class="text-3xl font-bold mb-6">预约挂号</h1>
    <p class="mb-4">
      在我们的<strong>预约挂号功能</strong>上，您可以在线查看医生的排班信息，并为自己预约挂号。无需排队，轻松选择合适的时间段进行就诊，省时省力。
    </p>

    <!-- 功能特点 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">功能特点：</h2>
    <ul class="list-disc list-inside mb-4">
      <li><strong>实时查看</strong>医生的可预约时间段，掌握最新排班信息。</li>
      <li>根据自己的时间安排，<strong>灵活选择就诊时间</strong>，避免冲突。</li>
      <li>预约成功后，<strong>及时收到确认信息</strong>，安心等待就诊。</li>
      <li><strong>自动提醒</strong>：预约成功后，系统会在就诊前发送提醒通知，确保您准时到达。</li>
      <li><strong>预约管理</strong>：在“我的预约”中查看、修改或取消预约，操作便捷。</li>
      <li><strong>多科室支持</strong>：支持多个科室的预约，满足不同就诊需求。</li>
    </ul>

    <!-- 使用步骤 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">使用步骤：</h2>
    <ol class="list-decimal list-inside mb-4">
      <li>登录您的账号，进入“预约挂号”页面。</li>
      <li>选择科室和医生，查看可预约的时间段。</li>
      <li>选择合适的时间，点击“预约”按钮。</li>
      <li>确认预约信息，提交预约请求。</li>
      <li>预约成功后，您可以在“我的预约”中查看详情。</li>
      <li>如需修改或取消预约，请在“我的预约”页面进行操作。</li>
    </ol>

    <!-- 常见问题 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">常见问题：</h2>
    <div class="faq mb-4">
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">如何查看医生的排班信息？</h3>
        <p>
          登录后，进入“预约挂号”页面，选择您需要预约的科室和医生，系统将自动显示医生的排班时间和可预约的时间段。
        </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">预约成功后如何查看我的预约详情？</h3>
          <p>
            您可以在“我的预约”页面中查看所有预约记录，包括预约时间、医生信息和就诊地点等详细信息。
          </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">我可以修改或取消预约吗？</h3>
        <p>
          是的，您可以在“我的预约”页面中选择需要修改或取消的预约记录，点击相应的按钮进行操作。请注意，根据医院政策，取消预约可能需要提前一定时间。
        </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">如果预约失败怎么办？</h3>
        <p>
          如果预约过程中出现问题，您可以刷新页面重新尝试，或者联系在线客服寻求帮助。确保您的网络连接正常，并检查是否选择了有效的预约时间段。
        </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">我可以同时预约多个科室吗？</h3>
        <p>
          是的，您可以在不同的科室分别进行预约。请确保每个科室的预约时间不冲突，方便您合理安排就诊时间。
        </p>
      </div>
      <!-- 可以根据需要添加更多常见问题 -->
    </div>

    <!-- 联系我们 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">联系我们：</h2>
    <p>
      如果您在预约过程中有任何疑问或需要帮助，请通过以下方式联系我们的客服团队：
    </p>
    <ul class="list-none mt-2">
      <li><strong>电话：</strong> 010-12345678</li>
      <li><strong>邮箱：</strong> support@buaa-hospital.com</li>
      <li><strong>在线客服：</strong> 点击页面右下角的客服图标与我们在线沟通。</li>
    </ul>
  </div>
</template>

