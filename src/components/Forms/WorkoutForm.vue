<!-- src/components/WorkoutForm.vue -->

<template>
  <div>
    <div v-for="(exercise, exerciseIndex) in exercises" :key="exerciseIndex">
      <label for="existingExercises">Select Existing component:</label>
      <select id="existingExercises" v-model="exercise.selectedExistingExercise">
        <option value="" disabled>Select an existing component</option>
        <option v-for="existingExercise in existingExercises" :key="existingExercise.id" :value="existingExercise">{{ existingExercise }}</option>
      </select>

      <label :for="'newExercise' + exerciseIndex">New exercise:</label>
      <input :type="'text'" :id="'newExercise' + exerciseIndex" v-model="exercise.newExercise" />


      <button @click="createExercise(exerciseIndex)">Add exercise</button>

      <br><br>

      <!-- Display sets with rep and rest fields -->
      <div v-for="(set, setIndex) in exercise.sets" :key="setIndex">
        <label :for="'reps' + exerciseIndex + setIndex">Reps:</label>
        <input :type="'reps' + exerciseIndex + setIndex" :id="'reps' + exerciseIndex + setIndex" v-model="set.reps" />

        <label :for="'rest' + exerciseIndex + setIndex">Rest (seconds):</label>
        <input :type="'rest' + exerciseIndex + setIndex" :id="'rest' + exerciseIndex + setIndex" v-model="set.rest" />

        <button @click="removeSet(exerciseIndex, setIndex)">Remove Set</button>
      </div>

      <button @click="addSet(exerciseIndex)">Add Set</button>

    </div>

    <button @click="addExercise">Add exercise</button>
    <button @click="submit">Submit</button>
    <button @click="resetTable">Reset Table</button>

      <br><br>
      <button @click="getAllSubmissions">Get All Submissions</button>

    <!-- Display the fetched submissions -->
    <div v-if="allSubmissions && allSubmissions.length > 0">
      <h3>All Submissions:</h3>
      <ul>
        <li v-for="workout in allSubmissions" :key="workout.submission_date">
          <strong>Submission Date:</strong> {{ workout.submission_date }}
          <ul>
            <li v-for="exercise in workout.exercises" :key="exercise.exercise_name">
              <strong>Exercise:</strong> {{ exercise.exercise_name }}
              <ul>
                <li v-for="set in exercise.sets" :key="set.reps">
                  Reps: {{ set.reps }}, Rest: {{ set.rest }}
                </li>
              </ul>
            </li>
          </ul>
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
      NewExercises:[],
      existingExercises: [],
      selectedExistingExercise: "",
      allSubmissions: [], // Initialize allSubmissions as an empty array
      category: "Workouts",
      exercises: [{ selectedExistingExercise: '', newExercise: '', sets: [{ reps: 0, rest: 0 }] }],



    };
  },
  methods: {
    
    async submit() {
      try {
        let can_send = true;
        // Check if selectedExistingExercise is not empty and a number
        for (const exercise of this.exercises) {
          console.log(exercise);
          if(!exercise.selectedExistingExercise){
            can_send = false;
          }
        } 
        if (can_send) {
          const formData = {
            category: this.category,
            exercises: this.exercises,
          };

          // Call the API endpoint to submit the time data
          const response = await apiService.submitTime(formData);

          console.log('Response from server:', response);
              this.exercises = [{ selectedExistingExercise: '', newExercise: '', sets: [{ reps: 0, rest: 0 }] }];
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
    addExercise() {
      // Add a new exercise with default values
      this.exercises.push({selectedExistingExercise: '', newExercise: '', sets: [{ reps: 0, rest: 0 }] });
    },

    async createExercise(exerciseIndex) {
      try {
        const data_form = {
          category: this.category,
          title: this.exercises[exerciseIndex].newExercise
        }

        // Fetch the list of existing projects from the server
        await apiService.addProject(data_form);

        // Update the existingExercises array with the fetched data
        await this.fetchExistingExercises()
        const newIndex = this.existingExercises.indexOf(this.exercises[exerciseIndex].newExercise);

        // Set selectedExistingExercise to the newly added project title
        this.exercises[exerciseIndex].selectedExistingExercise = newIndex !== -1 ? this.existingExercises[newIndex] : '';

        // this.selectedExistingExercise = this.newExercise;

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },

    async resetTable() {
        try {
            // Call the resetTable method from your apiService
            await apiService.resetTable(this.category);
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
    addSet(exerciseIndex) {
      // Add a new set to the specified exercise
      this.exercises[exerciseIndex].sets.push({ reps: 0, rest: 0 });
    },

    removeSet(exerciseIndex, setIndex) {
      // Remove the set at the specified index from the specified exercise
      this.exercises[exerciseIndex].sets.splice(setIndex, 1);
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
