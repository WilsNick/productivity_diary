<template>
  <div class="project-page-form">
    <div class="project-list">
      <h2>All Projects:</h2>
      <div v-for="project in existingProjects" :key="project.id" @click="selectProject(project.id)">
        <div class="project-card">
          {{ project.title }}
        </div>
      </div>

    </div>


    <div class="project-details">
      <h2>Project Details:</h2>
      <div v-if="selectedProject.id">
        <div class="title-container">
          <h1 :class="{ 'editing': isEditing }">
            <span v-if="!isEditing">{{ selectedProject.title }}</span>
            <input v-if="isEditing" v-model="editedProject.title" class="edit-input" />
          </h1>

          <div class="button-container">
            <button @click="toggleEditing" class="btn primary">
              {{ isEditing ? 'Save Changes' : 'Edit Project' }}
            </button>
            <button v-if="isEditing" @click="cancelEditing" class="btn secondary">Cancel</button>
          </div>
        </div>
        <p>
          <strong>Description:</strong><br />
          <span v-if="!isEditing">{{ selectedProject.description }}</span>
          <textarea v-if="isEditing" v-model="editedProject.description" class="edit-desc-input"></textarea>
        </p>
        <p :class="{ 'editing': isEditing }"><strong>Total Hours Spent:</strong>
          <br />{{ selectedProject.totalTimeSpent || 0 }} hours
        </p>


        <div>
          <button @click="toggleProjectForm" class="btn primary">
            {{ showProjects ? 'Close Form' : 'Add Entry' }}
          </button>

          <ProjectForm v-if="showProjects" />

        </div>
        <br>



        <div class="row">
          <div class="col-4" style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
            <h3>Todo</h3>
            <draggable class="list-group" :list=list1 group="people" @change="handleChange" itemKey="task">
              <template #item="{ element, index }">
                <div class="list-group-item">
                  <span v-if="!editingItem || (editingItem.list !== list1 || editingItem.index !== index)">
                    {{ element.task }}
                  </span>
                  <input v-else ref="editItemInput" v-model="editedItemTitle" @keyup.enter="$event.target.blur()"
                    @blur="saveEditedItem" />
                  <button v-if="!editingItem || (editingItem.list !== list1 || editingItem.index !== index)"
                    class="edit-button" @click="startEditingItem(list1, index)">
                    Edit
                  </button>
                </div>
              </template>
            </draggable>
            <button @click="startAddingItem(list1)" class="btn">Add Item</button>
            <div v-if="addingItem === list1">
              <input ref="newItemInput" v-model="newItemTitle" @keyup.enter="addItemToList(list1)" />
              <button @click="addItemToList(list1)" class="btn">Done</button>
            </div>
          </div>




          <div class="col-4" style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
            <h3>In progress</h3>
            <draggable class="list-group" :list="list2" group="people" @change="handleChange" itemKey="task">
              <template #item="{ element, index }">
                <div class="list-group-item">
                  <span v-if="!editingItem || (editingItem.list !== list2 || editingItem.index !== index)">
                    {{ element.task }}
                  </span>
                  <input v-else ref="editItemInput" v-model="editedItemTitle" @keyup.enter="$event.target.blur()"
                    @blur="saveEditedItem" />
                  <button v-if="!editingItem || (editingItem.list !== list2 || editingItem.index !== index)"
                    class="edit-button" @click="startEditingItem(list2, index)">
                    Edit
                  </button>
                </div>
              </template>
            </draggable>
            <button @click="startAddingItem(list2)" class="btn">Add Item</button>
            <div v-if="addingItem === list2">
              <input ref="newItemInput" v-model="newItemTitle" @keyup.enter="addItemToList(list2)" />
              <button @click="addItemToList(list2)">Done</button>
            </div>
          </div>


          <div class="col-4" style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
            <h3>Done</h3>
            <draggable class="list-group" :list="list3" group="people" @change="handleChange" itemKey="task">
              <template #item="{ element, index }">
                <div class="list-group-item">
                  <span v-if="!editingItem || (editingItem.list !== list3 || editingItem.index !== index)">
                    {{ element.task }}
                  </span>
                  <input v-else ref="editItemInput" v-model="editedItemTitle" @keyup.enter="$event.target.blur()"
                    @blur="saveEditedItem" />
                  <button v-if="!editingItem || (editingItem.list !== list3 || editingItem.index !== index)"
                    class="edit-button" @click="startEditingItem(list3, index)">
                    Edit
                  </button>
                </div>
              </template>
            </draggable>
            <button @click="startAddingItem(list3)" class="btn">Add Item</button>
            <div v-if="addingItem === list3">
              <input ref="newItemInput" v-model="newItemTitle" @keyup.enter="addItemToList(list3)" />
              <button @click="addItemToList(list3)">Done</button>
            </div>
          </div>
        </div>


        <div class="col-4" style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
          <h3 style="color: red;">Remove todos</h3>
          <draggable class="list-group" :list="list4" group="people" @change="handleChange" itemKey="task">
            <template #item="{ element, index }">
              <div class="list-group-item">
                <span v-if="!editingItem || (editingItem.list !== list4 || editingItem.index !== index)">
                  {{ element.task }}
                </span>

              </div>
            </template>
          </draggable>
        </div>



        <br>

        <div class="form-section" style="text-align: center; margin-top: 1rem;">
          <button @click="getAllSubmissions" class="get-submissions-btn">Get All Submissions</button>
        </div>
        <div v-if="allSubmissions && allSubmissions.length > 0" class="form-section">
          <h3>All Submissions:</h3>
          <ul>
            <li v-for="submission in allSubmissions" :key="submission.id">
              {{ submission.project_name }} - {{ submission.time_spent }} hours - {{ submission.description }} ({{
                submission.submission_date }})
            </li>
          </ul>
        </div>

      </div>
      <div v-else>
        <p>Select a project to view details.</p>
      </div>

    </div>

  </div>
</template>



<script>
import { projectsPageMethods } from "./ProjectsPageMethods";
import draggable from 'vuedraggable';
import ProjectForm from "./Forms/ProjectForm.vue";

export default {
  name: 'ProjectsPage',
  data() {
    return {
      existingProjects: [],
      selectedProject: {
        id: null,
        title: '',
        todos: {
          todo: [{ id: 1, name: "iiiiiiih" }],
          inProgress: [],
          done: [],
        },
        description: '',
        totalTimeSpent: 0,
      },
      list1: [
      ],
      list2: [
      ],
      list3: [
      ],
      list4: [
      ],
      isEditing: false,
      editedProject: {
        id: null,
        title: '',
        description: '',
      },
      addingItem: null,
      editingItem: null,
      newItemTitle: '',
      editedItemTitle: '',
      showProjects: false,
      allSubmissions: [], // Initialize allSubmissions as an empty array
    };
  },
  methods: projectsPageMethods,
  mounted() {
    this.fetchExistingProjects();
  },
  components: {
    draggable,
    ProjectForm,
  },
};
</script>


<style scoped>
.project-page-form {
  display: flex;
  gap: 20px;
}

.project-list {
  width: 30%;
  margin-left: 1rem;
}

.project-list h2 {
  color: #225cee;
  /* Highlight color */
}

.project-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  background: #ffffff;
  /* Card background color */
  transition: background 0.3s ease;
}

.project-card:hover {
  background: #ecf0f1;
  /* Change background on hover */
}

.project-details {
  width: 70%;
}

.project-details h2 {
  color: #225cee;
  /* Highlight color */
}

.project-details h1 {
  color: #2c3e50;
}

.row {
  display: flex;
  justify-content: space-between;
}

.col-4 {
  flex: 1;
  margin-right: 20px;
  /* Adjust the margin between columns */
}

.list-group {
  background-color: #ecf0f1;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.list-group-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

.btn {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-right: 10px;
  border-radius: 5px;
  /* Add border-radius for a rounded button */
  transition: background 0.3s ease;
}

.btn.secondary {
  background-color: #e74c3c;
}

.btn:hover {
  background-color: #0056b3;
  /* Darker shade on hover */
}

.editing {
  font-size: 1.5em;
  /* Adjust the font size as needed */
}

.edit-input {
  font-size: 1.5em;
  /* Adjust the font size as needed */
}

.edit-desc-input {

  font-size: 1em;
  width: 75%;
  height: 10rem;
}

.item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-button {
  margin-left: 10px;
}

.form-section {
  margin-bottom: 1.5rem;
}

.edit-button,
.get-submissions-btn {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.title-container {
  display: flex;
  align-items: center;
}

.button-container {
  margin-left: 2rem;
  /* Adjust the margin as needed */
}

.get-submissions-btn:hover {
  background-color: #0056b3;
  /* Darker shade on hover */
}
</style>