<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { listHabits, systemConfig } from "../api/hhh";
import type { HabitItem, SystemConfigResponse } from "../api/types";
import HabitCard from "../components/HabitCard.vue";

const loading = ref(false);
const error = ref<string | null>(null);

const cfg = ref<SystemConfigResponse | null>(null);

const items = ref<HabitItem[]>([]);
const total = ref(0);

const limit = ref(20);
const skip = ref(0);
const onlyHabits = ref(true);

const page = computed(() => Math.floor(skip.value / limit.value) + 1);
const pageCount = computed(() => Math.max(1, Math.ceil(total.value / limit.value)));

async function load() {
  loading.value = true;
  error.value = null;
  try {
    const [c, res] = await Promise.all([
      systemConfig(),
      listHabits({ limit: limit.value, skip: skip.value, only_habits: onlyHabits.value }),
    ]);
    cfg.value = c;
    items.value = res.items;
    total.value = res.total;
  } catch (e: any) {
    error.value = e?.message || String(e);
  } finally {
    loading.value = false;
  }
}

function prev() {
  skip.value = Math.max(0, skip.value - limit.value);
  load();
}
function next() {
  if (skip.value + limit.value >= total.value) return;
  skip.value = skip.value + limit.value;
  load();
}

onMounted(load);
</script>

<template>
  <div class="card">
    <div class="row" style="justify-content:space-between; align-items:flex-start">
      <div>
        <div style="font-weight:950; font-size:18px">Manage Habits</div>
        <div class="muted" style="font-size:13px; margin-top:6px">
          Display data stored in the local habit database
        </div>
      </div>

      <button class="btn primary" :disabled="loading" @click="load">
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>


    <!-- <div class="card" style="background:#fff">
      <div style="font-weight:900">Current mapping params (env → /system/config)</div>
      <div v-if="cfg" class="row" style="margin-top:10px; align-items:center">
        <span class="badge">threshold: <code>{{ cfg.mapping_params.threshold }}</code></span>
        <span class="badge">top_n: <code>{{ cfg.mapping_params.top_n }}</code></span>
        <span class="badge">API_BASE: <code>{{ cfg.api_base }}</code></span>
      </div>
      <div v-else class="muted" style="margin-top:10px">Loading...</div>
    </div> -->

    <div class="hr"></div>

    <div class="row" style="justify-content:space-between; align-items:center">
      <div class="row" style="align-items:center">
        <span class="badge">Total: {{ total }}</span>

        <label class="row" style="align-items:center; gap:8px; margin-left:10px">
          <input type="checkbox" v-model="onlyHabits" @change="skip=0; load()" />
          <span class="muted" style="font-size:13px">Only habits</span>
        </label>

        <label class="row" style="align-items:center; gap:8px; margin-left:10px">
          <span class="muted" style="font-size:13px">Items per page</span>
          <select class="select" style="width:90px" v-model.number="limit" @change="skip=0; load()">
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="30">30</option>
            <option :value="50">50</option>
          </select>
        </label>
      </div>

      <div class="row" style="align-items:center">
        <button class="btn" :disabled="loading || page<=1" @click="prev">Prev</button>
        <span class="muted" style="font-size:13px">Page {{ page }} / {{ pageCount }}</span>
        <button class="btn" :disabled="loading || page>=pageCount" @click="next">Next</button>
      </div>
    </div>

    <div v-if="error" class="hr"></div>
    <div v-if="error" class="card" style="border-color: rgba(239,68,68,.25)">
      <div style="font-weight:900">Error</div>
      <div class="muted" style="white-space:pre-wrap">{{ error }}</div>
    </div>

    <div class="hr"></div>

    <div v-if="loading" class="muted">Loading...</div>
    <div v-else-if="items.length === 0" class="muted">No items.</div>

    <div v-else class="col" style="gap:12px">
      <HabitCard v-for="it in items" :key="it.habit_key" :item="it" />
    </div>
  </div>
</template>
