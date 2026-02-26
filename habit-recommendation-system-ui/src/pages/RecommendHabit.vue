<script setup lang="ts">
import { ref, computed } from "vue";
import { recommend, recommendComment } from "../api/hhh";
import type {
  RecommendOut,
  KbHit,
  RecommendCommentReq,
  SelectedHabitOut,
  HabitRecommendation,
} from "../api/types";
import ContextLabels from "../components/ContextLabels.vue";
const DEFAULT_GOAL = `Enter your goal first — we’ll generate personalized recommendations for you.

For example:
I want to improve my sleep quality. I often scroll on my phone in bed, fall asleep slowly, and struggle to get up in the morning. I’d like to build a better bedtime routine.`;;
const goal = ref("");

const loading = ref(false);
const error = ref<string | null>(null);
const resp = ref<RecommendOut | null>(null);

// feedback (comment)
const commentText = ref("");
const commentBusy = ref(false);
const commentOk = ref(false);
const commentError = ref<string | null>(null);

const canSubmit = computed(() => goal.value.trim().length > 0);
const showEmptyWarn = computed(() => !canSubmit.value);

// ---- block #1: habit_recommendations ----
const recBlock = computed(() => resp.value?.recommendation_results_outputs || null);
const recMeta = computed(() => recBlock.value?.llm_meta || {});
const recMessage = computed(() => recBlock.value?.message || "");
const habitRecs = computed<HabitRecommendation[]>(
  () => recBlock.value?.habit_recommendations || []
);

// ---- block #2: hits grouped by (domain -> book) ----
type HitLine = { page_number: number; score: number; text: string };
type BookGroup = {
  domain: string;
  doc_id: string;
  doc_title: string;
  lines: HitLine[];
};
type DomainGroup = { domain: string; books: BookGroup[] };

const kbBlock = computed(() => resp.value?.kb_queries || null);
const kbMeta = computed(() => kbBlock.value?.llm_meta || {});
const kbRetrieval = computed(() => kbBlock.value?.retrieval || {});
const kbHits = computed<KbHit[]>(() => kbBlock.value?.hits || []);

const groupedHits = computed<DomainGroup[]>(() => {
  const hits = kbHits.value;
  const domMap = new Map<string, Map<string, BookGroup>>();

  for (const h of hits) {
    const domain = (h.domain || "unknown").trim() || "unknown";
    const title = (h.doc_title || "").trim();
    const docTitle = title || h.doc_id;
    const bookKey = `${h.doc_id}::${docTitle}`;

    if (!domMap.has(domain)) domMap.set(domain, new Map());
    const bookMap = domMap.get(domain)!;

    if (!bookMap.has(bookKey)) {
      bookMap.set(bookKey, {
        domain,
        doc_id: h.doc_id,
        doc_title: docTitle,
        lines: [],
      });
    }

    bookMap.get(bookKey)!.lines.push({
      page_number: h.page_number,
      score: h.score,
      text: h.text,
    });
  }

  const out: DomainGroup[] = [];
  for (const [domain, bookMap] of domMap.entries()) {
    const books = Array.from(bookMap.values()).map((b) => {
      b.lines.sort((a, c) => (c.score ?? 0) - (a.score ?? 0));
      return b;
    });
    books.sort((a, b) => a.doc_title.localeCompare(b.doc_title));
    out.push({ domain, books });
  }
  out.sort((a, b) => a.domain.localeCompare(b.domain));
  return out;
});

// ---- block #3: selected_habits ----
const selBlock = computed(() => resp.value?.selected_habits || null);
const selMeta = computed(() => selBlock.value?.llm_meta || {});
const selectedHabits = computed<SelectedHabitOut[]>(
  () => selBlock.value?.selected_habits || []
);

// ---- block #4: bilded_profiles ----
const profBlock = computed(() => resp.value?.bilded_profiles || null);
const profMeta = computed(() => profBlock.value?.llm_meta || {});
const profileDetailed = computed(() => profBlock.value?.profile_detailed || "");

// ---- block #5: feedback ----
const commentReady = computed(() => {
  return Boolean(resp.value?.request_uuid && resp.value?.text && resp.value?.text_signature);
});

function fmtScore(n: any) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "-";
  return x.toFixed(3);
}

function habitTopN(h: any) {
  const v =
    h?.retrieval?.top_n ??
    h?.retrieval?.topN ??
    h?.retrieval?.k ??
    h?.retrieval?.top_k ??
    null;
  return v == null ? "-" : String(v);
}

function habitThreshold(h: any) {
  const v =
    h?.retrieval?.threshold ??
    h?.retrieval?.score_threshold ??
    h?.retrieval?.min_score ??
    null;
  if (v == null) return "-";
  return fmtScore(v);
}

async function submit() {
  error.value = null;
  resp.value = null;

  commentOk.value = false;
  commentError.value = null;
  commentBusy.value = false;

  if (!canSubmit.value) {
    error.value = "To receive recommendations, please enter your goal.";
    return;
  }

  loading.value = true;
  try {
    const r = await recommend(goal.value.trim());
    resp.value = r;

    commentText.value = r?.user_feedback || "";

    commentOk.value = false;
    commentError.value = null;
  } catch (e: any) {
    error.value = e?.message || String(e);
  } finally {
    loading.value = false;
  }
}

async function saveFeedback() {
  commentError.value = null;
  commentOk.value = false;

  if (!resp.value?.request_uuid || !resp.value?.text || !resp.value?.text_signature) {
    commentError.value = "The current results are missing the fields required to save feedback.";
    return;
  }

  const req: RecommendCommentReq = {
    request_uuid: resp.value.request_uuid,
    text: resp.value.text,
    text_signature: resp.value.text_signature!,
    comment: (commentText.value ?? "").trim(),
  };

  commentBusy.value = true;
  try {
    await recommendComment(req);
    commentOk.value = true;
  } catch (e: any) {
    commentError.value = e?.message || String(e);
  } finally {
    commentBusy.value = false;
  }
}
</script>

<template>
  <div class="card page recCard">

    <div class="row headerRow">
      <div>
        <div class="title">Get recommendations</div>
        <div class="muted desc">
          Enter a specific behavior you want to improve, or a broader goal. Based on your existing form data, daily
          habits, and personal knowledge base, the system will generate actionable habit suggestions tailored to your
          everyday context.
        </div>
      </div>
    </div>

    <div class="hr"></div>

    <div class="row mainRow">
      <div class="left">
        <label class="muted label">Goal:</label>
        <div class="hr3"></div>
        <textarea class="textarea bigTextarea" v-model="goal" :placeholder="DEFAULT_GOAL"></textarea>

        <div v-if="showEmptyWarn" class="hint muted">⚠️ To receive recommendations, please enter your goal.</div>
        <div v-else class="hint muted">⚠️ The first recommendation will trigger the download of the BGE-M3 embeddings
          and the indexing of the PDFs in the knowledge base. The processing time depends on the length and number of
          the PDFs. Please be patient :D
        </div>
      </div>

      <div class="right col">
        <div class="spacer"></div>

        <button class="btn primary bigBtn btnFx" :disabled="loading || !canSubmit" @click="submit">
          {{ loading ? "Processing..." : "Generate recommendations" }}
        </button>

        <RouterLink class="btn bigBtn btnFx" to="/live">Go to management</RouterLink>
      </div>
    </div>

    <div v-if="error" class="hr"></div>
    <div v-if="error" class="card errorCard">
      <div class="errTitle">Error</div>
      <div class="muted" style="white-space: pre-wrap">{{ error }}</div>
    </div>

    <div v-if="resp" class="hr"></div>
    <div v-if="resp" class="card respCard">
      <!-- ===== Block 1 ===== -->
      <details class="details blockDetails" open>
        <summary class="blockSummary">
          <div class="blockTitle">habit recommendations</div>
          <div class="blockRight">
            <div class="metaBadges">
              <span class="badge">provider: <code>{{ recMeta.provider || "-" }}</code></span>
              <span class="badge">model: <code>{{ recMeta.model || "-" }}</code></span>
            </div>
            <span class="togglePill togglePillSm" aria-hidden="true"></span>
          </div>
        </summary>

        <div v-if="recMessage" class="muted" style="margin-top: 8px; white-space: pre-wrap">
          {{ recMessage }}
        </div>

        <div class="hr"></div>

        <div v-if="habitRecs.length === 0" class="muted">No habit recommendations.</div>

        <div v-else class="stack">
          <details v-for="(r, i) in habitRecs" :key="i" class="details innerDetails">
            <summary class="innerSummary">
              <div class="innerSummaryRow">
                <div class="innerSummaryText">
                  <div class="sumTitle">{{ r.context }}</div>
                  <div class="muted sumSub">behavior: <code>{{ r.behavior }}</code></div>
                </div>
                <span class="togglePill togglePillSm" aria-hidden="true"></span>
              </div>
            </summary>

            <div class="hr"></div>

            <div class="kv">
              <div class="k">context</div>
              <div class="v" style="white-space: pre-wrap">{{ r.context }}</div>
            </div>

            <div class="kv">
              <div class="k">behavior</div>
              <div class="v" style="white-space: pre-wrap">{{ r.behavior }}</div>
            </div>

            <div class="kv">
              <div class="k">explanation</div>
              <div class="v" style="white-space: pre-wrap; line-height: 1.55">
                {{ r.explanation }}
              </div>
            </div>
          </details>
        </div>
      </details>

      <div class="hr2"></div>

      <!-- ===== Block 2 ===== -->
      <details class="details blockDetails">
        <summary class="blockSummary">
          <div class="blockTitle">RAG retrieval results</div>

          <div class="blockRight">
            <div class="metaBadges">
              <span class="badge">provider: <code>{{ kbMeta.provider || "-" }}</code></span>
              <span class="badge">model: <code>{{ kbMeta.model || "-" }}</code></span>
              <span class="badge">top_n: <code>{{ kbRetrieval.top_n ?? "-" }}</code></span>
              <span class="badge">threshold: <code>{{ kbRetrieval.score_threshold ?? "-" }}</code></span>
            </div>
            <span class="togglePill togglePillSm" aria-hidden="true"></span>
          </div>
        </summary>

        <div class="hr"></div>

        <div v-if="groupedHits.length === 0" class="muted">No RAG retrieval results.</div>

        <div v-else class="stack">
          <details v-for="dg in groupedHits" :key="dg.domain" class="details innerDetails">
            <summary class="innerSummary">
              <div class="innerSummaryRow">
                <div class="innerSummaryText">
                  <div class="sumTitle">
                    domain: <code>{{ dg.domain }}</code>
                    <span class="muted sumSubInline">books: {{ dg.books.length }}</span>
                  </div>
                </div>
                <span class="togglePill togglePillSm" aria-hidden="true"></span>
              </div>
            </summary>

            <div class="hr"></div>

            <div class="stack">
              <details v-for="bk in dg.books" :key="bk.doc_id + bk.doc_title" class="details innerDetails2">
                <summary class="innerSummary">
                  <div class="innerSummaryRow">
                    <div class="innerSummaryText">
                      <div class="sumTitle">{{ bk.doc_title }}</div>
                      <div class="muted sumSub">hits: <code>{{ bk.lines.length }}</code></div>
                    </div>
                    <span class="togglePill togglePillSm" aria-hidden="true"></span>
                  </div>
                </summary>

                <div class="hr"></div>

                <div class="stack">
                  <details v-for="(ln, idx) in bk.lines" :key="idx" class="hitLine">
                    <summary class="hitSummary">
                      <div class="hitBadges">
                        <span class="badge">page: <code>{{ ln.page_number }}</code></span>
                        <span class="badge">score: <code>{{ fmtScore(ln.score) }}</code></span>
                      </div>
                      <span class="togglePill togglePillSm" aria-hidden="true"></span>
                    </summary>

                    <div class="hr"></div>
                    <div class="muted" style="white-space: pre-wrap; line-height: 1.55">
                      {{ ln.text }}
                    </div>
                  </details>
                </div>
              </details>
            </div>
          </details>
        </div>
      </details>

      <div class="hr2"></div>

      <!-- ===== Block 3 ===== -->
      <details class="details blockDetails" open>
        <summary class="blockSummary">
          <div class="blockTitle">selected habits</div>

          <div class="blockRight">
            <div class="metaBadges">
              <span class="badge">provider: <code>{{ selMeta.provider || "-" }}</code></span>
              <span class="badge">model: <code>{{ selMeta.model || "-" }}</code></span>
            </div>
            <span class="togglePill togglePillSm" aria-hidden="true"></span>
          </div>
        </summary>

        <div class="hr2"></div>

        <div v-if="selectedHabits.length === 0" class="muted">No selected habits.</div>

        <div v-else class="stack">
          <details v-for="(h, i) in selectedHabits" :key="h.habit_key || i" class="details innerDetails">
            <summary class="innerSummary">
              <div class="innerSummaryRow">
                <div class="innerSummaryText">
                  <div class="sumTitle">{{ h.habit }}</div>
                </div>
                <span class="togglePill togglePillSm" aria-hidden="true"></span>
              </div>
            </summary>

            <div class="hr2"></div>

            <div class="row badgesLine">
              <span class="badge">top_n: <code>{{ habitTopN(h) }}</code></span>
              <span class="badge">threshold: <code>{{ habitThreshold(h) }}</code></span>
              <span class="badge">score: <code>{{ fmtScore(h.score) }}</code></span>

              <span v-if="h.reason" class="badge badgeWide">
                reason: <span class="reasonText">{{ h.reason }}</span>
              </span>
            </div>

            <div class="hr2"></div>

            <div class="muted sectionLabel"></div>
            <ContextLabels :contexts="h.contexts || []" />
          </details>
        </div>
      </details>

      <div class="hr2"></div>

      <!-- ===== Block 4 ===== -->
      <details class="details blockDetails">
        <summary class="blockSummary">
          <div class="blockTitle">bilded profiles</div>

          <div class="blockRight">
            <div class="metaBadges">
              <span class="badge">provider: <code>{{ profMeta.provider || "-" }}</code></span>
              <span class="badge">model: <code>{{ profMeta.model || "-" }}</code></span>
            </div>
            <span class="togglePill togglePillSm" aria-hidden="true"></span>
          </div>
        </summary>

        <div class="hr2"></div>

        <div v-if="!profileDetailed" class="muted">No profile detailed.</div>
        <div v-else class="muted" style="white-space: pre-wrap; line-height: 1.55">
          {{ profileDetailed }}
        </div>
      </details>

      <div class="hr2"></div>

      <!-- ===== Block 5 ===== -->
      <details class="details blockDetails" open>
        <summary class="blockSummary">
          <div class="blockTitle">feedback</div>

          <div class="blockRight">
            <span class="togglePill togglePillSm" aria-hidden="true"></span>
          </div>
        </summary>

        <div class="hr2"></div>

        <label class="muted label"></label>
        <textarea class="textarea feedbackTextarea" v-model="commentText" rows="4"
          placeholder="Write a short feedback (optional)…" :disabled="commentBusy"></textarea>

        <div class="row feedbackActions">
          <button class="btn primary bigBtn btnFx" :disabled="commentBusy || !commentReady" @click="saveFeedback">
            {{ commentBusy ? "Saving..." : "Save comment" }}
          </button>

          <button class="btn bigBtn btnFx" :disabled="loading || !canSubmit" @click="submit">
            Regenerate recommendations
          </button>
        </div>

        <div v-if="commentOk" class="muted" style="margin-top: 8px">
          Feedback has been successfully submitted!
        </div>

        <div v-if="commentError" class="card errorCard" style="margin-top: 10px">
          <div class="errTitle">Error</div>
          <div class="muted" style="white-space: pre-wrap">{{ commentError }}</div>
        </div>
      </details>
    </div>
  </div>
</template>

<style scoped>
.page {
  max-width: 1100px;
  margin: 13px auto 0;
  padding: 0 14px 60px;

  --surface: rgba(255, 255, 255, 0.92);
  --surface2: rgb(248, 250, 252);
  --surface3: rgb(241, 245, 249);
  --border: rgba(15, 23, 42, 0.12);
  --border2: rgba(15, 23, 42, 0.10);
  --shadow1: 0 10px 20px rgba(15, 23, 42, 0.10);
  --shadow2: 0 6px 12px rgba(15, 23, 42, 0.08);

  --sub1: rgb(248, 251, 255);
  --sub2: rgb(244, 249, 255);
  --sub3: rgb(240, 247, 255);

  --subBorder1: rgba(59, 130, 246, 0.10);
  --subBorder2: rgba(59, 130, 246, 0.14);
  --subBorder3: rgba(59, 130, 246, 0.16);
}

.recCard {
  padding: 16px 18px 20px;
  border-radius: 18px;
  min-height: 600px;
  font-size: 14px;
}

.bigTextarea::placeholder {
  color: rgba(15, 23, 42, 0.45);
  opacity: 1;
}

/* header */
.headerRow {
  justify-content: space-between;
  align-items: flex-start;
}

.title {
  font-weight: 900;
  font-size: 18px;
}

.desc {
  font-size: 13px;
  margin-top: 6px;
}

/* main input row */
.mainRow {
  gap: 16px;
  align-items: stretch;
}

.left {
  flex: 1;
  min-width: 340px;
}

.label {
  font-size: 13px;
}

.textarea {
  min-height: 440px;
  resize: vertical;
}

.bigTextarea {
  min-height: 440px;
  resize: vertical;
}

.hint {
  margin-top: 8px;
  font-size: 12px;
  opacity: 0.75;
}

.right {
  width: 260px;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
}

.bigBtn {
  padding: 10px 12px;
  border-radius: 12px;
}

.right .bigBtn {
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.2;
}

.spacer {
  flex: 1;
  min-height: 0;
  max-height: 385px;
}

/* errors */
.errorCard {
  border-color: rgba(239, 68, 68, 0.25);
  background: rgba(239, 68, 68, 0.04);
}

.errTitle {
  font-weight: 800;
  margin-bottom: 4px;
}

.respCard {
  background: transparent;
}

.details {
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px 12px;
  background: var(--surface);
}

.details summary {
  cursor: pointer;
  list-style: none;
}

.details summary::-webkit-details-marker {
  display: none;
}

.blockDetails {
  padding: 12px 14px;
}

.blockSummary {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.blockTitle {
  font-weight: 800;
  font-size: 14px;
  line-height: 1.2;
}

.blockRight {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  flex: 0 0 auto;
}

.metaBadges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
  align-items: center;
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.innerDetails {
  background: #fff;
  border-color: var(--border2);
}

.selectedHabitItem {
  background: var(--sub1);
  border-color: var(--subBorder2);
}

.innerDetails2 {
  background: #fff;
  border-color: var(--border2);
}

.innerSummary {
  display: block;
}

/* ---------- Toggle Pill helpers ---------- */
.togglePill {
  border: 1px solid var(--border);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  padding: 10px 14px;
  border-radius: 12px;

  font-weight: 800;
  text-decoration: none;
  color: var(--text);

  display: inline-flex;
  align-items: center;
  gap: 8px;

  user-select: none;
  white-space: nowrap;
}

.blockSummary .togglePill,
.innerSummary .togglePill,
.hitSummary .togglePill {
  border-color: rgba(59, 130, 246, 0.25);
  background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%);
}

.togglePillSm {
  padding: 10px 12px;
  border-radius: 12px;
  font-size: 13px;
}

.innerSummaryRow {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.innerSummaryText {
  flex: 1;
  min-width: 0;
}

.innerSummaryRow .togglePill {
  margin-left: auto;
  flex: 0 0 auto;
}

.hitSummary {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hitBadges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.hitSummary .togglePill {
  margin-left: auto;
  flex: 0 0 auto;
}

summary .togglePill::after {
  content: "Expand Labels";
}

details[open]>summary .togglePill::after {
  content: "Collapse Labels";
}

/* ---------------------------------------- */

.sumTitle {
  font-weight: 700;
  font-size: 13px;
  line-height: 1.35;
}

.sumSub {
  font-size: 12px;
  margin-top: 4px;
  opacity: 0.78;
}

.sumSubInline {
  font-size: 12px;
  margin-left: 10px;
  opacity: 0.78;
}

.sectionLabel {
  font-size: 13px;
  opacity: 0.8;
  margin-bottom: 6px;
}

/* kv */
.kv {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 10px;
  padding: 6px 0;
}

@media (max-width: 900px) {
  .kv {
    grid-template-columns: 1fr;
  }
}

.k {
  font-weight: 650;
  font-size: 12px;
  color: rgba(15, 23, 42, 0.72);
}

.v {
  font-size: 13px;
}

.badgesLine {
  gap: 10px;
  flex-wrap: wrap;
  align-items: flex-start;
}

.badgeWide {
  flex: 1;
  min-width: 260px;
  max-width: 100%;
}

.reasonText {
  white-space: pre-wrap;
  word-break: break-word;
}

.hitLine {
  border: 1px solid var(--border2);
  border-radius: 12px;
  padding: 8px 10px;
  background: #fff;
}

/* feedback */
.feedbackTextarea {
  resize: vertical;
  min-height: 96px;
  max-width: 97%;
}

.feedbackActions {
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.btnFx {
  background: rgb(248, 250, 252) !important;
  border-color: rgb(226, 232, 240) !important;
  filter: none !important;

  position: relative;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  transition:
    transform 140ms ease,
    box-shadow 140ms ease,
    border-color 140ms ease,
    background-color 140ms ease;
}

.btnFx:hover {
  background: rgb(241, 245, 249) !important;
  border-color: rgb(203, 213, 225) !important;
  opacity: 1 !important;
  filter: none !important;

  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.10);
}

.btnFx:active {
  background: rgb(226, 232, 240) !important;
  opacity: 1 !important;
  filter: none !important;

  transform: translateY(0) scale(0.97);
  box-shadow: 0 6px 12px rgba(15, 23, 42, 0.08);
}

.btn.primary.btnFx {
  background: rgb(239, 246, 255) !important;
  border-color: rgb(191, 219, 254) !important;
  color: rgb(37, 99, 235) !important;
}

.btn.primary.btnFx:hover {
  background: rgb(219, 234, 254) !important;
  border-color: rgb(147, 197, 253) !important;
}

.btn.primary.btnFx:active {
  background: rgb(191, 219, 254) !important;
}

.btnFx:disabled,
.btnFx[aria-disabled="true"] {
  transform: none !important;
  box-shadow: none !important;
  cursor: not-allowed;
  opacity: 1 !important;
  filter: none !important;
}

.hr3 {
  height: 5px;
  border: 0;
  margin: 0;
}
</style>
