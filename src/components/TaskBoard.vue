<template>
    <div>
      <div class="task-board">
        <draggable v-model="todoTasks" group="tasks" @change="handleTaskChange">
          <div class="task-column">
            <h3>Todo</h3>
            <div v-for="task in todoTasks" :key="task.id" class="task-item">
              {{ task.title }}
            </div>
          </div>
        </draggable>
  
        <draggable v-model="inProgressTasks" group="tasks" @change="handleTaskChange">
          <div class="task-column">
            <h3>In Progress</h3>
            <div v-for="task in inProgressTasks" :key="task.id" class="task-item">
              {{ task.title }}
            </div>
          </div>
        </draggable>
  
        <draggable v-model="doneTasks" group="tasks" @change="handleTaskChange">
          <div class="task-column">
            <h3>Done</h3>
            <div v-for="task in doneTasks" :key="task.id" class="task-item">
              {{ task.title }}
            </div>
          </div>
        </draggable>
      </div>
    </div>
  </template>
  
  <script>
  import draggable from 'vuedraggable';
  
  export default {
    components: {
      draggable,
    },
    data() {
      return {
        todoTasks: [
          { id: 1, title: 'Task 1' },
          { id: 2, title: 'Task 2' },
          // ... (other tasks)
        ],
        inProgressTasks: [
          // ... (tasks in progress)
        ],
        doneTasks: [
          // ... (completed tasks)
        ],
      };
    },
    methods: {
      handleTaskChange(event) {
        // Handle task changes here (e.g., update task status in the database)
        console.log('Task change:', event);
      },
    },
  };
  </script>
  
  <style>
  .task-board {
    display: flex;
  }
  
  .task-column {
    flex: 1;
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 8px;
  }
  
  .task-item {
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    padding: 8px;
    margin-bottom: 8px;
    border-radius: 4px;
  }
  </style>
  