<template>
  <div
    class="row appTopbar"
    style="justify-content:space-between; align-items:flex-start; margin-bottom:14px"
  >
    <div>
      <div style="font-weight:950; font-size:28px">Habit Recommendation System UI</div>
      <!-- <div class="muted" style="font-size:13px; margin-top:4px">
        UI for HHH-service (8081)
      </div> -->
    </div>

    <div class="row navBtns">
      <RouterLink class="btn navBtn" to="/donate">Donate Habit</RouterLink>
      <RouterLink class="btn navBtn" to="/manage">Manage Habits</RouterLink>
      <RouterLink class="btn navBtn" to="/profile">Health Profile</RouterLink>
      <RouterLink class="btn navBtn" to="/recommend">Get Recommendation</RouterLink>
      <RouterLink class="btn navBtn" to="/live">Manage Recommendations</RouterLink>
    </div>
  </div>

  <RouterView />
</template>

<script setup lang="ts"></script>

<style scoped>
.navBtns .navBtn {
  user-select: none;
  cursor: pointer;

  transition:
    transform 120ms ease,
    box-shadow 120ms ease,
    border-color 120ms ease,
    background-color 120ms ease,
    filter 120ms ease;
}

.navBtns .navBtn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
}

.navBtns .navBtn:active {
  transform: translateY(0px) scale(0.98);
  box-shadow: 0 6px 12px rgba(15, 23, 42, 0.06);
}

.navBtns .navBtn:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.7);
  outline-offset: 2px;
}

.navBtns .navBtn.router-link-exact-active {
  border-color: rgba(59, 130, 246, 0.45);
  background: rgba(59, 130, 246, 0.08);
}
</style>
