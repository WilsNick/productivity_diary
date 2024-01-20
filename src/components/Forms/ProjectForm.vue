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
      <button @click="submit">Submit</button>

      <br><br>
      <button @click="getAllSubmissions">Get All Submissions</button>

    <!-- Display the fetched submissions -->
    <div v-if="allSubmissions && allSubmissions.length > 0">
      <h3>All Submissions:</h3>
      <ul>
        <li v-for="submission in allSubmissions" :key="submission.id">
          {{ submission.project_name }} - {{ submission.time_spent }} hours - {{ submission.description }} ({{ submission.submission_date }})
        </li>
      </ul>
    </div>
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
      allSubmissions: [], // Initialize allSubmissions as an empty array

    };
  },
  methods: {
    
    async submit() {
      try {
        // Check if selectedExistingProject is not empty and a number
        if (this.selectedExistingProject) {
          const formData = {
            category: "Projects",
            project_name: this.selectedExistingProject,
            time_spent: this.timeSpent,
            description: this.description,
          };

          // Call the API endpoint to submit the time data
          const response = await apiService.submitTime(formData);

          console.log('Response from server:', response);

          // Reset the form fields to their initial state
          this.timeSpent = 0;
          this.description = '\u2022 ';
        } else {
          console.error('Invalid selectedExistingProject value.');
          console.error(this.selectedExistingProject);
        }
      } catch (error) {
        console.error('Error submitting time:', error);
      }
    },

    async fetchExistingProjects() {
      try {

        // Fetch the list of existing projects from the server
        const response = await apiService.getExistingProjects("Projects");

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
        const data_form = {
          category: "Projects",
          title: this.NewProject
        }
        // Fetch the list of existing projects from the server
        await apiService.addProject(data_form);

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
            await apiService.resetTable("Projects");
            console.log('Table reset successful');

            // After resetting the table, fetch the updated list of existing projects
            this.fetchExistingProjects();
        } catch (error) {
            console.error('Error resetting table:', error);
        }
    },
    addBulletPoint() {
      // Check if the description is empty or doesn't start with a bullet point
      if (!this.description.trim() || !this.description.startsWith('\u2022 ')) {
        this.description += '\u2022 '; // Add a bullet point
      } else {
        // Add a new line with another bullet point
        this.description += '\n\u2022 '; // '\n' for a new line
      }
    },
    async getAllSubmissions() {
        try {

          // Fetch all submissions from the server
          const response = await apiService.getAllSubmissions("Projects");
          console.log(response);
          // Update the allSubmissions array with the fetched data
          this.allSubmissions = response.submissions;

        } catch (error) {
            console.error('Error fetching all submissions:', error);
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
