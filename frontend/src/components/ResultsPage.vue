<template>
    <div class="container mt-5">
      <h1>Results</h1>
      <div v-if="results">
        <h2>Summary</h2>
        <p>{{ results.summary }}</p>
  
        <h2>Entities</h2>
        <ul>
          <li v-for="(entity, index) in results.entities" :key="index">
            <strong>{{ entity[0] }}</strong> - {{ entity[1] }}
          </li>
        </ul>
  
        <h2>Tokens</h2>
        <p>{{ results.tokens.join(", ") }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ResultsPage",
    data() {
      return {
        results: null,
      };
    },
    async created() {
      try {
        const response = await axios.get("http://localhost:5001/results");
        this.results = response.data;
      } catch (error) {
        console.error("Failed to load results:", error);
      }
    },
  };
  </script>
  