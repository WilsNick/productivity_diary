<template>
    <div class="project-form">
      <div class="project-list">
        <h3>All Projects:</h3>
        <div v-for="project in existingProjects" :key="project.id" @click="selectProject(project)">
          <div class="project-card">
            {{ project.title }}
          </div>
        </div>
      </div>
  
      <div class="project-details">
        <h3>Project Details:</h3>
        <div v-if="selectedProject">
          <h4>
            <span v-if="!isEditing">{{ selectedProject.title }}</span>
            <input v-if="isEditing" v-model="editedProject.title" />
          </h4>
          <p>
            <strong>Description:</strong>
            <span v-if="!isEditing">{{ selectedProject.description }}</span>
            <textarea v-if="isEditing" v-model="editedProject.description"></textarea>
          </p>
          <p><strong>Total Time Spent:</strong> {{ selectedProject.totalTimeSpent }} hours</p>
          <p><strong>Todos:</strong></p>
          <div class="draggable-columns">
        <!-- Draggable Todo Column -->
        <div class="draggable-column">
          <h3>Todo</h3>
          <draggable
            :list="list1"
            :disabled="enabled"
            item-key="id"
            class="list-group"
            ghost-class="ghost"
            :move="checkMove"
            @start="dragging = true"
            @end="dragging = false"
          >
            <template #item="{ element }">
              <div class="list-group-item" :class="{ 'not-draggable': !enabled }">
                {{ element.name }}
              </div>
            </template>
          </draggable>
        </div>

        <!-- Draggable In Progress Column -->
        <div class="draggable-column">
          <h3>In Progress</h3>
          <draggable
            :list="list2"
            :disabled="enabled"
            item-key="id"
            class="list-group"
            ghost-class="ghost"
            :move="checkMove"
            @start="dragging = true"
            @end="dragging = false"
          >
            <template #item="{ element }">
              <div class="list-group-item" :class="{ 'not-draggable': !enabled }">
                {{ element.name }}
              </div>
            </template>
          </draggable>
        </div>

        <!-- Draggable Done Column -->
        <div class="draggable-column">
          <h3>Done</h3>
          <draggable
            :list="list3"
            :disabled="enabled"
            item-key="id"
            class="list-group"
            ghost-class="ghost"
            :move="checkMove"
            @start="dragging = true"
            @end="dragging = false"
          >
            <template #item="{ element }">
              <div class="list-group-item" :class="{ 'not-draggable': !enabled }">
                {{ element.name }}
              </div>
            </template>
          </draggable>
        </div>
          </div>
          <ul>
            <li v-for="todo in selectedProject.todos" :key="todo.id">{{ todo.task }}</li>
          </ul>
  
            <button @click="toggleEditing" style="margin-right: 1rem;">
                {{ isEditing ? 'Save Changes' : 'Edit Project' }}
            </button>
            <button v-if="isEditing" @click="cancelEditing" style="margin-right: 1rem;">Cancel</button>

        </div>
        <div v-else>
          <p>Select a project to view details.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { apiService } from "@/services/apiService";
//   import TaskBoard from "./TaskBoard.vue";
import draggable from 'vuedraggable';

  export default {
    name: 'ProjectsPage',
    data() {
        return {
            existingProjects: [],
            selectedProject: "",
            list1: [
        { id: 1, name: 'Item 1' },
        { id: 2, name: 'Item 2' },
        // Add more items as needed
      ],
      list2: [
        { id: 3, name: 'Item 3' },
        { id: 4, name: 'Item 4' },
        // Add more items as needed
      ],
      list3: [
        { id: 5, name: 'Item 5' },
        { id: 6, name: 'Item 6' },
        // Add more items as needed
      ],
            // selectedProject: null,
            isEditing: false,
            editedProject: {
                id: null,
                title: '',
                description: '',
            },
        };
    },
    methods: {
        handleColumnChange(event) {
      console.log('Column changed:', event);
    },
    handleItemChange(event) {
      console.log('Item changed:', event);
    },
        async fetchExistingProjects() {
            try {
                const response = await apiService.getExistingProjects("Projects");
                if (response.projects) {
                    this.existingProjects = response.projects;
                }
                else {
                    console.error('Error: Unexpected response format from the server.');
                }
            }
            catch (error) {
                console.error('Error fetching existing projects:', error);
            }
        },
        selectProject(project) {
            this.selectedProject = project;
        },
        toggleEditing() {
            if (this.isEditing) {
                this.saveProject();
            }
            else {
                // If entering edit mode, pre-fill the edited project with the selected project's data
                this.editedProject = {
                    id: this.selectedProject.id,
                    title: this.selectedProject.title,
                    description: this.selectedProject.description,
                };
            }
            this.isEditing = !this.isEditing;
        },
        cancelEditing() {
            // If canceling edits, reset the edited project and exit edit mode
            this.editedProject = {};
            this.isEditing = false;
        },
        async saveProject() {
            try {
                // Call the API endpoint to update the project
                const response = await apiService.updateProject(this.editedProject);
                console.log('Response from server:', response);
                // Refresh the project list
                await this.fetchExistingProjects();
                // Reset editing state
                this.isEditing = false;
                this.editedProject = {
                    id: null,
                    title: '',
                    description: '',
                };
            }
            catch (error) {
                console.error('Error updating project:', error);
            }
        },
    },
    mounted() {
        this.fetchExistingProjects();
    },
    components: {
      draggable,
    },
    // components: { TaskBoard }
};
  </script>
  
  <style scoped>
  .project-form {
    display: flex;
    gap: 20px;
  }
  
  .project-list {
    width: 40%;
  }
  
  .project-card {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    cursor: pointer;
  }
  
  .project-details,
  .project-details h4,
  .project-details p,
  .project-details ul,
  .project-details li {
    margin: 0;
    padding: 0;
  }
  
  .project-details h4 {
    color: #3498db;
  }
  
  .project-details p {
    margin-bottom: 10px;
  }
  
  .project-details button {
    background-color: #3498db;
    color: #fff;
    border: none;
    padding: 8px 12px;
    margin-top: 10px;
    cursor: pointer;
  }
  .draggable-columns {
    display: flex;
    gap: 20px; /* Adjust the gap between columns */
  }

  .draggable-column {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .draggable-column h3 {
    margin-bottom: 10px;
    color: #3498db; /* Adjust the color as needed */
  }
  .project-details button:hover {
    background-color: #2980b9;
  }
  
  textarea {
    width: 100%;
    height: 80px;
  }
  </style>
  