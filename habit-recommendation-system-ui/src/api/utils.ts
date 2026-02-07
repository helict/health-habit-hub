export const API_BASE =
  import.meta.env.VITE_HHH_BASE || "http://127.0.0.1:8081";

/**
 * Structured API error so UI can read HTTP status + backend JSON detail.
 */
export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data: any) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function isJsonContentType(ct: string | null) {
  if (!ct) return false;
  return ct.toLowerCase().includes("application/json");
}

/**
 * Fetch JSON with better error handling:
 * - On success: returns parsed JSON as T.
 * - On failure: throws ApiError(status, data) where data is parsed JSON if possible, else text.
 */
export async function jsonFetch<T>(
  input: RequestInfo,
  init?: RequestInit
): Promise<T> {
  const r = await fetch(input, init);

  const ct = r.headers.get("content-type");
  const wantJson = isJsonContentType(ct);

  let data: any = null;
  if (wantJson) {
    data = await r.json().catch(() => null);
  } else {
    data = await r.text().catch(() => "");
  }

  if (!r.ok) {
    const msg =
      (data && typeof data === "object" && (data?.detail?.message || data?.message)) ||
      (typeof data === "string" && data.trim()) ||
      `HTTP ${r.status}`;

    throw new ApiError(String(msg), r.status, data);
  }

  if (wantJson) return data as T;

  if (typeof data === "string") {
    const trimmed = data.trim();
    if (!trimmed) return (null as any) as T;
    try {
      return JSON.parse(trimmed) as T;
    } catch {
      return (data as any) as T;
    }
  }

  return data as T;
}

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
