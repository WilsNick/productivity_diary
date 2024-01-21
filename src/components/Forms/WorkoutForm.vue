<!-- src/components/WorkoutForm.vue -->

<template>
  <div class="workout-form">
    <div v-for="(exercise, exerciseIndex) in exercises" :key="exerciseIndex" class="exercise-container">
      <div class="form-section">
        <label for="existingExercises">Select Existing Exercise:</label>
        <select id="existingExercises" v-model="exercise.selectedExistingExercise">
          <option value="" disabled>Select an existing exercise</option>
          <option v-for="existingExercise in existingExercises" :key="existingExercise.id" :value="existingExercise">{{ existingExercise }}</option>
        </select>
      </div>

      <div class="form-section">
        <label :for="'newExercise' + exerciseIndex">New Exercise:</label>
        <div class="new-exercise-row">
          <input :type="'text'" :id="'newExercise' + exerciseIndex" v-model="exercise.newExercise" class="large-input" />
          <button @click="createExercise(exerciseIndex)" class="small-btn">Add Exercise</button>
        </div>
      </div>

      <div class="form-section">
        <label>Sets:</label>
        <div v-for="(set, setIndex) in exercise.sets" :key="setIndex" class="set-container">
          <div class="set-input">
            <label :for="'reps' + exerciseIndex + setIndex">Reps:</label>
            <input :type="'reps' + exerciseIndex + setIndex" :id="'reps' + exerciseIndex + setIndex" v-model="set.reps" class="small-input" />
          </div>
          <div class="set-input">
            <label :for="'rest' + exerciseIndex + setIndex">Rest (seconds):</label>
            <input :type="'rest' + exerciseIndex + setIndex" :id="'rest' + exerciseIndex + setIndex" v-model="set.rest" class="small-input" />
          </div>
          <button @click="removeSet(exerciseIndex, setIndex)" class="remove-set-btn">Remove Set</button>
        </div>
      </div>

      <button @click="addSet(exerciseIndex)" class="add-set-btn">Add Set</button>
    </div>

    <div class="form-section">
      <button @click="addExercise" class="add-exercise-btn">Add Exercise</button>
      <button @click="submit" class="submit-btn">Submit</button>
      <button @click="resetTable" class="reset-table-btn">Reset Table</button>
    </div>

    <div class="form-section" style="text-align: center; margin-top: 1rem;">
      <button @click="getAllSubmissions" class="get-submissions-btn">Get All Submissions</button>
    </div>

    <div v-if="allSubmissions && allSubmissions.length > 0" class="form-section">
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
.workout-form {
  max-width: 800px;
  margin: auto;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.exercise-container {
  margin-bottom: 1.5rem;
}

.set-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.form-section {
  margin-bottom: 1.5rem;
}

label {
  font-weight: bold;
}

input,
select,
button {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  background-color: #007bff; /* Matching header color */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 1rem;
  transition: background-color 0.3s ease;
}

.small-input {
  width: 40%;
}

.large-input {
  width: 60%;
}
.new-exercise-row {
  display: flex;
  gap: 0.5rem; /* Adjust the gap as needed */
}

.new-exercise-row input {
  flex: 1;
}

.small-btn {
  width: 30%; /* Adjust the width as needed */
}

.add-set-btn,
.remove-set-btn {
  width: 30%;
}

.add-exercise-btn,
.submit-btn,
.reset-table-btn,
.get-submissions-btn {
  width: 32%;
  margin: 0.5%;
  display: inline-block;
}

.add-exercise-btn,
.submit-btn,
.reset-table-btn,
.get-submissions-btn {
  background-color: #007bff;
  color: #fff;
}
.small-btn,
.large-btn,
.submit-btn,
.reset-table-btn,
.remove-set-btn,
.add-set-btn,
.add-exercise-btn,
.get-submissions-btn {
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 1rem;
  transition: background-color 0.3s ease;
}

.small-btn:hover,
.large-btn:hover,
.submit-btn:hover,
.reset-table-btn:hover,
.remove-set-btn:hover,
.add-set-btn:hover,
.add-exercise-btn:hover,

.get-submissions-btn:hover {
  background-color: #0056b3; /* Darker shade on hover */
}

.reset-table-btn {
  background-color: #dc3545;
}
</style>