<!-- src/components/WorkoutForm.vue -->

<template>
  <div>
      <label for="existingExercises">Select Existing exercise:</label>
      <select id="existingExercises" v-model="selectedExistingExercise">
        <option value="" disabled>Select an existing exercise</option>
        <option v-for="exercise in existingExercises" :key="exercise.id" :value="exercise">{{ exercise }}</option>
      </select>

      <label for="NewExercise">New exercise:</label>
      <input type="text" id="NewExercise" v-model="NewExercise" />

      <button @click="addExercise">Add exercise</button>

      <button @click="resetTable">Reset Table</button>

      <br><br>

      <br><br>

      <!-- Display sets with rep and rest fields -->
      <div v-for="(set, index) in sets" :key="index">
        <label :for="'reps' + index">Reps:</label>
        <input :type="'reps' + index" :id="'reps' + index" v-model="set.reps" />

        <label :for="'rest' + index">Rest (seconds):</label>
        <input :type="'rest' + index" :id="'rest' + index" v-model="set.rest" />

        <button @click="removeSet(index)">Remove Set</button>
      </div>

      <button @click="addSet">Add Set</button>
      <button @click="submit">Submit</button>

      <br><br>
      <button @click="getAllSubmissions">Get All Submissions</button>

    <!-- Display the fetched submissions -->
    <div v-if="allSubmissions && allSubmissions.length > 0">
      <h3>All Submissions:</h3>
      <ul>
        <li v-for="submission in allSubmissions" :key="submission.id">
          {{ submission.project_name }} - {{ submission.reps }} reps - {{ submission.description }} ({{ submission.submission_date }})
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
      NewExercise:"",
      reps: 0,
      existingExercises: [],
      selectedExistingExercise: "",
      description: '\u2022 ',
      allSubmissions: [], // Initialize allSubmissions as an empty array
      category: "Thesis",
      sets: [{ reps: 0, rest: 0 }], // Array to store sets with reps and rest


    };
  },
  methods: {
    
    async submit() {
      try {
        // Check if selectedExistingExercise is not empty and a number
        if (this.selectedExistingExercise) {
          const formData = {
            category: this.category,
            project_name: this.selectedExistingExercise,
            time_spent: this.reps,
          };

          // Call the API endpoint to submit the time data
          const response = await apiService.submitTime(formData);

          console.log('Response from server:', response);

          // Reset the form fields to their initial state
          this.reps = 0;
          this.description = '\u2022 ';
        } else {
          console.error('Invalid selectedExistingExercise value.');
          console.error(this.selectedExistingExercise);
        }
      } catch (error) {
        console.error('Error submitting time:', error);
      }
    },

    async fetchExistingExercises() {
      try {

        // Fetch the list of existing projects from the server
        const response = await apiService.getExistingProjects(this.category);

        // Ensure that the 'projects' property exists in the response
        if (response.projects) {
          // Extract the 'title' from each project and update the existingExercises array
          this.existingExercises = response.projects.map(project => project.title);
          console.log(this.existingExercises);
        } else {
          console.error('Error: Unexpected response format from the server.');
        }

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },


    async addExercise() {
      try {
        const data_form = {
          category: this.category,
          title: this.NewExercise
        }
        // Fetch the list of existing projects from the server
        await apiService.addProject(data_form);

        // Update the existingExercises array with the fetched data
        await this.fetchExistingExercises()
        const newIndex = this.existingExercises.indexOf(this.NewExercise);

        // Set selectedExistingExercise to the newly added project title
        this.selectedExistingExercise = newIndex !== -1 ? this.existingExercises[newIndex] : '';

        // this.selectedExistingExercise = this.NewExercise;

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
            this.fetchExistingExercises();
        } catch (error) {
            console.error('Error resetting table:', error);
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
    addSet() {
      // Add a new set with default values for reps and rest
      this.sets.push({ reps: 0, rest: 0 });
    },
    removeSet(index) {
      // Remove the set at the specified index
      this.sets.splice(index, 1);
    },
  },
  mounted() {
    // Fetch the list of existing projects when the component is mounted
    this.fetchExistingExercises();
  },
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
