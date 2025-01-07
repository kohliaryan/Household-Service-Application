import ServicsCard from "../components/ServicsCard.js";
import LoginPage from "../pages/LoginPage.js";
import RegisterPage from "../pages/RegisterPage.js";
import SrevicesList from "../pages/SrevicesList.js";

const Home = {
  template: `<h1> This is Home </h1>`,
};

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/services", component: SrevicesList },
];
const router = new VueRouter({
  routes,
});
export default router;
