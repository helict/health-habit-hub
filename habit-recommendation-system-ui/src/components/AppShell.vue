<template>
  <div class="row" style="justify-content:space-between; align-items:flex-start; margin-bottom:14px">
    <div>
      <div style="font-weight:950; font-size:18px">Habit Recommendation System UI</div>
      <div class="muted" style="font-size:13px; margin-top:4px">
        UI for HHH-service (8081): <code>/ingest</code> · <code>/habits</code> · <code>/system/config</code>
      </div>
    </div>

    <div class="row">
      <RouterLink class="btn" to="/donate">Donate Habit</RouterLink>
      <RouterLink class="btn primary" to="/manage">Manage Habits</RouterLink>
    </div>
  </div>

  <RouterView />
</template>

<script setup lang="ts"></script>
