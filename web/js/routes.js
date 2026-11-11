// Routes of the site: "#/" (home), "#/<page>", "#/<page>/<anchor>". Pure functions, no DOM.

/** "#/03-money/округление" → {page: "03-money", anchor: "округление"}; unknown → home. */
export function parse(hash, known = null) {
  const m = String(hash || "").match(/^#\/([^/]*)(?:\/(.+))?$/);
  let page = m ? m[1] || "home" : "home";
  let anchor = m && m[2] ? safeDecode(m[2]) : "";
  if (known && !known.includes(page)) {
    page = "home";
    anchor = "";
  }
  return { page, anchor };
}

export function href(page, anchor = "") {
  const base = page === "home" ? "#/" : `#/${page}`;
  return anchor ? `${base}/${encodeURIComponent(anchor)}` : base;
}

function safeDecode(text) {
  try {
    return decodeURIComponent(text);
  } catch {
    return text;
  }
}
