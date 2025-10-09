<script setup>
import { ref, computed } from "vue";

const habit = ref("");
const language = ref("en");
const loading = ref(false);
const error = ref("");
const result = ref(null);


const API_URL = import.meta.env.VITE_SEED_URL || "http://127.0.0.1:8081/send";

const jsonData = computed(() =>
  result.value?.data ? JSON.stringify(result.value.data, null, 2) : ""
);

async function submit() {
  if (!habit.value.trim()) return;
  loading.value = true;
  error.value = "";
  result.value = null;
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ habit: habit.value, language: language.value }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    result.value = await res.json();
  } catch (e) {
    error.value = e.message || String(e);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main style="padding:24px;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial">
    <h2>Habit Classifier (HHH → API)</h2>

    <div style="margin:12px 0;">
      <label>Sentence：</label>
      <input
        v-model="habit"
        placeholder="e.g. I always read a book before bed."
        style="width:520px;padding:8px 10px"
        @keyup.enter="submit"
      />
    </div>

    <div style="margin:12px 0;">
      <label>Language：</label>
      <select v-model="language" style="padding:8px 10px">
        <option value="en">English (en)</option>
        <option value="de">Deutsch (de)</option>
        <option value="zh">中文 (zh)</option>
      </select>
    </div>

    <div style="margin:12px 0;">
      <button :disabled="loading || !habit.trim()" @click="submit" style="padding:8px 12px">
        {{ loading ? "Submitting..." : "Submit" }}
      </button>
      <span v-if="error" style="color:#dc2626;margin-left:10px">{{ error }}</span>
    </div>

    <div v-if="result" style="border:1px solid #e5e7eb;border-radius:8px;padding:12px;margin-top:16px">
      <div>
        <strong>Result: </strong>
        <span :style="{color: result.ok ? '#16a34a' : '#dc2626'}">
          {{ result.ok ? "is a habit" : "not a habit — try again" }}
        </span>
      </div>
      <div style="margin-top:6px;"><strong>Message:</strong> {{ result.message }}</div>
      <div style="margin-top:10px;">
        <strong>Raw data from API:</strong>
        <pre style="background:#f9fafb;padding:10px;border-radius:6px;overflow:auto">{{ jsonData }}</pre>
      </div>
    </div>
  </main>
</template>
