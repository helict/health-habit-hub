<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { listRecommendHistory } from "../api/hhh";
import type { RecommendOut } from "../api/types";
import RecommendHistoryItem from "../components/RecommendHistoryItem.vue";

const loading = ref(false);
const error = ref<string | null>(null);

const items = ref<RecommendOut[]>([]);
const total = ref(0);

const limit = ref(20);
const skip = ref(0);

const page = computed(() => Math.floor(skip.value / limit.value) + 1);
const pageCount = computed(() => Math.max(1, Math.ceil(total.value / limit.value)));

async function load() {
  loading.value = true;
  error.value = null;
  try {
    const res = await listRecommendHistory({ limit: limit.value, skip: skip.value });
    items.value = res.items || [];
    total.value = res.total || 0;
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
        <div style="font-weight:950; font-size:18px">Recommendation History</div>
        <div class="muted" style="font-size:13px; margin-top:6px">
          You can review an overview of your personalized recommendations and all the information used to generate them on this page.
        </div>
      </div>

      <button class="btn primary" :disabled="loading" @click="load">
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <div class="hr"></div>

    <div class="row" style="justify-content:space-between; align-items:center">
      <div class="row" style="align-items:center">
        <span class="badge">Total: {{ total }}</span>

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
      <RecommendHistoryItem v-for="it in items" :key="it.text_signature || it.request_uuid" :item="it" />
    </div>
  </div>
</template>
