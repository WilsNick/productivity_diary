<!-- src/App.vue -->

<template>
  <div id="app">
    <HelloWorld />
    <MyForm @formSubmitted="handleFormSubmission" />
    <DisplayData />
    <RemoveAllDataButton />
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld";
import MyForm from "@/components/MyForm";
import DisplayData from "@/components/DisplayData";
import RemoveAllDataButton from "@/components/RemoveAllDataButton";

export default {
  name: "App",
  components: {
    HelloWorld,
    MyForm,
    DisplayData,
    RemoveAllDataButton,
  },
  methods: {

  },
};
</script>

<style>
#app {
  background-color: black;
  color: white; /* Set text color to white for better visibility on a black background */
  min-height: 100vh; /* Ensure the background covers the entire viewport height */
}
</style>
