<script setup lang="ts">
import { computed } from "vue";
import type { ContextItem, BcioMapping } from "../api/types";
import { round4 } from "../api/utils";

const props = defineProps<{ contexts: ContextItem[] }>();

const LABELS = [
  "TIME",
  "PHYSICAL SETTING",
  "PRIOR BEHAVIOR",
  "OTHER PEOPLE",
  "INTERNAL STATE",
  "BEHAVIOR",
  "REASONING",
];

const grouped = computed(() => {
  const groups: Record<string, ContextItem[]> = {};
  for (const L of LABELS) groups[L] = [];

  for (const c of props.contexts || []) {
    const ln = c?.name ?? "UNKNOWN";
    if (!groups[ln]) groups[ln] = [];
    groups[ln].push(c);
  }

  const orderedKeys = [...LABELS, ...Object.keys(groups).filter((k) => !LABELS.includes(k))];
  return orderedKeys.map((k) => ({ label: k, items: groups[k] || [] }));
});

function shouldShowItem(c: ContextItem): boolean {
  if (c.classification === 1) return true;
  if (c.value && c.value.trim() !== "") return true;
  return false;
}

function mappings(c: ContextItem): BcioMapping[] {
  return c.bcio_mappings || [];
}
</script>

<template>
  <div>
    <div style="font-weight:900; margin-bottom:10px">Context Labels</div>

    <div v-for="g in grouped" :key="g.label" class="card" style="background:#f8fbff; margin-bottom:10px">
      <div style="display:flex; justify-content:space-between; align-items:center">
        <div style="font-weight:900"><code>{{ g.label }}</code></div>
        <div class="muted" style="font-size:12px">items: {{ g.items.length }}</div>
      </div>

      <div class="hr"></div>

      <div v-if="g.items.length === 0" class="muted" style="font-size:13px">No data.</div>

      <div v-else class="col" style="gap:10px">
        <div
          v-for="(c, idx) in g.items"
          :key="idx"
          v-show="shouldShowItem(c)"
          class="card"
          style="background:#fff"
        >
          <div class="row" style="justify-content:space-between; align-items:center">
            <div class="muted" style="font-size:12px">
              <!--classification=<code>{{ c.classification }}</code>,-->
              Confidence score=<code>{{ c.confidence }}</code>
            </div>
          </div>

          <div style="margin-top:6px; font-weight:800">
            value: <span style="font-weight:900">{{ c.value ?? "null" }}</span>
          </div>

          <div v-if="mappings(c).length" class="hr"></div>

          <div v-if="mappings(c).length">
            <div class="muted" style="font-size:13px; margin-bottom:6px">BCIO mappings</div>
            <div class="col" style="gap:8px">
              <div v-for="(m, j) in mappings(c)" :key="j" class="card" style="background:#f8fafc">
                <div class="row" style="justify-content:space-between; align-items:center">
                  <div style="font-weight:900">{{ m.bcio_label }}</div>
                  <div class="muted" style="font-size:12px">
                    probability=<code>{{ round4(m.probability) }}</code>
                  </div>
                </div>
                <div class="muted" style="font-size:12px; margin-top:6px">
                  iri: <code>{{ m.iri }}</code>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="muted" style="font-size:12px; margin-top:8px">No BCIO mapping.</div>
        </div>
      </div>
    </div>
  </div>
</template>
