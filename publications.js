// Search box and topic filters for the publications page.
// Each entry is <div class="pub filterable kw1 kw2 ...">; keywords are classes.
(function () {
  const list = document.getElementById("pub-list");
  const search = document.getElementById("pub-search");
  const buttons = document.querySelectorAll(".pub-filter");
  const count = document.getElementById("pub-count");
  if (!list || !search || !count || buttons.length === 0) {
    throw new Error("publications.js: expected page elements not found");
  }
  const entries = Array.from(list.querySelectorAll(".pub.filterable"));
  const headings = Array.from(list.querySelectorAll("h2"));
  let topic = "all";

  function text(el, selector) {
    const node = el.querySelector(selector);
    return node ? node.textContent.toLowerCase() : "";
  }

  function update() {
    const query = search.value.trim().toLowerCase();
    let shown = 0;
    for (const el of entries) {
      const topicOK = topic === "all" || el.classList.contains(topic);
      const queryOK = !query ||
        text(el, ".pub-title").includes(query) || text(el, ".pub-authors").includes(query);
      const visible = topicOK && queryOK;
      el.hidden = !visible;
      if (visible) shown++;
    }
    // Hide a section heading when none of its entries are visible.
    for (const h of headings) {
      let any = false;
      for (let el = h.nextElementSibling; el && el.tagName !== "H2"; el = el.nextElementSibling) {
        if (el.classList.contains("pub") && !el.hidden) { any = true; break; }
      }
      h.hidden = !any;
    }
    count.textContent = (shown === entries.length)
      ? `${entries.length} publications`
      : `Showing ${shown} of ${entries.length} publications`;
  }

  for (const b of buttons) {
    b.addEventListener("click", () => {
      topic = b.dataset.filter;
      buttons.forEach(x => x.classList.toggle("active", x === b));
      update();
    });
  }
  search.addEventListener("input", update);
  update();
})();
