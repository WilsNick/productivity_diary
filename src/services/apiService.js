// src/services/apiService.js

// Base URL for the backend server
const BASE_URL = 'http://localhost:5000'; // Update with your actual backend URL

// Service object containing various API calls
export const apiService = {

  // Fetch existing projects based on category
  async getExistingProjects(category) {
    try {
      const response = await fetch(`${BASE_URL}/get-existing-projects?category=${category}`);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to get existing projects: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error getting existing projects: ${error.message}`);
    }
  },

  // Fetch all submissions based on category
  async getAllSubmissions(category) {
    try {
      const response = await fetch(`${BASE_URL}/get-all-submissions?category=${category}`);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to get all submissions: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error getting all submissions: ${error.message}`);
    }
  },

  // Add a new project
  async addProject(data_form) {
    try {
      const response = await fetch(`${BASE_URL}/add-project`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_form),  // Wrap the project_title in an object
      });
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to add project: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error adding project: ${error.message}`);
    }
  },

  // Reset table based on category
  async resetTable(category) {
    try {
      const response = await fetch(`${BASE_URL}/reset-table?category=${category}`);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to reset table: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error resetting table: ${error.message}`);
    }
  },

  // Submit time for a project
  async submitTime(formData) {
    try {
      const response = await fetch(`${BASE_URL}/submit-time`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to submit time: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error submitting time: ${error.message}`);
    }
  },

  // Update project information
  async updateProject(updatedProject) {
    try {
      const response = await fetch(`${BASE_URL}/update-project`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedProject),
      });
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to update project: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error updating project: ${error.message}`);
    }
  },

  // Update todo information
  async updateTodo(updatedTodo) {
    try {
      const response = await fetch(`${BASE_URL}/update-todo`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedTodo),
      });
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to update todo: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error updating todo: ${error.message}`);
    }
  },

  // Update a single todo
  async updatedSingleTodo(updatedSingleTodo) {
    try {
      const response = await fetch(`${BASE_URL}/update-single-todo`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedSingleTodo),
      });
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to update todo: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error updating todo: ${error.message}`);
    }
  },

  // Add a new todo
  async addTodo(AddTodo) {
    try {
      const response = await fetch(`${BASE_URL}/add-todo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(AddTodo),
      });
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to update todo: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error updating todo: ${error.message}`);
    }
  },

  // Get project information based on projectId
  async getProjectInfo(projectId) {
    try {
      const response = await fetch(`${BASE_URL}/get-project-info?projectId=${projectId}`);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to get project details: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error getting project details: ${error.message}`);
    }
  },

  // Get total time spent on a project based on projectTitle
  async getTimeSpent(projectTitle) {
    try {
      const response = await fetch(`${BASE_URL}/sum_time_spent?project_title=${projectTitle}`);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        throw new Error(`Failed to get project details: ${data.error}`);
      }
    } catch (error) {
      throw new Error(`Error getting project details: ${error.message}`);
    }
  }

};
