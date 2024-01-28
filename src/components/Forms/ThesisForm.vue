<!-- src/components/ThesisForm.vue -->

<template>
  <div class="thesis-form">
    <div class="form-row">
      <div class="form-column">
        <label for="existingProjects">Select Existing Component:</label>
        <select id="existingProjects" v-model="selectedExistingProject">
          <option value="" disabled>Select an existing component</option>
          <option v-for="project in existingProjects" :key="project.id" :value="project">{{ project }}</option>
        </select>
      </div>
      <div class="form-column">
        <label for="newProject">New Component:</label>
        <div class="new-project-row">
          <input type="text" id="newProject" v-model="newProject" class="large-input" />
          <button @click="addProject" class="small-btn">Add Component</button>
        </div>
      </div>
    </div>

    <div class="form-section">
      <label for="timeSpent">Time Spent (in hours):</label>
      <div class="input-section">
        <input type="number" id="timeSpent" v-model="timeSpent" class="small-input" />
      </div>
    </div>

    <div class="form-section">
      <label for="description">Description:</label>
      <div class="input-section">
        <textarea id="description" v-model="description" @keydown.enter.prevent="addBulletPoint" rows="4"
          class="description-input"></textarea>
      </div>
    </div>

    <div class="form-section" style="text-align: center;">
      <button @click="submit" class="submit-btn">Submit</button>
      <button @click="resetTable" class="reset-table-btn">Reset Table</button>
    </div>

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
</template>


<script>
import { apiService } from "@/services/apiService";

export default {
  data() {
    return {
      NewProject: "",
      timeSpent: 0,
      existingProjects: [],
      selectedExistingProject: "",
      description: '\u2022 ',
      allSubmissions: [], // Initialize allSubmissions as an empty array
      category: "Thesis"

    };
  },
  methods: {

    async submit() {
      try {
        // Check if selectedExistingProject is not empty and a number
        if (this.selectedExistingProject) {
          const formData = {
            category: this.category,
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
        const response = await apiService.getExistingProjects(this.category);

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
          category: this.category,
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
        const response = await apiService.getAllSubmissions(this.category);
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
.thesis-form {
  max-width: 800px;
  margin: auto;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-column {
  flex: 1 1 100%;
  max-width: calc(50% - 0.75rem);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.new-project-row {
  display: flex;
  gap: .5rem;
}

.form-section {
  margin-bottom: 1.5rem;
}

.input-section {
  margin-top: 1rem;
}

label {
  font-weight: bold;
}

input,
select,
button,
textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  background-color: #007bff;
  /* Matching header color */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 1rem;
  transition: background-color 0.3s ease;
}

.small-input {
  width: 50%;
}

.large-input {
  width: 75%;
}

.description-input {
  width: calc(100% - 2rem);
  /* Adjusted width to prevent overflow */
}

.small-btn {
  width: 40%;
}

.submit-btn,
.get-submissions-btn,
.reset-table-btn {
  width: 48%;
  margin: 0.5%;
  display: inline-block;
}

.submit-btn {
  background-color: #007bff;
  color: white;
}

.reset-table-btn {
  background-color: #dc3545;
  color: white;
}

.get-submissions-btn {
  background-color: #007bff;
  color: white;
}

.reset-table-btn:hover,
.small-btn:hover,
.submit-btn:hover,
.get-submissions-btn:hover {
  background-color: #0056b3;
  /* Darker shade on hover */

}
</style>