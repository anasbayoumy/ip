// ============================================================
// MODEL — Task data structure
// ============================================================
class Task {
  constructor(description) {
    this.id          = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    this.description = description.trim();
    this.completed   = false;
    this.createdAt   = new Date().toISOString();
  }
  toggle()   { this.completed = !this.completed; }
  edit(text) { this.description = text.trim(); }
}

// ============================================================
// MODEL — Task collection + persistence
// ============================================================
class TaskModel {
  constructor() {
    this.tasks = this._load();
  }
  _load() {
    try {
      const raw = localStorage.getItem('taskflow_22p0011');
      if (!raw) return [];
      return JSON.parse(raw).map(d => Object.assign(new Task(d.description), d));
    } catch { return []; }
  }
  _save() {
    localStorage.setItem('taskflow_22p0011', JSON.stringify(this.tasks));
  }
  add(description) {
    const t = new Task(description);
    this.tasks.push(t);
    this._save();
    return t;
  }
  remove(id) {
    this.tasks = this.tasks.filter(t => t.id !== id);
    this._save();
  }
  toggle(id) {
    const t = this.tasks.find(t => t.id === id);
    if (t) { t.toggle(); this._save(); }
  }
  edit(id, text) {
    const t = this.tasks.find(t => t.id === id);
    if (t) { t.edit(text); this._save(); }
  }
  getFiltered(filter, sort) {
    let list = [...this.tasks];
    if (filter === 'completed') list = list.filter(t => t.completed);
    if (filter === 'pending')   list = list.filter(t => !t.completed);
    if (sort === 'time-asc')    list.sort((a, b) => a.createdAt.localeCompare(b.createdAt));
    if (sort === 'time-desc')   list.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    if (sort === 'alpha-asc')   list.sort((a, b) => a.description.localeCompare(b.description));
    if (sort === 'alpha-desc')  list.sort((a, b) => b.description.localeCompare(a.description));
    return list;
  }
}

// ============================================================
// VIEW — DOM rendering
// ============================================================
class TaskView {
  constructor() {
    this.listEl      = document.getElementById('taskList');
    this.inputEl     = document.getElementById('taskInput');
    this.addBtn      = document.getElementById('addBtn');
    this.filterBtns  = document.querySelectorAll('.btn-filter');
    this.sortSel     = document.getElementById('sortSelect');
    this.totalEl     = document.getElementById('totalCount');
    this.doneEl      = document.getElementById('doneCount');
    this.pendingEl   = document.getElementById('pendingCount');
    this.pctEl       = document.getElementById('pctCount');
    this.progressEl  = document.getElementById('progressBar');
  }

  renderList(tasks) {
    if (!tasks.length) {
      this.listEl.innerHTML = `
        <div class="empty-state">
          <span class="emoji">📋</span>
          <p>No tasks here yet. Start adding!</p>
        </div>`;
      return;
    }
    this.listEl.innerHTML = tasks.map(t => this._taskHTML(t)).join('');
  }

  _taskHTML(t) {
    const date = new Date(t.createdAt);
    const ts   = date.toLocaleDateString('en-GB', { day:'2-digit', month:'short' })
               + ' · ' + date.toLocaleTimeString('en-GB', { hour:'2-digit', minute:'2-digit' });
    return `
    <div class="task-item${t.completed ? ' done' : ''}" data-id="${t.id}">
      <div class="task-check" data-action="toggle">${t.completed ? '✓' : ''}</div>
      <div class="task-body">
        <div class="task-text" data-action="toggle">${this._esc(t.description)}</div>
        <div class="task-time">🕐 ${ts}</div>
      </div>
      <div class="task-actions">
        <div class="btn-icon btn-edit" data-action="edit" title="Edit">✏️</div>
        <div class="btn-icon btn-delete" data-action="delete" title="Delete">🗑️</div>
      </div>
    </div>`;
  }

  _esc(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  showEditMode(id, currentText) {
    const el = this.listEl.querySelector(`[data-id="${id}"] .task-body`);
    if (!el) return;
    el.innerHTML = `
      <input class="task-edit-input" value="${this._esc(currentText)}" data-edit-id="${id}" />
      <div class="task-time">Press Enter or click 💾 to save</div>`;
    const item = this.listEl.querySelector(`[data-id="${id}"] .btn-edit`);
    if (item) { item.textContent = '💾'; item.classList.add('btn-save'); item.classList.remove('btn-edit'); }
    el.querySelector('input').focus();
  }

  getEditValue(id) {
    const inp = this.listEl.querySelector(`[data-edit-id="${id}"]`);
    return inp ? inp.value : null;
  }

  animateRemove(id, cb) {
    const el = this.listEl.querySelector(`[data-id="${id}"]`);
    if (el) {
      el.classList.add('removing');
      setTimeout(cb, 300);
    } else { cb(); }
  }

  updateStats(tasks) {
    const total   = tasks.length;
    const done    = tasks.filter(t => t.completed).length;
    const pending = total - done;
    const pct     = total ? Math.round((done / total) * 100) : 0;
    this.totalEl.textContent   = total;
    this.doneEl.textContent    = done;
    this.pendingEl.textContent = pending;
    this.pctEl.textContent     = pct + '%';
    this.progressEl.style.width = pct + '%';
  }

  setActiveFilter(f) {
    this.filterBtns.forEach(b => b.classList.toggle('active', b.dataset.filter === f));
  }

  getInput()     { return this.inputEl.value; }
  clearInput()   { this.inputEl.value = ''; this.inputEl.focus(); }
  getSortValue() { return this.sortSel.value; }
}

// ============================================================
// CONTROLLER — wires Model + View + events
// ============================================================
class TaskController {
  constructor(model, view) {
    this.model     = model;
    this.view      = view;
    this.filter    = 'all';
    this.editingId = null;

    // Bind events
    this.view.addBtn.addEventListener('click',   () => this._addTask());
    this.view.inputEl.addEventListener('keydown', e => { if (e.key === 'Enter') this._addTask(); });
    this.view.sortSel.addEventListener('change',  () => this._render());
    this.view.filterBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        this.filter = btn.dataset.filter;
        this.view.setActiveFilter(this.filter);
        this._render();
      })
    );
    this.view.listEl.addEventListener('click', e => this._handleListClick(e));
    this.view.listEl.addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.target.classList.contains('task-edit-input')) {
        const id = e.target.dataset.editId;
        if (id) this._saveEdit(id);
      }
    });

    this._render();
  }

  _addTask() {
    const text = this.view.getInput().trim();
    if (!text) { this.view.inputEl.focus(); return; }
    this.model.add(text);
    this.view.clearInput();
    this._render();
  }

  _handleListClick(e) {
    const btn  = e.target.closest('[data-action]');
    if (!btn) return;
    const item = btn.closest('[data-id]');
    if (!item) return;
    const id     = item.dataset.id;
    const action = btn.dataset.action;

    if (action === 'delete') {
      this.view.animateRemove(id, () => {
        this.model.remove(id);
        this._render();
      });
    } else if (action === 'toggle') {
      this.model.toggle(id);
      this._render();
    } else if (action === 'edit') {
      this.editingId = id;
      const task = this.model.tasks.find(t => t.id === id);
      if (task) this.view.showEditMode(id, task.description);
    } else if (btn.classList.contains('btn-save') || action === 'edit') {
      this._saveEdit(id);
    }
  }

  _saveEdit(id) {
    const val = this.view.getEditValue(id);
    if (val && val.trim()) {
      this.model.edit(id, val);
    }
    this.editingId = null;
    this._render();
  }

  _render() {
    const tasks    = this.model.tasks;
    const filtered = this.model.getFiltered(this.filter, this.view.getSortValue());
    this.view.renderList(filtered);
    this.view.updateStats(tasks);
  }
}

// ============================================================
// BOOTSTRAP
// ============================================================
const app = new TaskController(new TaskModel(), new TaskView());
