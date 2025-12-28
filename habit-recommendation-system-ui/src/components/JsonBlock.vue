<script setup lang="ts">
defineProps<{ value: any }>();
</script>

<template>
  <pre>{{ JSON.stringify(value, null, 2) }}</pre>
</template>
