// Streams a book's PDF from the GitHub release to the in-site reader.
// GitHub does not allow browsers to read release files directly (no CORS),
// so this relay forwards the request, keeps byte-range support (the reader
// loads big books page by page) and returns the file inline.
export const config = { runtime: "edge" };

const REPO = "https://github.com/Alidodkhonov/kitobxona/releases/download";

export default async function handler(req) {
  const url = new URL(req.url);
  const id = url.searchParams.get("id") || "";
  const tag = url.searchParams.get("t") || "";
  if (!/^\d{1,6}$/.test(id) || !/^b[1-9]$/.test(tag)) {
    return new Response("Bad request", { status: 400 });
  }
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });

  const upstreamHeaders = {};
  const range = req.headers.get("range");
  if (range) upstreamHeaders["range"] = range;

  let res;
  try {
    res = await fetch(`${REPO}/${tag}/${id}.pdf`, { headers: upstreamHeaders, redirect: "follow" });
  } catch (e) {
    return new Response("Upstream error", { status: 502, headers: cors() });
  }
  if (!res.ok && res.status !== 206) {
    return new Response("Not found", { status: res.status === 404 ? 404 : 502, headers: cors() });
  }

  const h = cors();
  h.set("Content-Type", "application/pdf");
  h.set("Content-Disposition", `inline; filename="${id}.pdf"`);
  h.set("Accept-Ranges", "bytes");
  for (const k of ["content-length", "content-range", "etag", "last-modified"]) {
    const v = res.headers.get(k);
    if (v) h.set(k, v);
  }
  h.set("Cache-Control", "public, max-age=86400, s-maxage=604800");
  h.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(res.body, { status: res.status, headers: h });
}

function cors() {
  const h = new Headers();
  h.set("Access-Control-Allow-Origin", "*");
  h.set("Access-Control-Allow-Headers", "Range");
  h.set("Access-Control-Expose-Headers", "Content-Length, Content-Range, Accept-Ranges");
  return h;
}
