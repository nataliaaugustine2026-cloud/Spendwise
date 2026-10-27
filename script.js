document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const categoryFilter = document.getElementById("categoryFilter");
  const sortFilter = document.getElementById("sortFilter");
  const rowsBody = document.getElementById("expenseRows");
  const resultCount = document.getElementById("resultCount");
  const themeToggle = document.getElementById("themeToggle");
  const editDialog = document.getElementById("editDialog");
  const editForm = document.getElementById("editForm");

  // Search, category filter, and sorting work directly on the rendered table.
  function filterAndSortRows() {
    const query = (searchInput?.value || "").trim().toLowerCase();
    const category = categoryFilter?.value || "";
    const sort = sortFilter?.value || "newest";
    const rows = [...rowsBody.querySelectorAll("tr[data-description]")];

    rows.forEach(row => {
      const matchesQuery = row.dataset.description.includes(query);
      const matchesCategory = !category || row.dataset.category === category;
      row.hidden = !(matchesQuery && matchesCategory);
    });

    const visibleRows = rows.filter(row => !row.hidden);
    visibleRows.sort((a, b) => {
      if (sort === "oldest") return a.dataset.date.localeCompare(b.dataset.date);
      if (sort === "high") return Number(b.dataset.amount) - Number(a.dataset.amount);
      if (sort === "low") return Number(a.dataset.amount) - Number(b.dataset.amount);
      return b.dataset.date.localeCompare(a.dataset.date);
    });
    visibleRows.forEach(row => rowsBody.appendChild(row));

    if (resultCount) resultCount.textContent = `Showing ${visibleRows.length} of ${rows.length} expense(s)`;
  }

  [searchInput, categoryFilter, sortFilter].forEach(element => {
    element?.addEventListener(element.tagName === "INPUT" ? "input" : "change", filterAndSortRows);
  });

  // Edit dialog: Flask receives the edited values at /edit/<id>.
  document.querySelectorAll(".edit-button").forEach(button => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".row-menu[open]").forEach(menu => menu.removeAttribute("open"));
      editForm.action = `/edit/${button.dataset.id}`;
      document.getElementById("editDescription").value = button.dataset.description;
      document.getElementById("editAmount").value = button.dataset.amount;
      document.getElementById("editCategory").value = button.dataset.category;
      document.getElementById("editDate").value = button.dataset.date;
      editDialog.showModal();
    });
  });

  document.getElementById("closeDialog")?.addEventListener("click", () => editDialog.close());
  editDialog?.addEventListener("click", event => {
    if (event.target === editDialog) editDialog.close();
  });

  // Theme preference is saved in the browser.
  const savedTheme = localStorage.getItem("spendwise-theme");
  if (savedTheme === "dark") document.body.classList.add("dark-theme");
  themeToggle?.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    localStorage.setItem(
      "spendwise-theme",
      document.body.classList.contains("dark-theme") ? "dark" : "light"
    );
  });

  // Simple SVG donut chart using the totals shown in the category legend.
  const donut = document.getElementById("donutChart");
  const legend = document.getElementById("categoryLegend");
  if (donut && legend) {
    const colors = ["#8b78e6", "#efad72", "#69b9a7", "#e7839b", "#7da7e8", "#d7c36d", "#b2a5c9"];
    const items = [...legend.querySelectorAll(".legend-row")].map(row => ({
      amount: Number((row.querySelector("strong")?.textContent || "").replace(/[₹,]/g, "")),
      color: getComputedStyle(row.querySelector("i")).backgroundColor
    })).filter(item => item.amount > 0);
    const total = items.reduce((sum, item) => sum + item.amount, 0);
    if (total > 0) {
      let current = 0;
      const stops = items.map((item, index) => {
        const start = current;
        current += item.amount / total * 100;
        return `${item.color} ${start}% ${current}%`;
      });
      donut.style.background = `conic-gradient(${stops.join(", ")})`;
    } else {
      donut.style.background = `conic-gradient(${colors[0]} 0 100%)`;
    }
  }

  // Set today's date in the add form if it has no value.
  const dateInput = document.getElementById("date");
  if (dateInput && !dateInput.value) {
    dateInput.value = new Date().toISOString().slice(0, 10);
  }
});
