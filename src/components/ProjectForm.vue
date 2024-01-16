<!-- src/components/ProjectForm.vue -->

<template>
  <div>
      <!-- Show existing projects dropdown only if the selected category is "passion_project" -->
      <label for="existingProjects">Select Existing Project:</label>
      <select id="existingProjects" v-model="selectedExistingProject">
        <option value="" disabled>Select an existing project</option>
        <option v-for="project in existingProjects" :key="project.id" :value="project">{{ project }}</option>
      </select>

      <label for="NewProject">New project:</label>
      <input type="text" id="NewProject" v-model="NewProject" />

      <button @click="addProject">Add project</button>

      <button @click="resetTable">Reset Table</button>

      <br><br>

      <label for="timeSpent">Time Spent (in hours):</label>
      <input type="number" id="timeSpent" v-model="timeSpent" />

      <br><br>
      
      <label for="description">Description:</label>
      <textarea id="description" v-model="description" @keydown.enter.prevent="addBulletPoint" rows="4"></textarea>

      <br><br>

  </div>
</template>

<script>
import { apiService } from "@/services/apiService";

export default {
  data() {
    return {
      NewProject:"",
      timeSpent: 0,
      existingProjects: [],
      selectedExistingProject: "",
      description: '\u2022 ',

    };
  },
  methods: {
    
    async fetchExistingProjects() {
      try {
        // Fetch the list of existing projects from the server
        const response = await apiService.getExistingProjects();

        // Ensure that the 'projects' property exists in the response
        if (response.projects) {
          // Extract the 'title' from each project and update the existingProjects array
          this.existingProjects = response.projects.map(project => project.title);
          console.log(this.existingProjects);
        } else {
          console.error('Error: Unexpected response format from the server.');
        }

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },


    async addProject() {
      try {
        // Fetch the list of existing projects from the server
        await apiService.addProject(this.NewProject);

        // Update the existingProjects array with the fetched data
        await this.fetchExistingProjects()
        const newIndex = this.existingProjects.indexOf(this.NewProject);

        // Set selectedExistingProject to the newly added project title
        this.selectedExistingProject = newIndex !== -1 ? this.existingProjects[newIndex] : '';

        // this.selectedExistingProject = this.NewProject;

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },

    async resetTable() {
        try {
            // Call the resetTable method from your apiService
            await apiService.resetTable();
            console.log('Table reset successful');

            // After resetting the table, fetch the updated list of existing projects
            this.fetchExistingProjects();
        } catch (error) {
            console.error('Error resetting table:', error);
        }
    },
    addBulletPoint() {
      // Check if the description is empty or doesn't end with a bullet point
      if (!this.description.trim() || !this.description.endsWith('\u2022 ')) {
        this.description += '\u2022 '; // Add a bullet point
      } else {
        // Add a new line with another bullet point
        this.description += '\n\u2022 '; // '\n' for a new line
      }
    },
  },
  mounted() {
    // Fetch the list of existing projects when the component is mounted
    this.fetchExistingProjects();
  },
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
