import { createRouter, createWebHistory } from "vue-router";
import FileUploader from "../components/FileUploader.vue";
import ResultsPage from "../components/ResultsPage.vue";

const routes = [
  { path: "/", component: FileUploader },
  { path: "/results", component: ResultsPage },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
