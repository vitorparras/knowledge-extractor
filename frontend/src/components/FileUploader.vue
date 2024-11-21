<template>
    <div class="container mt-5">
      <h1>Upload File</h1>
      <form @submit.prevent="uploadFile">
        <input type="file" @change="onFileChange" class="form-control mb-3" />
        <button type="submit" class="btn btn-primary">Upload</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        file: null,
      };
    },
    methods: {
      onFileChange(event) {
        this.file = event.target.files[0];
      },
      async uploadFile() {
        const formData = new FormData();
        formData.append("file", this.file);
  
        try {
          const response = await axios.post('http://localhost:5001/api/upload', formData);
          
          console.log(response);

          this.$router.push("/results");
        } catch (error) {
          console.error("Upload failed:", error);
        }
      },
    },
  };
  </script>
  