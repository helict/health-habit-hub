<script setup lang="ts">
import { computed, ref } from "vue";
import type { HabitItem } from "../api/types";
import { createdAtFromObjectId, fmtTime } from "../api/utils";
import ContextLabels from "./ContextLabels.vue";

const props = defineProps<{ item: HabitItem }>();
const open = ref(false);

const isHabit = computed(() => (props.item.habit_class ?? 0) === 1);

const createdAtISO = computed(() => {
  return props.item.created_at || (props.item._id ? createdAtFromObjectId(props.item._id) : null);
});
const createdAtText = computed(() => fmtTime(createdAtISO.value) || "N/A");

const contexts = computed(() => {
  const mapped = props.item.contexts_mapped || [];
  return mapped.length ? mapped : (props.item.contexts_raw || []);
});
</script>

<template>
  <div class="card" style="background:#fff">
    <div class="row" style="justify-content:space-between; align-items:flex-start">
      <div style="flex:1; min-width:0">
        <div class="row" style="align-items:center; gap:8px">
          <span class="badge" :class="isHabit ? 'ok' : 'no'">
            {{ isHabit ? "habit" : "non-habit" }}
          </span>
          <!-- <span class="muted" style="font-size:13px">
            habit_key: <code>{{ item.habit_key }}</code>
          </span>
          <span v-if="item.uuid" class="muted" style="font-size:13px">
            uuid: <code>{{ item.uuid }}</code>
          </span> -->
          <div style="margin-top:-2px; font-weight:950; line-height:1.2">
          {{ item.habit }}
        </div>
        </div>

        <div class="hr"></div>


        <div v-if="item.mapping_params" class="row" style="margin-top:10px; gap:10px">
          <span class="badge">language: <code>{{ item.language }}</code></span>
          <span class="badge">threshold: <code>{{ item.mapping_params.threshold }}</code></span>
          <span class="badge">top_n: <code>{{ item.mapping_params.top_n }}</code></span>
        </div>

        <div v-if="item.bcio_mapping_error" class="hr"></div>
        <div v-if="item.bcio_mapping_error" class="card" style="border-color: rgba(239,68,68,.25)">
          <div style="font-weight:900">BCIO mapping error</div>
          <div class="muted" style="white-space:pre-wrap">{{ item.bcio_mapping_error }}</div>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px">
        <button class="btn primary" @click="open = !open">
          {{ open ? "Collapse" : "Expand" }} Labels
        </button>
      </div>
    </div>

    <div v-if="open" class="hr"></div>
    <ContextLabels v-if="open" :contexts="contexts" />
  </div>
</template>
