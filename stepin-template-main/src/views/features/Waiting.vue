<!-- 文件路径：src/views/features/Waiting.vue -->
<template>
  <div class="feature-detail px-10 py-8">
    <h1 class="text-3xl font-bold mb-6">候诊查询</h1>
    <p class="mb-4">
      使用我们的<strong>候诊查询功能</strong>，您可以实时查看自己的排队信息，了解当前的候诊进度，合理安排到院时间，避免长时间等待。
    </p>

    <!-- 功能特点 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">功能特点：</h2>
    <ul class="list-disc list-inside mb-4">
      <li><strong>实时排队信息</strong>：查看当前排队人数和预计等待时间，掌握最新候诊动态。</li>
      <li><strong>智能提醒</strong>：接近就诊时间时，系统会通过短信或消息通知您，防止错过就诊。</li>
      <li><strong>历史候诊记录</strong>：查看以往的候诊情况，方便总结就诊经验。</li>
      <li><strong>多科室支持</strong>：支持多个科室的候诊查询，满足不同就诊需求。</li>
      <li><strong>用户友好的界面</strong>：简洁直观的界面设计，让您轻松操作。</li>
      <li><strong>数据安全保障</strong>：确保您的个人信息和候诊数据的安全性。</li>
    </ul>

    <!-- 使用步骤 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">使用步骤：</h2>
    <ol class="list-decimal list-inside mb-4">
      <li>登录您的账号，进入“候诊查询”页面。</li>
      <li>选择您当前就诊的科室和医生。</li>
      <li>系统将显示您的排队号和当前候诊进度。</li>
      <li>根据预计等待时间，合理安排您的到院时间。</li>
      <li>接近就诊时间时，系统会自动发送提醒通知。</li>
      <li>如需取消或更改预约，可在“我的预约”中进行操作。</li>
    </ol>



    <!-- 常见问题 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">常见问题：</h2>
    <div class="faq mb-4">
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">如何查看我的排队信息？</h3>
        <p>
          登录后，进入“候诊查询”页面，选择相应的科室和医生，系统会自动显示您的排队号和预计等待时间。
        </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">如果我需要取消预约怎么办？</h3>
        <p>
          在“我的预约”页面中，您可以查看所有预约记录，并选择需要取消的预约，点击“取消预约”按钮即可。
        </p>
      </div>
      <div class="faq-item mb-4">
        <h3 class="text-xl font-semibold">候诊信息会更新多频繁？</h3>
        <p>
          系统会每隔一分钟自动刷新一次候诊信息，确保您获取到最新的排队动态。
        </p>
      </div>
      <!-- 可以根据需要添加更多常见问题 -->
    </div>

    <!-- 联系我们 -->
    <h2 class="text-2xl font-bold mt-6 mb-4">联系我们：</h2>
    <p>
      如果您在使用过程中有任何疑问或需要帮助，请通过以下方式联系我们的客服团队：
    </p>
    <ul class="list-none mt-2">
      <li><strong>电话：</strong> 010-12345678</li>
      <li><strong>邮箱：</strong> support@buaa-hospital.com</li>
      <li><strong>在线客服：</strong> 点击页面右下角的客服图标与我们在线沟通。</li>
    </ul>
  </div>
</template>
