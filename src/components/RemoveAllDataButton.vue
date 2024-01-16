<!-- src/components/RemoveAllDataButton.vue -->

<template>
    <button @click="removeAllData">Remove All Data</button>
  </template>
  
  <script>
  import { apiService } from "@/services/apiService";
  
  export default {
    methods: {
      async removeAllData() {
        try {
          const response = await apiService.removeAllData();
          console.log('Response from server:', response);
          // Handle the response as needed
        } catch (error) {
          console.error('Error removing data from server:', error);
          // Handle the error
        }
      },
    },
  };
  </script>
  