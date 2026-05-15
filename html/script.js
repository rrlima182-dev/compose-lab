let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function saveTasks() {
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function addTask() {
  const name = document.getElementById('taskName').value.trim();
  const time = document.getElementById('taskTime').value;
  const priority = document.getElementById('taskPriority').value;

  if (!name) {
    alert('Digite o nome da tarefa.');
    return;
  }

  if (time) {
    const now = new Date();
    const currentTime = now.toTimeString().slice(0, 5);

    if (time <= currentTime) {
      alert('Esse horário já passou. Escolha um horário futuro.');
      return;
    }
  }

  const task = {
    id: Date.now(),
    name,
    time: time || 'Sem horário',
    priority,
    done: false
  };

  tasks.push(task);
  tasks.sort((a, b) => a.time.localeCompare(b.time));

  saveTasks();
  renderTasks();

  document.getElementById('taskName').value = '';
  document.getElementById('taskTime').value = '';
  document.getElementById('taskPriority').value = 'baixa';
}

function toggleTask(id) {
  tasks = tasks.map(task => {
    if (task.id === id) {
      return { ...task, done: !task.done };
    }

    return task;
  });

  saveTasks();
  renderTasks();
}

function deleteTask(id) {
  tasks = tasks.filter(task => task.id !== id);

  saveTasks();
  renderTasks();
}

function updateDashboard() {
  const total = tasks.length;
  const done = tasks.filter(task => task.done).length;
  const pending = tasks.filter(task => !task.done).length;
  const high = tasks.filter(task => task.priority === 'alta').length;

  document.getElementById('totalTasks').innerText = total;
  document.getElementById('doneTasks').innerText = done;
  document.getElementById('pendingTasks').innerText = pending;
  document.getElementById('highTasks').innerText = high;
}

function renderTasks() {
  const taskList = document.getElementById('taskList');

  taskList.innerHTML = '';

  updateDashboard();

  if (tasks.length === 0) {
    taskList.innerHTML = '<p class="empty">Nenhuma tarefa cadastrada ainda.</p>';
    return;
  }

  tasks.forEach(task => {
    const div = document.createElement('div');

    div.className = `task ${task.done ? 'done' : ''}`;

    div.innerHTML = `
      <div class="task-info">
        <div class="task-title">${task.name}</div>
        <div class="task-meta">
          ${task.time} · 
          <span class="priority ${task.priority}">
            ${task.priority}
          </span>
        </div>
      </div>

      <div class="actions">
        <button class="small-btn" onclick="toggleTask(${task.id})">
          ${task.done ? 'Voltar' : 'Feito'}
        </button>

        <button class="small-btn delete" onclick="deleteTask(${task.id})">
          Excluir
        </button>
      </div>
    `;

    taskList.appendChild(div);
  });
}

function loadTheme() {
  const savedTheme = localStorage.getItem('theme') || 'dark';

  document.body.classList.remove('light-mode', 'dark-mode');
  document.body.classList.add(`${savedTheme}-mode`);

  const button = document.getElementById('themeButton');

  if (button) {
    button.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
  }
}

function toggleTheme() {
  const isDark = document.body.classList.contains('dark-mode');
  const newTheme = isDark ? 'light' : 'dark';

  localStorage.setItem('theme', newTheme);

  loadTheme();
}

renderTasks();
loadTheme();