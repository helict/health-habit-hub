<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { recommend, recommendComment } from "../api/hhh";
import type {
    RecommendOut,
    KbHit,
    RecommendCommentReq,
    SelectedHabitOut,
    HabitRecommendation,
} from "../api/types";
import ContextLabels from "./ContextLabels.vue";

const props = defineProps<{
    item: RecommendOut;
}>();

const localResp = ref<RecommendOut>(props.item);
watch(
    () => props.item,
    (v) => (localResp.value = v),
    { deep: true }
);

// feedback (comment)
const commentText = ref("");
const commentBusy = ref(false);
const commentOk = ref(false);
const commentError = ref<string | null>(null);

watch(
    () => localResp.value?.user_feedback,
    (v) => {
        commentText.value = v || "";
    },
    { immediate: true }
);

// ---- block #1: habit_recommendations ----
const recBlock = computed(() => localResp.value?.recommendation_results_outputs || null);
const recMeta = computed(() => recBlock.value?.llm_meta || {});
const recMessage = computed(() => recBlock.value?.message || "");
const habitRecs = computed<HabitRecommendation[]>(
    () => recBlock.value?.habit_recommendations || []
);

// ---- block #2: hits grouped by (domain -> book) ----
type HitLine = { page_number: number; score: number; text: string };
type BookGroup = { domain: string; doc_id: string; doc_title: string; lines: HitLine[] };
type DomainGroup = { domain: string; books: BookGroup[] };

const kbBlock = computed(() => localResp.value?.kb_queries || null);
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
            bookMap.set(bookKey, { domain, doc_id: h.doc_id, doc_title: docTitle, lines: [] });
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
const selBlock = computed(() => localResp.value?.selected_habits || null);
const selMeta = computed(() => selBlock.value?.llm_meta || {});
const selectedHabits = computed<SelectedHabitOut[]>(
    () => selBlock.value?.selected_habits || []
);

// ---- block #4: bilded_profiles ----
const profBlock = computed(() => localResp.value?.bilded_profiles || null);
const profMeta = computed(() => profBlock.value?.llm_meta || {});
const profileDetailed = computed(() => profBlock.value?.profile_detailed || "");

// ---- block #5: feedback ----
const commentReady = computed(() => {
    return Boolean(localResp.value?.request_uuid && localResp.value?.text && localResp.value?.text_signature);
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

async function saveFeedback() {
    commentError.value = null;
    commentOk.value = false;

    if (!localResp.value?.request_uuid || !localResp.value?.text || !localResp.value?.text_signature) {
        commentError.value = "Current results are missing the fields required to save feedback.";
        return;
    }

    const req: RecommendCommentReq = {
        request_uuid: localResp.value.request_uuid,
        text: localResp.value.text,
        text_signature: localResp.value.text_signature!,
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

const regenBusy = ref(false);
const regenError = ref<string | null>(null);

async function regen() {
    regenError.value = null;
    if (!localResp.value?.text) return;

    regenBusy.value = true;
    try {
        const r = await recommend(localResp.value.text.trim());
        localResp.value = r;
        commentText.value = r?.user_feedback || "";
        commentOk.value = false;
        commentError.value = null;
    } catch (e: any) {
        regenError.value = e?.message || String(e);
    } finally {
        regenBusy.value = false;
    }
}

function shortSig(sig?: string | null) {
    if (!sig) return "-";
    return sig.length <= 10 ? sig : sig.slice(0, 10) + "…";
}
</script>

<template>
    <details class="details historyItem">
        <summary class="historySummary">
            <div class="historyLeft">
                <span class="badge badgeGreen">goal</span>
                <div class="goalText" :title="localResp.text">{{ localResp.text }}</div>
            </div>

            <div class="historyRight">
                <!-- <span class="badge">created_at: <code>{{ localResp.created_at || "-" }}</code></span>
                <span class="badge">sig: <code>{{ shortSig(localResp.text_signature) }}</code></span> -->
                <span class="togglePill togglePillSm" aria-hidden="true"></span>
            </div>
        </summary>

        <div class="hr2"></div>

        <div class="card respCard" style="background: transparent; padding: 0; border: 0">
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

                <div class="hr2"></div>

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

                        <div class="hr2"></div>

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

                <div class="hr2"></div>

                <div v-if="groupedHits.length === 0" class="muted">No hits.</div>

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

                        <div class="hr2"></div>

                        <div class="stack">
                            <details v-for="bk in dg.books" :key="bk.doc_id + bk.doc_title"
                                class="details innerDetails2">
                                <summary class="innerSummary">
                                    <div class="innerSummaryRow">
                                        <div class="innerSummaryText">
                                            <div class="sumTitle">{{ bk.doc_title }}</div>
                                            <div class="muted sumSub">hits: <code>{{ bk.lines.length }}</code></div>
                                        </div>
                                        <span class="togglePill togglePillSm" aria-hidden="true"></span>
                                    </div>
                                </summary>

                                <div class="hr2"></div>

                                <div class="stack">
                                    <details v-for="(ln, idx) in bk.lines" :key="idx" class="hitLine">
                                        <summary class="hitSummary">
                                            <div class="hitBadges">
                                                <span class="badge">page: <code>{{ ln.page_number }}</code></span>
                                                <span class="badge">score: <code>{{ fmtScore(ln.score) }}</code></span>
                                            </div>
                                            <span class="togglePill togglePillSm" aria-hidden="true"></span>
                                        </summary>

                                        <div class="hr2"></div>
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

                <div v-if="!profileDetailed" class="muted">No profile_detailed.</div>
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

                <div v-if="!localResp.user_feedback" class="muted">No user feedback.</div>

                <div v-else class="muted" style="white-space: pre-wrap; line-height: 1.55">
                    {{ localResp.user_feedback }}
                </div>
            </details>
        </div>
    </details>
</template>

<style scoped>
.historyItem {
    border: 1px solid rgba(15, 23, 42, 0.12);
    border-radius: 16px;
    padding: 10px 12px;
    background: rgba(255, 255, 255, 0.92);
}

.historySummary {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: flex-start;
    cursor: pointer;
    list-style: none;
}

.historySummary::-webkit-details-marker {
    display: none;
}

.historyLeft {
    display: flex;
    gap: 10px;
    align-items: center;
    min-width: 0;
}

.goalText {
    font-weight: 800;
    font-size: 13px;
    line-height: 1.35;
    max-width: 680px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.historyRight {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
    align-items: center;
}

.badgeGreen {
    border-color: rgba(16, 185, 129, 0.35) !important;
    background: linear-gradient(180deg, rgba(209, 250, 229, 0.9) 0%, rgba(167, 243, 208, 0.9) 100%) !important;
    color: rgb(48, 153, 120) !important;
    font-weight: 900;
}

.respCard {
    background: transparent;
}

.details {
    border: 1px solid rgba(15, 23, 42, 0.12);
    border-radius: 14px;
    padding: 10px 12px;
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
    background: rgba(255, 255, 255, 0.92);
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

.innerDetails,
.innerDetails2 {
    background: #fff;
    border-color: rgba(15, 23, 42, 0.10);
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
    border: 1px solid rgba(15, 23, 42, 0.10);
    border-radius: 12px;
    padding: 8px 10px;
    background: #fff;
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

.hr {
    height: 1px;
    background: rgba(15, 23, 42, 0.08);
    margin: 10px 0;
    border-radius: 999px;
}

.hr2 {
    height: 15px;
    border: 0;
    margin: 0;
}

.togglePill {
    border: 1px solid rgba(15, 23, 42, 0.12);
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%);
    padding: 10px 14px;
    border-radius: 12px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    user-select: none;
    white-space: nowrap;
}

.togglePillSm {
    padding: 10px 12px;
    border-radius: 12px;
    font-size: 13px;
}

summary .togglePill::after {
    content: "Expand Labels";
}

details[open]>summary .togglePill::after {
    content: "Collapse Labels";
}

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

.errorCard {
    border-color: rgba(239, 68, 68, 0.25);
    background: rgba(239, 68, 68, 0.04);
}

.errTitle {
    font-weight: 800;
    margin-bottom: 4px;
}
</style>
