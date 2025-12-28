export const API_BASE =
  import.meta.env.VITE_HHH_BASE || "http://127.0.0.1:8081";

export async function jsonFetch<T>(
  input: RequestInfo,
  init?: RequestInit
): Promise<T> {
  const r = await fetch(input, init);
  if (!r.ok) {
    const text = await r.text().catch(() => "");
    throw new Error(text || `HTTP ${r.status}`);
  }
  return r.json() as Promise<T>;
}

/**
 * Mongo ObjectId → time (fallback)
 * ObjectId first 4 bytes = unix timestamp (seconds)
 */
export function createdAtFromObjectId(oid?: string | null): string | null {
  if (!oid || oid.length < 8) return null;
  try {
    const tsHex = oid.slice(0, 8);
    const tsMs = parseInt(tsHex, 16) * 1000;
    return new Date(tsMs).toISOString();
  } catch {
    return null;
  }
}

export function fmtTime(iso?: string | null): string {
  if (!iso) return "-";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export function round4(n: number) {
  return Math.round(n * 10000) / 10000;
}
